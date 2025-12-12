
import time
import schema, json, uuid, functools, logging
from nx5d.repo.filesystem import FilesystemWalker
from nx5d.repo.filesystem import DataRepository as FsDataRepository
from nx5d.repo.base import DataRepoBase
from nx5d.xrd.udkm import opcast

import glob as glb

import nx5d._version as myver

logger = logging.getLogger(__name__)

spice_schema = schema.Schema({
    # Version of the format
    'version': 'kmc3/1a',

    # Optional (obsolete?); a type string (needs to be locally unique)
    schema.Optional('type'): schema.Optional(str),

    # A string suitable to serve as a Python name for data of this type
    'handle': str,

    # UUID of this particular entry.
    'uuid': schema.Or(str, uuid.UUID),

    # Incrementing counter; the higher number wins for this particular
    # anchor.
    'revision': int,

    # Scan reference from which on this update is valid
    'anchor': schema.Or(str, int),

    # Data dictionary (if None, this erases the whole chain
    # for this anchor)
    'data': schema.Or(None, dict)
})

# Validators for the 'data' payloads of various spice types
spice_types = {
    'straight': schema.Schema({ 'param': float}),
    'conflicted': schema.Schema({ 'value': float})
}

class SpiceBranch:
    '''
    Easy way to access fields of a single spice branch/type,
    for a specific anchor, sorted by revision.

    As per the data model, there will always be the "current version"
    of a view, if there currently is no revision conflict. Properties
    of the current version can be queried with the properties:
      - `.keys()  .alues()  .iems()` -- dict-like access
      - `.meta()` -- access to spice-object metadata
      - `.data()  .xr()` -- access to spice-type data (dict or xarray like)
      - `.uuid()  .revision()  .anchor()` -- commonly required spice
        metadata headers

    Some dynamic properties:
      - `.conflicted()` -- tells whether the view is clean or has a revision
        conflict
      - ...? 
    '''
    def __init__(self, *slist):
        '''
        Args:
          slist: list of spice objects (for the same type)
        '''

        self._dlist = sorted(slist, key=lambda x: x['revision'], reverse=True)


    def latest(self):
        '''
        Returns a list of items of the latest revision.
        The list should only have one item if there are no conflicts.
        '''
        ri = iter(self._dlist)
        latest = next(ri)
        candidates = [latest]
        while True:
            try:
                another = next(ri)
                if another['revision'] == latest['revision']:
                    candidates.append(another)
                if another['revision'] < latest['revision']:
                    raise StopIteration()
            except StopIteration:
                return candidates


    def history(self):
        '''
        Returns all spice object entries.
        '''
        return self._dlist


    def conflicted(self):
        '''
        Returns a list of conflicted items in the latest revision,
        or an empty list if there is no conflict.
        '''
        i = iter(self.latest())
        first = next(i)
        candidates = []
        while True:
            try:
                candidates.append(next(i))
            except StopIteration:
                if candidates: # not empty? -> conflicted!
                    candidates.append(first)
                break
        return candidates


    def obj(self):
        '''
        Returns the underlying JSON object representation if there are no
        conflicts; raises `SpiceRevisionConflict` otherwise.
        '''
        i = iter(self.latest())
        first = next(i)
        try:
            second = next(i)
            raise SpiceRevisionConflict(first, second)
        except StopIteration:
            return first


    def __dir__(self):
        return self.obj()['data'].keys()


    def __getattr__(self, k):
        try:
            return self.obj()['data'][k]
        except KeyError:
            raise AttributeError(k)


    def __getitem__(self, k):
       return self.obj()['data'][k]


    def keys(self):
        return self.obj()['data'].keys()


    def values(self):
        return self.obj()['data'].values()


    def items(self):
        return self.obj()['data'].items()


    def meta(self, k=None):
        '''
        Returns meta-data for the spice entry (i.e. information
        on fields that are _not_ part of the data).

        This is only usable if the branch is unconflicted.
        '''
        obj = self.obj()
        d = {
            k:obj[k] for k in filter(lambda x: x != 'data', obj.keys())
        }

        if k is not None:
            return d[k]
        
        return d


    def uuid(self):
        ''' Returns the UUID of the latest revision, if the branch is unconflicted. '''
        return self.meta('uuid')

    
    def revision(self):
        ''' Returns the revision of the latest revision. Also usable for conflicted branches. '''
        return next(iter(self._dlist))['revision']


    def anchor(self):
        ''' Returns the anchor. Also usable for conflicted branches. '''
        return next(iter(self._dlist))['anchor']


    def data(self):
        '''
        Returns a dictionary with all data fields, if the branch is unconflicted.
        '''
        return {k:v for k,v in self.obj()['data'].items()}


    def xr(self):
        '''
        Returns an xarray dataset with all data fields, if the branch is unconflicted.
        '''
        import xarray
        return xarray.Dataset(self.data())


    def make_update(self, **updates):
        '''
        Returns an updated spice entry.

        Essentially, this just copies everything from the underlying
        dataset, updates the UUID and revision, and updates the data
        fields.
        '''
        obj = next(iter(self._dlist))        
        dcopy = obj['data'].copy()
        
        for k,v in updates.items():
            if k not in dcopy:
                raise RuntimeError(f'msg="Key not available" key={k}')
            
        dcopy.update(**updates)
        n = {
            'version':  'kmc3/1a',
            'handle':   obj['handle'],
            'uuid':     uuid.uuid4(),
            'revision': obj['revision']+1,
            'anchor':   obj['anchor'],
            'data': dcopy
        }
        
        return spice_schema.validate(n)

    
    def __repr__(self):
        obj = next(iter(self._dlist))
        return self.__class__.__name__ \
            + f"<{obj['handle']}:{obj['revision']}"\
            + f"{'#' if self.conflicted() else ''}>"\
            + "(" \
            + ', '.join([
                f'{k}={v}' for k, v in obj['data'].items()
            ]) \
            + ")"

    def _repr_html_(self):
        obj = next(iter(self._dlist))
        return '<table><tr><th>Handle</th><th>Data</th></tr>'+\
            '\n'.join([
                f'<tr><td>{k}</td><td>{v}</td></td>' \
                for k,v in obj['data'].items()
            ]) + \
            '</table>'


BranchView = SpiceBranch
    

class SpiceView:
    '''
    Views a number of branches (for one specific anchor).

    Typically, this object will have attributes (see `.__dir__()`)
    with all branch names (i.e. "spice types"), and each attribute
    will hold a `BranchView` instance as value. If there's
    a revision conflict, then the value will be a tuple of
    `BranchViews` instead.
    '''
    def __init__(self, view_point, **branches):
        self._view = view_point
        self._data = branches
        Branch = lambda x: x if not isinstance(x, tuple) else x[0]

    @property
    def view_point(self):
        return

    @property
    def data(self):
        return self._data

    def handles(self):
        return self._data.keys()

    def __dir__(self):
        return self.handles()

    def __getattr__(self, handle):
        try:
            return self._data[handle]
        except KeyError:
            raise AttributeError(handle)


    def __repr__(self):
        from pprint import pformat
        return self.__class__.__name__+'('+pformat(self._data)+')'


    def _as_pandas_dframe(self):
        # Returns a Pandas DataFrame representation of this view
        view = self.data

        _view_item_dict = lambda v: { 
            'revision': v['revision'],
            'uuid':     v['uuid'][:6],
            'anchor':   v['anchor'],
            'data':     ' '.join([f'{f}={n}' for f,n in v['data'].items()])
        }

        import pandas
        out = pandas.DataFrame()
        for k,v in view.items():
            row_vals = {
                'viewpoint': self._view,
                'handle': k,
                'clean': not v.conflicted()
            }

            for vi in v.latest():
                row_vals.update(_view_item_dict(vi))
                out = pandas.concat([
                    out, pandas.DataFrame({
                        k: {row_vals['viewpoint']: v } \
                        for k, v in row_vals.items()
                    })
                ], ignore_index=True)

        if len(out)>0:
            return out.set_index('viewpoint')
        else:
            return out


    def _repr_html_(self):
        return self._as_pandas_dframe().fillna('')._repr_html_()


class SpiceRevisionConflict(RuntimeError):
    def __init__(self, candidate, other):
        self.canidate = candidate
        self.other = other
        super().__init__(f'msg="Revision conflict" '
                         f'handle={candidate["handle"]} '
                         f'candidate={candidate["uuid"]} '
                         f'conflicting={other["uuid"]}')

class SpiceUnavailable(RuntimeError):
    def __init__(self, msg=None, **params):
        self._params = params
        if msg is None:
            msg = \
                f'msg="Unavailable for '+\
                ' '.join([f'{k}="{v}"' for k,v in params.items()])
        super().__init__(msg)


def _rev_shortid(x):
    # returns a short-uuid variant for spice branch 'x'
    return x['uuid'][:6]


def _rev_conflict_list(rlist):
    # `rlist` is a spice branch (revision list)
    # returns a list of short-UUIDs that conflict with the
    # first (i.e. most recent) one
    return [
        _rev_shortid(d) for d in \
        filter(lambda x: x.meta('revision') == rlist[0].meta('revision'), rlist)
    ]
        

class SpiceCollection:
    '''
    In-memory representation all the available spice for a proposal.

    From here, views of branches can be created (i.e. collections of
    spice for a specific anchor, containing specific types) -- these are
    anchored at or above a specific frame.
    '''
    def __init__(self):
        # Data model here is:
        #  { type: { anchor: [revision] }  }
        self._data = { }


    def add(self, sdata):
        '''
        Adds a new update entry to the spice chain.
        '''
        d = spice_schema.validate(sdata)
        t_part = self._data.setdefault(d['handle'], {})
        a_part = t_part.setdefault(d['anchor'], [])
        a_part.append(d)


    def find(self, startswith=False, insensitive=False, **meta_args):
        '''
        Returns a list with BranchView objects that match criteria.

        Args:
          startswith: if set to `True`, when checking for matches
            of string values, only check if the spice value starts
            with the suppied search value. Otherwise check for a full
            match
          insensitive: if set to `True`, the match for strings will be
            performed in a case-insensitive way.
          **meta_args: keys and search values for meta fields to search
            in.

        Returns: a list with matching branch views, or an empty list
        if no result matches.
        '''
        ret = []
        for st,anclist in self._data.items():
            for anc,revlist in anclist.items():
                for rev in revlist:
                    for k,v in meta_args.items():
                        if k not in rev:
                            continue
                        r = rev[k]
                        v2 = v.lower() if isinstance(v, str) and insensitive else v
                        r2 = r.lower() if isinstance(r, str) and insensitive else r
                        if startswith:
                            if not r2.startswith(v2):
                                continue
                        else:
                            if not r2 == v2:
                                continue
                        ret.append(BranchView(rev))
        return ret


    def startswith(self, insensitive=True, **meta_args):
        '''
        Convenient wrapper for `.find()` with different defaults.
        '''
        return self.find(insensitive=insensitive, startswith=True, **meta_args)


    def handles(self, *handles):
        '''
        Returns the spice repo by spice handles as a dictionary
        { 'handle': { 'anchor': [revisions...] } }
        '''
        return {
            k:v for k,v in \
            (self._data.items() \
             if len(handles)==0 \
             else filter(lambda x: x[0] in handles, self._data.items()))
        }


    def anchors(self, *handles):
        '''
        Returns the spice repo by anchor points, as a dictionary
        like:
           {
              'anchor': { 'handle': [revisions, ... ]  },
              ...
           }
        '''
        ret = {}
        for stype,v in filter(lambda x: (x[0] in handles or len(handles)==0), self._data.items()):
            for sanchor,w in v.items():
                a = ret.setdefault(sanchor, {})
                a.setdefault(stype, SpiceBranch(*w))
            #    sorted_revisions = sorted(w, key=lambda x: x['revision'],
            #                              reverse=True)
            #    t = a.setdefault(stype, sorted_revisions)
        return { k:v for k,v in sorted(ret.items()) }


    def view(self, scan, *handles, ignore_conflict=False):
        '''
        Returns a SpiceView for the specified frame and types.

        If no types are requested, all available types are returned.
        There's always the latest revision that's returned for every
        frame/type combination. Conflicts in the latest revision
        are either reported (raising `SpiceRevisionConflict`) or
        ignored.

        Args:
            scan: the scan reference of the data point we want to
              collect spice for (i.e. "virtual anchor"). Set to
              `None` to view the seed.
        
            *handles: list of spice handles (strings)
            ignore_conflicts: if set to `False`, revision conflicts
              in the latest revision are ignored and all available
              revisions are returned.

        Returns: a `SpiceView` object.
        '''

        # BTW, the difference betwee a "scan" and an "anchor"
        # is this:
        #
        #  - a "scan" is (the reference of) a data collection run;
        #    it usually has a specific spice set associated with it,
        #    but mostly _indirectly_ through spice types published
        #    earlier
        #
        #  - an "anchor" is a scan which is boundary for the validity
        #    for a speific version of spice, which means that all previous
        #    scans don't have the (same version of) spice data for this
        #    type.

        if len(handles) == 0:
            search_handles = [k for k in  self._data.keys()]
        else:
            search_handles = handles

        branches = {}

        def revisions_for_anchor(data, viewpt):
            # Returns an (anchor-pt, revisions-list) for a specific
            # view point, or None if there's no revision in data.
            # `data` is for a specific type only.
            # If `viewpt` is `None`, return for the default anchor
            # (i.e. the seed).
            if (data is None) or  (len(data) == 0):
                raise RuntimeError(f'msg="No entries" stype={st}')

            # Sort by "anchor" (key of 'for_type') and find the one
            # that's immediately at or above requested frame.
            if viewpt is not None:
                tmp = sorted(data.items(), reverse=True)
                for a, rev_list in tmp:
                    if (a <= viewpt) and (len(rev_list) > 0):
                        return a, sorted(rev_list,
                                         key=lambda x: x['revision'],
                                         reverse=True)
            else:
                tmp = sorted(data.items(), reverse=False)
                if len(tmp) > 0:
                    rev_list = next(iter(tmp))[1]
                    return None, sorted(rev_list,
                                        key=lambda x: x['revision'],
                                        reverse=True)
                
            if len(data) != 0:
                msg = f'msg="Corrupt spice repo" detail="Unanchored entry"'
                logger.error(msg)
            raise SpiceUnavailable(msg=msg, anchor=viewpt)


        for st in search_handles:
            try:
                anc_pt, revisions = revisions_for_anchor(self._data.get(st, None), scan)
                tmp = branches[st] = SpiceBranch(*revisions)
                if not ignore_conflict:
                    chk = tmp.obj() ## will raise if there's a conflict
            except SpiceUnavailable as e:
                # If we have an explicit list with types, raise an error
                # if one is missing. Otherwise ignore.
                if handles is not None:
                    raise SpiceUnavailable(msg=str(e)+f' stype={st}', anchor=scan)

        return SpiceView(view_point=scan, **branches)


    def _list(self, *stypes):
        '''
        Creates a Pandas list with all data
        '''
        shortid = _rev_shortid
        conflict_list = _rev_conflict_list
        conflicted = lambda rlist: False if (len(rlist) <= 1) \
            else (rlist[0]['revision'] == rlist[1]['revision'])

        import pandas
        out = pandas.DataFrame()
        
        for anchor,branchlist in self.anchors(*stypes).items():
            cols = { 'anchor': {anchor: anchor}, }
            handles = {
                handle: {
                    anchor: shortid(branch.obj()) if not branch.conflicted() \
                    else ','.join([shortid(b) for b in branch.history()])
                } \
                for handle,branch in branchlist.items()
            }
            cols.update(handles)
            out = pandas.concat([out, pandas.DataFrame(cols)], ignore_index=True)

        if len(out)>0:
            return out.set_index('anchor').fillna('')
        else:
            return None

    
    def __repr__(self):
        return f'{self.__class__.__name__}[{",".join(self.handles().keys())}]'


    def _repr_html_(self):
        return self._list()._repr_html_()            


class SpiceProposal:
    '''
    Base class for access and storage-related operations for `SpiceCollection`

    Implements main operations like saving, seeding, updating etc.
    This is usually not used directly, it's subclassed. The subclass
    needs to implement at least the `.save()` and `.load_collection()`
    members.

    The most spice operations (seed, anchor, update) can be implemented
    generically as they're only logics around the actual collection object.
    '''
    def __init__(self, collection=None, name=None):
        '''
        Initializes the proposal backend.

        Args:
          collection: if specified, the spice data collection.
            If this is `None` (the default), then `.init_collection()`
            is called.
          name: Human-readable proposal name, used for output. Typically,
            this should be the same as the proposal key that was used to
            load the proposal.
        '''
        self.name = name
        self._collection = collection if collection is not None \
            else self.init_collection()


    def init_collection(self):
        '''
        Returns an initialized/popuplated spice collection from disk.

        The default implementation just returns an empty (but otherwise
        functional) `SpiceCollection`. You'd have to subclass and implement
        this for a spice proposal based on persistent storage.
        '''
        return SpiceCollection()


    def save(self, obj):
        '''
        Unconditionally saves a spice object.

        Saving is also performed non-idempotently, i.e. even if there's
        already a similar object existing. This can lead to conflicts or
        other kinds of logical spice system corruptions -- use only
        if you know what you're doing. Otherwise, use functions like
        `.seed()` or `.update()` instead, with `idem=True`.

        Args:
          obj: the full spice object (i.e. on-disk object, not just
            the data keys)

        Returns: a copy of the spice object, as written to disk.
        '''
        data = spice_schema.validate(obj)
        data.update({'uuid': str(data['uuid'])})
        self.collection.add(data)
        return data


    @property
    def collection(self):
        return self._collection


    def ls(self, *stypes):
        '''
        Lists the contents as an type/anchor point overview.
        '''
        return self.collection._list(*stypes)


    def view(self, *a, **kw):
        '''
        Convenience wrapper for the underlying `SpiceCollection.view()` method.
        '''
        return self.collection.view(*a, **kw)


    def seed(self, handle, payload=None, anchor=None, revision=1,
             idem=True, **extra_payload):
        '''
        Seeds (i.e. "creates") a new spice type in this proposal.
        
        This uses `.save()` under the hood, but wraps around some code
        to create  UUIDs, revisions and anchor from scratch, and check
        for already existing spice types.

        Args:
          handle: the handle of the spice
          payload: a dictionary with spice fields and values
          anchor: if specified, this will be used as the anchor seed.
            Typically this is `null` (JSON), or `None` (Python),
            which means that the backend will do its best to use
            a useful default that always sorts at the top of the
            list.
          revision: revision for the seed -- the default of `1` is
            a good choice.
          idem: if set to `True` (the default), the operation is
            idempotent. This means that when called repeatedly with
            the same handle, only the first call will have an effect.
            All subsequent other calls will have no effect on the
            repository and will just return the data already in store.
            But repated calls will _not_ fail. If set to `False`,
            attempts to re-seed with the same handle will raise a
            `RuntimeError`.
          **extra_payload: any other named arguments will be merged
            into `payload`. This is for convenience, so that
            both calls of the kind `.seed(payload={"param": ...})` and
            of the kind `.seed(param=...)`. Note that the extra
            payload parameters will overwrite original payload
            parameters, if specified repeatedly.

        Returns: a copy of the spice object that was saved, as
        returned by `.save()`.
        '''

        if payload is None:
            payload = {}
        payload.update(extra_payload)

        if handle in self._collection.handles():
            v = self._collection.view(None, handle)
            item = getattr(v, handle)
            if idem:
                #print('idem seed:', item.meta('uuid'))
                return item.obj()
            else:
                raise ValueError(f'{handle}: already exists as uuid={item.meta("uuid")}')

        obj = {
            'version': 'kmc3/1a',
            'type': handle,
            'handle': handle,
            'uuid': uuid.uuid4(),
            'revision': revision if revision is not None else 1,
            'anchor': anchor if anchor is not None else '',
            'data': payload
        }
        
        return self.save(obj)

    
    def anchor(self, anchor, handle, idem=True):
        '''
        Creates an anchor point for a spice type

        Args:
          anchor: anchor point, i.e. scan to which to anchor the
            spice type.
          handle: spice handle for which to create the anchor point.
            Spice type must already have been seeded. (See `.seed()`).
          idem: if set to `True` (the default), 

        Returns: the result of `.save()` which is a copy of the spice
        data that was saved.
        '''
        v = self._collection.view(anchor, handle)
        obj = getattr(v, handle)
        if (obj.meta('anchor') == anchor):
            if idem:
                return obj.obj()
            else:
                raise RuntimeError(f'{handle}: already anchored at {anchor}, '
                                   f'use update instead')
        
        nobj = {
            'version': 'kmc3/1a',
            'type': handle,
            'handle': handle,
            'uuid': uuid.uuid4(),
            'revision': obj.meta('revision')+1,
            'anchor': anchor,
            'data': obj.data()
        }

        return self.save(nobj)


    def update(self, *addr, payload=None, idem=True,
               **extra_payload):
        '''
        Updates an existing spice type with respect to a viewpoint.

        Args:
          addr: which spice to update. This can be either specified as
            a (viewpoint, handle) combination (in which case `addr` must
            be two arguments), or as a single UUID string (in which case
            the number of `addr` arguments is 1.)
          payload: `dict` with keys with values to update. Keys must
            match those in the seeded version of the spice type.
          idem: if set to `True` (default) the values will be checked
            against the last available revision of the spice type
            for the anchor. If the values match, there will be no
            update and the already available version will be returned
            instead.
          **extra_payload: keywords specified here will be used to
            update the payload dictionary before applying.

        Returns: the full resulting spice object after update.
        '''
        if payload is None:
            payload = {}
        payload.update(extra_payload)

        if len(addr)==2: ## (viewpoint, handle)
            found = getattr(self.collection.view(addr[0], addr[1]), addr[1])
            if not isinstance(found, BranchView):
                raise RuntimeError(f'bad branch for "{addr[1]}@{addr[0]}": {found}')

        elif len(addr)==1: ## UUID
            if isinstance(addr[0], uuid.UUID):
                s = self._collection.find(startswith=False, insensitive=True, uuid=str(addr[0]))
            else:
                s = self.collection.find(startswith=True, insensitive=True, uuid=str(addr[0]))
                
            if len(s) != 1:
                raise RuntimeError(f'bad branch for "{addr[0]}": {s}')
    
            found = next(iter(s))


        new = found.make_update(**payload)
        for k,v in found.data().items():
            if ((new['data'][k] != v) or (not idem)):
                return self.save(new)

        return found.obj()


    def __repr__(self):
        n = self.__class__.__name__
        return n


    def _repr_html_(self):
        tmp = self.ls()
        if tmp is not None:
            return tmp._repr_html_()
        else:
            return self.__repr__()+' (empty)'


class FsSpiceProposal(SpiceProposal):
    '''
    SpiceProposal implementation for a filesystem-like backend

    The spice objects are stored as files (or file-like) entries,
    one object per file. The target of the file is a URL format,
    implementing the 'file' mechanism, and possibly others like
    's3' in the future.
    '''
    def __init__(self, folder, glob=None, on_load_fail='warn', name=None):
        '''
        Initialization of the proposal access.

        (FIXME: specifying collection, AND key, AND url, feels like
        an awful lot of superfluous information...)

        Args:
          folder: Spice (proposal) folder to work on
          glob: Globbing pattern for the spice files within
            the folder. By default (i.e. when set to `None`),
            a string representation of UUIDs.
          on_load_fail: One of "warn", "ignore" or "raise" -- what
            to do when encountering a spice file that can't be
            loaded.
          name: Human-readablye name for nicer errors. We recommend
            you put the repo key here.
        '''

        self._folder = folder
        if glob is None:
            self._glob = \
                '[a-fA-F0-9]'*8 + '-' + \
                '[a-fA-F0-9]'*4 + '-' + \
                '[a-fA-F0-9]'*4 + '-' + \
                '[a-fA-F0-9]'*4 + '-' + \
                '[a-fA-F0-9]'*12
        else:
            self._glob = '*'

        self._on_load_fail = on_load_fail

        super().__init__(name=name)

        
    def init_collection(self):
        '''
        (Re)loads the spice collection from disk into memory
        '''
        col = SpiceCollection()
        for p in glb.glob(f'{self._folder}/{self._glob}'):
            with open(p, 'r') as f:
                try:
                    col.add(json.load(f))
                except Exception as e:
                    if self._on_load_fail in ('raise',):
                        raise e
                    elif self._on_load_fail in ('warn',):
                        logger.warning(str(e))

        return col


    def save(self, obj):
        '''
        Overriding `.save()` to actually store data on disk.
        '''
        import os        
        fpath = os.path.join(self._folder, str(obj['uuid']))
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        with open(fpath, 'x') as f:
            r = super().save(obj)
            json.dump(r, f)
            return r

    
    def __repr__(self):
        return f'{self.__class__.__name__}[{self._folder}]'


class FsSpiceRepository(FsDataRepository):
    '''
    On-disk access to spice

    The idea is that for each proposal we have a proposal-dependent
    base URL (possibly) containing raw data, and containing the spice
    collection for the proposal. This class manages access to the
    repository as a whole, and delegates proposal-specific work
    to the appropriate `SpiceProposal` implementation.
    '''

    def __init__(self, url, **repo_args):
        '''
        Args:
          url: URL of the spice repository (which may be the same as
            the data repository, if spice is stored on-disk alongside
            data). This should resolve to the per-proposal spice folders,
            not the data folders (e.g. "/mnt/repo/{proposal}/spice/" if
            your spice is in a "./spice/" subfolder of the corresponding
            proposal).
          **repo_args: keyword arguments to pass on to the
            `FsDataProposal` subclass. We recommend at least
            `glob` and `proposal_k2h` to be set.
        '''
        self._u = url
        super().__init__(url, **repo_args)


    def _proposal(self, key):
        '''
        Returns a `SpiceProposal` for the specified proposal key.
        '''
        scm, path = self._split_url(self._u.format(proposal=key))
        return {
            'file': FsSpiceProposal(path, name=key),
        }[scm]


    def _split_url(self, url):
        # return (scheme, path) from url
        parts = url.split('://')
        if len(parts) == 1:
            return ('file', parts[0])
        elif len(parts) == 2:
            return parts
        raise RuntimeError(f'don\'t understand {url}: {parts}')

    
class MemorySpiceRepository(DataRepoBase):
    '''
    Purely in-memory spice repository

    Inside Nx5d this is mostly used for unit testing, but it might have
    some use outside (e.g. for quick spice-based setups inside Jupyter
    Notebooks without access to permanent storage).

    Spice proposals are saved in an internal dictionary.

    As an option, this repository can be based off a template of another
    repository. This is such, this class is a good way of goofing around
    with spice of an existing repository without creating any damage
    (because nothing is saved).
    '''
    def __init__(self, template=None):
        '''
        Initializes the internal repo, possibly from a starting template

        Args:
          template: if not `None`, it is expected to be an instance of
            another (type of) spice repository which's contents will be
            used as a starting point. Loading of the other repo's data
            happens lazily, when `.proposal()` is called.
        '''
        super().__init__('')
        self._storage = {} ## key -> collection map
        self._template = template
        self._template_proposals = {} if template is None \
            else { k:k for k in template.all() }


    def all(self):
        keys = { k:k for k in self._storage.keys() }
        if self._template is not None:
            keys.update({k:k for k in self._template.all() })
        return keys


    def new(self, key):
        if (key in self._storage):
            return
        
        if (self._template is not None) and (key not in self._template.all()):
            return

        self._storage[key] = SpiceProposal(name=key)


    def _proposal(self, key):
        if (key not in self._storage) and (self._template is not None):
            self._storage[key] = self._template.proposal(handle=key)
        return SpiceProposal(self._storage[key].collection, name=key)
