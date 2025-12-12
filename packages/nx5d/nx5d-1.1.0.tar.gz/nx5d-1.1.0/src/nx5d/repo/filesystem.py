from nx5d.repo.base import DataRepoBase, DataProposalBase
import parse, os, logging

import glob as glb

from functools import partial

logger = logging.getLogger(__name__)

# Implements filesystem-based proposal and data reading.

class FilesystemWalker:
    '''
    Class to conveniently iterate through filesystem folders.

    The asumption is that data is stored in a filesytem directory
    structure.

    Args:
      fmt: starting point, containing a format key as the
        place where subentries should be expected.
    '''
    def __init__(self, fmt, glob=None):

        if glob is None:
            glob = '*'

        self._format = fmt
        self._glob = fmt.format(key=glob)


    def _path2key(self, p):
        '''
        Returns the key part from a path.
        '''
        r = parse.parse(self._format, p)
        if (r.named is None) or ('key' not in r.named):
            raise RuntimeError(f'msg="Cannot parse key from path" '
                               f'path="{p}" '
                               f'format="{self._format}"')
        return r.named['key']


    def _key2path(self, key):
        '''
        Given a sub-group key, returns the corresponding path.
        '''
        return self._format.format(key)


    def _list_entries(self):
        # Lists all entries below `base`.
        # Override this if the backend is not an actual filesystem.
        return glb.glob(os.path.join(self._glob))


    def keys(self):
        return [
            self._path2key(i) for i in self._list_entries()
        ]


    def entry(self, name):
        path = self._key2path(name)
        return self._subwalker(os.path.join(self._entry, path))

    
class GenericDataWalker:
    # Base class for filesystem-globbing listing for various resources.
    #
    # This is used as a base class for various filesystem-walking
    # containers, like DataRepository and DataProposal (here),
    # but also `nx5d.spice.FsSpiceRepository`.
    #
    # This base implements mechanisms for URL loading and listing
    # (file/s3/https/tield come to mind), and transforming of path
    # keys <-> handles, as well as delegating __getattr__() calls
    # to sub-classes.
    #
    # Note that the subclasses `DataRepository`, respectively
    # `DataProposal` don't necessarily need to be used together. In
    # fact, most cases will likely have a FS-based `DataRepository`,
    # while having something else entirely (e.g. an ArrayAccess-based
    # `DataProposal`).
    def __init__(self,
                 url,
                 glob=None,
                 k2h=None,
                 h2k=None,
                 subnode_class=None
                 ):
        '''
        Initializes access to a filesytem-based repository reader.

        The general idea is that the repository location is
        a filesystem or filesystem-like entity able to deliver
        all proposals by a globbing pattern, and/or to retrieve
        a _specific_ proposal by filling in a formatting key.

        Args:
        
          url: string format for a full, typical item key path
            (e.g. "file:///mnt/data/proposals/{key}/")
        
          glob: globbing pattern for the data item, if different
            from `*`.

          subnode_class: class to initialize the return value
            of `._subnode()` with. The sole argument of the
            proposal class is the key, e.g. "proposal url"
            or "scan url".

          k2h: if not `None`, expected to be a callable `call(key)`
            which will transform an on-disk proposal key into a
            Python compatible handle.

          h2k: if not `None`, expected to be a callable `call(handle)`
            that will transform a Python handle into an on-disk
            proposal key.
        '''

        self._k2h = k2h if k2h is not None else lambda x: x
        self._h2k = h2k

        # for later use when creating subnodes
        self._base_url_format = url

        import urllib
        purl = urllib.parse.urlparse(url)
        
        self._walker = self._init_walker(purl.scheme,
                                         fmt=purl.path,
                                         glob=glob)
        self._SubnodeCls = subnode_class


    def _init_walker(self, scheme, **kw):
        return {
            'file': FilesystemWalker
        }[scheme](**kw)

    def _key2handle(self, k):
        if self._k2h is None:
            raise RuntimeError('no key->handle transform available')
        return self._k2h(k)

    def _handle2key(self, h):
        if self._h2k is None:
            return self._hkmap[h]
        return self._h2k(h)

    def _subkeys(self):
        self._khmap = {
            k:self._key2handle(k) for k in self._walker.keys()            
        }
        self._hkmap = {
            h:k for k,h in self._khmap.items()
        }
        return self._khmap.keys()

    
    def key_handle_map(self):
        self._subkeys() # regenerate map
        return self._khmap


    def _subnode(self, key):
        sub_url = self._base_url_format.format(key=key)
        #print("Walker Subnode Class:", self._SubnodeCls)
        return self._SubnodeCls(sub_url)


class DataRepository(GenericDataWalker, DataRepoBase):
    def __init__(self,
                 url,
                 glob=None,
                 proposal_k2h=None,
                 proposal_class=None,
                 proposal_kwargs=None,
                 **repo_kwargs):
        '''
        Initializes an on-disk proposal manager.

        Args:
          url: Path format for finding the proposals. Must contain
            `{proposal}` as a formatting key.
          glob: globbing pattern for the proposal keys,
            defaults to `*` if not specified.
          proposal_k2h: key-to-handle translation, defaults
            to a `lambda x: x`. Should otherwise be a callable,
            which, wen called with the proposal key as a parameter,
            returns a uniqe handle.
          proposal_class: class to instantiate on every new .proposal()
            request. If set to "auto" or "same", this
            specific repository implementation will just assume that
            the proposal subclass is a filesystem walker based
            class. You can pass a different kind of class, but it
            must have the same initialization parameters as
            the `FsDataProposal` class. Alternatively, ignore
            this or set to `None` (the default), and overwrite
            the `._proposal()` member function.
          proposal_kwargs: additional keyword arguments to pass on to
            the initialization of the proposal class.
          **repo_kwargs: additional keyword arguments will be
            passed to the `DataRepoBase` subclass.
        '''
        DataRepoBase.__init__(self, url, **repo_kwargs)

        import urllib
        purl = urllib.parse.urlparse(url)
        self._proposal_minimized = self._minimize_path(purl.path)

        # This is the smaller proposal-only URL. Since this is a
        # filesystem proposal lister, we ignore everything that isn't
        # host or path (intra-document stuff is not handled by this
        # DataProposal lister)
        scheme = purl.scheme if (purl.scheme is not None) and len(purl.scheme)>0 \
            else 'file'
        self._proposal_min_url = \
            f'{scheme}://'\
            f'{purl.netloc}/'\
            f'{self._proposal_minimized}'
        
        # This is what we'll pass on to the filesystem walker,
        # repo key here is "...{key}..."

        if self._proposal_minimized != purl.path:
            logger.info(f'msg="Minimized proposal URL" '
                        f'path={self._proposal_min_url}')
        
        self._walker_base_format = self._proposal_min_url.format(
            proposal="{key}"
        )
        
        GenericDataWalker.__init__(
            self,
            self._walker_base_format,
            glob=glob,
            k2h=proposal_k2h,
            h2k=None, # Reverse lookup handle->key done by superclass
            subnode_class=None, # Disable sub-walking.
                                # Need to overwrite ._proposal()!
        )

        self._ProposalSubclass = proposal_class
        self._proposal_kwargs = proposal_kwargs \
            if proposal_kwargs is not None else {}


    def _minimize_path(self, original_path, **keywords):
        # Calculates the minized {proposal}-only path,
        # by substituing increasingly larger path elements,
        # until at {proposal} gets substituted.
        from os import path
        head = original_path
        while len(head) > 0:
            try:
                head.format(proposal='jinkies!')
                return head
            except KeyError: pass
            head, tail = path.split(head)
        raise RuntimeError(f'unusable proposal path: {original_path}')
        

    @property
    def proposal_url(self):
        return self._proposal_min_url

    def all(self):
        return self.key_handle_map()

    def keys(self):
        return self.key_handle_map().keys()

    def handles(self):
        return self.key_handle_map().values()

    def _proposal(self, key):
        if self._ProposalSubclass == 'auto':
            self._ProposalSubclass = DataProposal

        if self._ProposalSubclass is None:
            raise RuntimeError(f'No proposal subclass available')
        from collections import defaultdict
        dd = defaultdict(lambda x: x)
        subpath = self._repo_url.format(
            proposal=key, scan='{scan}'
        )
        return self._ProposalSubclass(repo=self, key=key, url=subpath,
                                      **self._proposal_kwargs)


class DataProposal(GenericDataWalker, DataProposalBase):
    def __init__(self,
                 repo,
                 key,
                 url,
                 glob=None,
                 scheme=None,
                 scan_class=None,
                 scan_k2h=None):
        '''
        Initializes a filesystem-based proposal walker.

        Args:

          repo: Repository object (parent)

          key: Identifying information for this proposal
        
          url: URL (format) of the proposal folder. Use the
            `{scan}` format key to denote how the scan key
            ties into the URL to produce scan URLs. The URL
            may or may not have the specific proposal key
            already baked into the URL. In any case, replacing
            the format key `{proposal}` for the specified `key`
            parameter will be attempted.
        
          glob: globbing/search pattern for the scans, if
            different from "*".

          scheme: this will generally be obtained from the URL,
            or will default to "file". Specify something else
            ("s3", "https", "tiled"...?) manually if you need.

          scan_class: subclass to use for building scan objects
            (typically a subclass of `DataScanBase`, or compatible).

          scan_k2h: key to handle transformator, should match
            `call(key)` and return a python-compatible symbol
            name to use for subscans.
        '''
        #print(f"New filesystem proposal: key={key} url={url}")
        DataProposalBase.__init__(self, repo, key)

        # This is the URL format for Run sub-nodes; need to fill in the
        # {proposal} key, but keep open all other keys (in particular
        # {scan} or {iscan}).
        from collections import defaultdict
        class _dd(defaultdict):
            def __missing__(self, key):
                return f'{{{key}}}'
        self._scan_url = url.format_map(_dd(proposal=key))

        walker_url_base = url.format(proposal=key, scan="{key}")

        self._ScanClass = scan_class
        GenericDataWalker.__init__(self,
                                   walker_url_base,
                                   glob=glob,
                                   k2h=scan_k2h)


    @property
    def scan_url(self):
        '''
        Returns a URL pattern that contains `{scan}` or where the scan
        info should go.
        '''
        return self._scan_url


    def all(self):
        return self.key_handle_map()

    def keys(self):
        return self.all().keys()

    def handles(self):
        return self.all().values()

    def _scan(self, key):
        return self._ScanClass(self, key)

