
import logging

from itertools import takewhile
from more_itertools import before_and_after

logger = logging.getLogger(__name__)

class UnknownScanType(Exception): pass

class DataRepositoryBase:
    '''
    Abstract base class for `DataRepository` type of objects.

    The main purpose of a `DataRepository` is to provide listing
    and basic access to proposal data via `.all()`,
    respectively `.proposal()`.

    We'll also reuse the `.__dir__()` Python-builtin for
    listing the proposals, and the `.__getattr__()` for
    returning a proposal object.
    '''

    def __init__(self, url, spice_url=None):
        self._repo_url = url

        # We keep a local cache of proposal objects that we create.
        # This is because associated with a proposal, there may be
        # other associated (e.g. spice), and the expectation is that
        # <repo>.<proposal> conserves state.
        self._proposal_cache = {}

        self._spice_url = spice_url

    @property
    def spice_url(self):
        return self._spice_url

    @property
    def repo_url(self):
        '''
        The full repository URL as specified by user
        '''
        return self._repo_url


    def all(self):
        '''
        Returns a key->handle map for all
        proposals managed by this repository.
        '''
        raise RuntimeError('not implemented')


    def keys(self):
        return self.all().keys()


    def handles(self):
        return self.all().values()


    def _proposal(self, key):
        '''
        Returns a `DataProposal` object for the proposal of this
        repo designated by `handle` or by `key`.
        '''
        raise RuntimeError('not implemented')


    def proposal(self, *, handle=None, key=None):
        if key is None:
            try:
                key = {h:k for k,h in self.all().items()}[handle]
            except KeyError as e:
                logger.warning(f'msg="Proposal not present in spice repo" '
                               f'handle="{handle}" key="{key}"')

        return self._proposal_cache.setdefault(key, self._proposal(key))


    def __dir__(self):
        return super().__dir__()+[i for i in self.handles()]


    def __getattr__(self, handle):
        if handle not in self.handles():
            raise AttributeError(f'no such proposal: {handle}')        
        return self.proposal(handle=handle)


DataRepoBase = DataRepositoryBase

class DataScanBase:
    '''
    Abstract base class for `DataScan` objects.

    This is the main working unit for data preparation.
    A data scan is a series of data points ("frames" in
    `nx5d` lingo) collected in a single sweep or run of
    the measurement setup, for one particular scope.
    Generally, a "scan" has associated with it:
    
    - `.type`: a string that describes the type of scan,
      unambiguously within the framework of the data
      repository in use; scans of a type have the same
      data and positioners, and are to be analysed/processed
      in the same way. This is essential to determine the
      recipe for data processing.

    - `.summary`: a Key-Value store ("dictionary") of information
      that can be rapidly obtained about the scan without doing
      a full-open or full-retrieve of all the scan data.
      The specific keys are generally dependent on the exact
      `.type`, but they are all required to have at least
      a "description" field, which will be shown alongside
      name and kind in listings.

    - `.logbook`: a Markdown lab log book entry to accompany
      the scan

    - `.raw`: the collection of all data that was measured and
      is supposed to remain unchanged; typically, this is in
      some version of "device coordinate system" (angles,
      intensities, distances...). This is an `xarray.Dataset`.

    - `.cooked`: experimental data transformed into a
      physically more meaningful format; typically this involves
      coordinate transformation, interpolation, merging data
      points ("frames") into a larger whole. This also is an
      `xarray.Dataset`.
    
    - `.spice`: a collection of data ("spice data") required
      for processing ("cooking") the data from its raw form
      into a physically accessible form. This is typically a
      `nx5d.spice.SpiceView` object.
    '''

    def __init__(self, proposal, key):
        self._proposal = proposal
        self._scan_key = key
        self._summary = None

    def _get_summary(self):
        # Called to create a new summary object. Needs to implement
        # a mechanism to determine at least 'description' and 'type'.
        # Any other keys are optional, but will (eventually) be displayed
        # in human-readable listing forms occasionally.
        raise RuntimeError('not implemented')

    def _get_raw(self):
        # Loads raw data
        raise RuntimeError('not implemented')

    def _get_logentry(self):
        raise RuntimeError('not implemented')


    def _cook(self, data, **spice):
        '''
        Expected to return a cooked version of the data.

        This is what gets called under the hood when `.cooked`
        or similar functions are involved. This is intended for
        subclasses to (re)implement, not as a public use API.

        The default implementation checks for the existence of a
        spice type called "recipes". If it's not found, a `RuntimeError`
        is raised. If the "recipes" spice record is found, it is
        expected to be a dictionary with the following properties:
        - any key (except for `__default__`, see below) will be
          compared against this scan's type. If it matches, the data
          will be cooked by that recipe. The match is case-sensitive.
        - if no key is found by the name of this scan's type, but
          a `__default__` key exists, then the recipe of the default
          key is used.

        The preference is that recipes for every scan types are
        registered once, seeded in the beginning. Recipes for known
        types can be overridden according to spice rules; but spice
        rules also dictate that, once the "recipes" type is seeded,
        no new keys can be added or removed. This means that on new
        scan types can be implemented "on-the-fly". As a (deliberately
        ugly) workaround we honor the "__default__" key, to still
        make processing possible, but strongly encourage proper the
        beamline engineer to properly define their scan types instead
        of relying on later additions.

        For spice that is to be saved on-disk, the recipe must be defined
        as a string. The string has a URL-like format, pointing to a
        routine / callable with the signature
        `func(scan_type, input_data, **spice)` which must cook the data
        and return it -- see also: `nx5d.recipe:load_recipe()` for
        specific URL schemes.

        For purely in-memory spice types, the recipe can also be
        a reference to a Python callable.

        Args:
          data: input data
          **spice: spice keys and (view) values.

        Returns: the cooked data.
        '''
        if 'recipes' not in spice:
            raise RuntimeError('no recipes available and cooking not implemented')

        recipes = spice['recipes']
        try:
            rt = recipes[self.type]
        except KeyError:
            try: rt = recipes['__default__']
            except KeyError:
                raise RuntimeError(f'{self.type}: no recipe in '
                                   f'{spice["recipes"].keys} '
                                   f'and no __default__ mentioned')

        if isinstance(rt, str):
            rcall = self._load_recipe(rt)
        elif hasattr(rt, "__call__"):
            rcall = rt
        elif rt is None:
            rcall = lambda *a, **kw: None
        else:
            raise RuntimeError(f'unknown recipe spec: {rt}')

        return rcall(self.type, data, **spice)


    def _load_recipe(self, recipe_url):
        ## Loads the recipe from URL        
        import urllib
        from nx5d.recipe import load_recipe
        return load_recipe(recipe_url)


    @property
    def summary(self):
        if self._summary is None:
            try:
                self._summary = self._get_summary()
            except UnknownScanType:
                self._summary = {
                    'type': 'raw',
                    'descrption': 'raw'
                }
        return self._summary

    @property
    def url(self):
        return self._proposal.scan_url.format(scan=self.key)

    @property
    def key(self):
        return self._scan_key

    @property
    def type(self):
        return self.summary['type']

    @property
    def cooked(self):
        if not hasattr(self, '_cooked'):
            smap = {
                k:v.data() for k,v in self.spice.data.items()
            }
            self._cooked = self._cook(self.raw, **smap)
        return self._cooked

    @property
    def logbook(self):
        return self._get_logentry()

    @property
    def spice(self):
        if self._proposal.spice is not None:
            return self._proposal.spice.view(self._scan_key)


    @property
    def raw(self):
        if not hasattr(self, '_raw'):
            self._raw = self._get_raw()
        return self._raw

    def _repr_html_(self):
        return \
            '<table>'+\
              f'<tr><th>key</th><th>type</th>'+\
              ''.join([
                f'<th>{k}</th>' for k in
                filter(lambda x: x != 'type', self.summary.keys())
              ]) +\
              f'</tr>' +\
              f'<tr><td>{self.key}</td><td>{self.type}</td>'+''.join([
                f'<td>{v[1]}</td>' for v in
                filter(lambda x: x[0] != 'type', self.summary.items())
              ])+\
              f'</tr></table>'

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.key}]'


class StackedDataScan(DataScanBase):
    '''
    Implements access to a series of similar scans

    Delegates all access ("raw", "cooked" etc) to the underlying 
    '''

    def __init__(self, proposal, scans, coords, stype, key=None):
        '''
        Args:
          proposal: The parent proposal
        
          scans: A list of "key" arguments to pass to the underlying
            scan class.

          coords: List of coodinate names to stack along. For each of
            the coordinates, a new dimension will be prepended to the
            input data. `None` or empty list also accepted.

          stype: Deviation of the scan type to report when asked for
            `.type`. This can contain the `{}` formatter to be replaced
            with the type of the original scans (which should be the
            same for all scans in the series)

          key: The key of this scan
        '''
        if key is None:
            key = '-'.join([scans[0], scans[-1]])
        super().__init__(proposal, key)
        self._scan_keylist = scans
        self._scan_coords = coords
        self._reported_type = stype

    
    def _get_summary(self):
        smry = {}
        for s in self._scan_keylist:
            scan = self._proposal._scan(key=s)
            smry.update(scan.summary)
            smry['type'] = self._reported_type.format(s)
        return smry


    def _get_raw(self):
        # Stacks all raw data
        
        subscans = {
            k:self._proposal._scan(k) for k in self._scan_keylist
        }

        from xarray import concat as xr_cat

        data_stack = None
        for tmp in subscans.values():
            scan_data = tmp.raw
            scan_data['scan'] = tmp.key
            if data_stack is None:
                data_stack = scan_data
            else:
                data_stack = xr_cat([data_stack, scan_data], dim='index')

        # by this point, the data is already stacked along its natural
        # 'index' dimension; make sure all the coordinates are maked as
        # such.
        if (self._scan_coords is not None) and len(self._scan_coords) > 0:
            for c in self._scan_coords[::-1]:
                data_stack = data_stack.set_coords(c)

        return data_stack


    def _get_logentry(self):
        raise RuntimeError('not implemented')



class DataProposalBase:
    '''
    Abstract base class for `DataProposal` type of objects.

    A "proposal" is a collection of data scans (sometimes
    called "runs") which belong together historically and,
    generally, by topic.

    Generally, spice management starts at proposal level,
    although spice _access_ happens one level below (scan
    level).

    A proposal has:
    
    - `.handle`: a string to refer to the proposal to, suitable
      of being converted in a Python symbol name

    - `.key`: a string that the proposal will be recognized at
      in all other instances, in particular (but not limited to)
      at the repository level.

    - `.all()`: a list of all the handles of all its subscans
    '''

    def __init__(self, repo, key, spice=None):
        '''
        Constructs a proposal access object.

        This is never used directly, there are several implementations (see
        `nx5d.repo.filesystem.py` and `nx5d.repo.astor.py` for examples).
        Typically, they will _also_ need other information, e.g. a base
        URL of where to get the data from. But in any case, they need a
        reference to the parent repository object (`repo`) and an
        identifyable information (`key`) of the current proposal.
        
        Args:
          repo: The parent repository object
          key: Identifying information for this proposal
          spice: A `SpiceProposal` or `SpiceCollection` object.
            Defaults to `None` if not specified; in that case, a
            spice proposal from the parent object (`repo`) will
            be requested for the same key.
        '''
        self._repo = repo
        self._proposal_key = key
        
        if spice is not None:
            self._spice = spiece
        else:
            self._my_spice_repo = self._spice_repo()
            self._spice = self._spice_repo().proposal(key=key)


    def _spice_repo(self, spice_url=None):
        '''
        Called once, during `.__init__()`, to obtain a spice repository
        for this proposal. `spice_url` is an explicit spice repository
        URL to use. Typically, `spice_url` is only then different from
        `None` when the upper layers (e.g. a `Repository` class) was
        initialized by the user with a specific spice repo.

        If `spice_url` is `None`, the environment variable `NX5D_SPICE_REPO`
        will be queried first. If it is an empty string or unset, the
        parent repository's `.spice_url` property will be queried.
        If all these still end up in an undefined spice repo, then a
        memory-only spice repository is created specifically for this
        proposal.

        This method can be overwritten by derived classes to perform
        additional spice operations upon spice repo initialization (e.g.
        checking for and/or seeding default spice types for this specific
        data proposal).
        '''
        from os import environ
        if (spice_url is None):
            if (self._repo.spice_url is None):
                spi_url = environ.get('NX5D_SPICE_REPO', '')
            else:
                spi_url = self._repo.spice_url

        if spi_url in (None, ''):
            # Constructing a memory spice repo
            from nx5d.spice import MemorySpiceRepository
            s = MemorySpiceRepository()
            s.new(self._proposal_key)
            return s
        else:
            from nx5d.spice import FsSpiceRepository
            return FsSpiceRepository(spi_url)


    #def location(self, **k):
    #    '''
    #    Returns the base part of the URL, with all relevant keys (e.g.
    #    "{propsal}") already substituted. This is useful for lower classes
    #    (e.g. DataScan) to be able to construct paths relative to the base
    #    proposal folder.
    #    '''
    #    raise RuntimeError('not implemented')


    @property
    def key(self):
        return self._proposal_key


    @property
    def handle(self):
        return self.all()[self._proposal_key]

    @property
    def spice(self):
        return self._spice
    
    def _scan_candidates(self):
        '''
        Returns a key-handle map for all scans in this proposal.
        This is where the actual reading of the scan list is supposed to take
        place, and needs to be reimplemented by derived classes.
        '''
        raise RuntimeError('not implemented')


    def all(self):
        '''
        Returns a key-handle map for all scans in this proposal.

        This is the high-level function that is part of the API, and implements some
        additional logic. One of the things it implements is the "stack" logic, whereby
        we can instruct Nx5d to load several consecutive scans and stack them on top
        of one another, forming a new type (built-in, spice-triggered call to .stack(),
        so to speak -- an "autostacking" of sorts).

        Autostacking is controlled by means of a spice type "stack", with the following
        schema:
        ```
           "stack": {
               "type": str | None,
               "options": { ... }
           }
        ```
        Herein the fields have the following meaning:
        - type: the type to assign to the new virtual, stacked DataScan. If the type is
          `None` or an empty string, the previous stack series is ended, and no
          current series starts. If the type is any other string (even if it's the
          same as a previous one), a new stack series with the corresponding type is
          started.
        - options: Key-Value assignment passed along as keyword agruments to `.stack()`.
          Most interesting will probably be the `coords` key, an optional, list of strings
          specifying which data keys to be promoted to coordinate status.

        Currently the data is always stacked along the first (i.e. "index") dimension,
        but this may change in the future.
        '''
        candidates = self._scan_candidates()
        stacks = self.spice.collection.anchors("stack")        
        if len(stacks) == 1: ## Easy way out, we don't have stack info
            return candidates

        bnd = [ anchor for anchor,spice in stacks.items() ]

        def _append_stack(scan_stack, scan_list, prev_type):
            # Helper to create a stacked-scan and append it to the "official"
            # scan list
            stack_handle = f'{next(iter(scan_stack))[1]}_stack'
            stack_key = f'{stack_handle}_{prev_type}'
            scan_list.append((stack_key, stack_handle))
            self._stacks[stack_key] = {
                'key': stack_key,
                'stype': prev_type,
                'scans': [k[0] for k in scan_stack]}
            self._stacks[stack_key].update(prev_params)

        sitr = iter(candidates.items())
        prev_type = None
        prev_params = {}
        scan_list = []
        self._stacks = {}
        for anchor,stackbranch in stacks.items():
            sti = stackbranch['stack']
            scan_stack = []

            if anchor not in (None, ''):
                before, after = before_and_after(lambda x: x[0] < anchor, sitr)
                if prev_type in (None, ''):
                    scan_list += [b for b in before]
                else:
                    scan_stack = [b for b in before]
                sitr = iter(after)

            if len(scan_stack) > 0:
                _append_stack(scan_stack, scan_list, prev_type)
                scan_stack = []

            prev_type = sti.type
            prev_params = sti.options if sti.options is not None else {}

        scan_list += [a for a in sitr]

        return dict(scan_list)


    def keys(self):
        return self.all().keys()


    def handles(self):
        return self.all().values()


    def recipe(self, stype):
        '''
        Expected to return a function able to process raw data of type `stype`.
        '''
        raise RuntimeError('not implemented')


    def _scan(self, key):
        '''
        Returns a `DataProposal` object for the proposal of this
        repo designated by `handle` or by `key`.
        '''
        raise RuntimeError('not implemented')


    def scan(self, handle=None, key=None):
        if key is None:
            key = {h:k for k,h in self.all().items()}[handle]

        if hasattr(self, "_stacks") and key in self._stacks:
            si = self._stacks[key]
            return self.stack(**si)

        return self._scan(key)


    def stack(self, stype, scans, key=None, coords=None):
        '''
        '''
        return StackedDataScan(proposal=self, scans=scans,
                               coords=coords, stype=stype,
                               key=key)


    def __dir__(self):
        return super().__dir__() + [i for i in self.handles()]


    def __getattr__(self, handle):
        if handle not in self.all().values():
            raise AttributeError(f'No such scan: {handle}')
        return self.scan(handle=handle)


    def _repr_html_(self):
        candidates = [self.scan(key=k) for k in self.keys()]

        desc = lambda x: x.summary['description'] \
            if len(x.summary['description']) > 0 \
               else ' '.join([
                       f'{k}={v}' for k,v in
                       filter(lambda x: x[0] not in \
                              ('description', 'type', 'intg', 'steps'),
                              x.summary.items())
               ])

        k2h = self.all()
        return \
            '<table><tr> '+\
            '<th>scan</th> '+\
            '<th>handle</th> '+\
            '<th>type</th> '+\
            '<th>integration</th> '+\
            '<th>steps</th> '+\
            '<th>notes</th> '+\
            '</tr>\n'+\
            '\n'.join([
                f'<tr> '
                f'<td style="text-align:left">{s.key}</td> '
                f'<td style="text-align:left">{k2h[s.key]}</td> '
                f'<td>{s.type}</td> '
                f'<td>{s.summary.get("intg", "")}</td> '
                f'<td>{s.summary.get("steps", "")}</td> '
                f'<td style="text-align:left">{desc(s)}</td> </tr>' \
                for s in candidates
            ])+\
            '</table>'
