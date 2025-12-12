from nx5d.repo.base import DataProposalBase
from camagick.source.astor import Processor as Astor
import functools

class DataProposal(DataProposalBase):
    def __init__(self,
                 repo,
                 key,
                 url,
                 scan_class=None,
                 scan_k2h=None):
        '''
        Initializes a filesystem-based proposal walker.

        Args:
          repo: The `DataRepository` object that this proposal
            is part of. This is used because the repository object
            usually also has API elements for access to specific
            services (spice repo, caching etc), which we need to
            pass down.

          key: Identifying information for this proposal inside
            `repo`. Path (inside of `url`) of the group containing
            scans as subgroups.
        
          url: URL (format) of the proposal folder. Use the
            `{scan}` format key to denote how the scan key
            ties into the URL to produce scan URLs. The URL may or
            may not yet have the proposal key filled in. In any case,
            formatting the URL with the proposal key specified in `key`
            (as a replacement for `{proposal}`) will be attempted.

          scan_class: subclass to use for building scan objects
            (typically a subclass of `DataScanBase`, or compatible).

          scan_k2h: key to handle transformator, should match
            `call(key)` and return a python-compatible symbol
            name to use for subscans.
        '''
        super().__init__(repo, key)
        self._k2h = scan_k2h if scan_k2h is not None else lambda x: x
        self._ScanClass = scan_class
        self._astor = Astor(url.format(proposal=key), scans=f'/.keys')


    def all(self):
        self._k2hmap = { str(k):str(self._k2h(k))\
                         for k in self._astor.read()['scans'] }
        return self._k2hmap


    def _scan(self, key):
        return self._ScanClass(self, key)
