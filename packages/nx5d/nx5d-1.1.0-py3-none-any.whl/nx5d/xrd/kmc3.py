#!/usr/bin/python3

#
#        nx5d - The NX5 Duct Tape
#        Copyright (C) 2022-2023 Florin Boariu
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        (at your option) any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from nx5d.xrd.base import DatasetFactory as DsFactoryBase

def default_seeds(flavor='eiger'):
    # Returns the default seeds for KMC3.
    # 'flavor' is either 'eiger' or 'pilatus', depending
    # on which detector is currently active for the experiment.

    return {
        # Default recipes, taken from the local kmc3recipes.
        'recipes': {
            'sRSM':    "py://kmc3recipes.cooking:sRSM",
            'TRSM':    "py://kmc3recipes.cooking:TRSM",
            'rocking': "py://kmc3recipes.cooking:rocking",
            'dRSS':    "py://kmc3recipes.cooking:dRSS",
        },
        
        # Experimental geometry definition; different for 'eiger' vs 'pilatus'
        # with regard to detector pixel geometry.
        'exp_info': {
            "goniometerAxes":   { 'theta': 'x+',  'chi': 'y+', 'phi': 'z+' },
            "detectorAxes":     { 'tth': 'x+', },
            "detectorTARAlign": (0.0, 0.0, 0.0),
            "imageAxes":        ('x-', 'z-'),
            "imageSize":        (512, 1028)    if flavor=='eiger' else (195, 487),
            "imageCenter":      (253, 507)     if flavor=='eiger' else (95, 318),
            "imageChannelSize": (0.075, 0.075) if flavor=='eiger' else (0.172, 0.172),
            "imageDistance":    '@PilatusYOffset',
            "sampleFaceUp":     'z+',
            "beamDirection":    (0, 1, 0),
            "sampleNormal":     (0, 0, 1),
            "beamEnergy":       '@monoE',
        },

        # Will manipulate angle offsets. Names must match those of
        # exp_info, and those of the data.
        'offsets': {
            'phi':   0.0,
            'chi':   0.0,
            'theta': 0.0,
            'tth':   0.0,
        },

        # Extra arguments to pass to QMappers.qmap()
        'qmap_kws': {
        },
    }

instrument_list = {
    'images':  '{scan}/instrument/images/data',
    'pilatus': '{scan}/instrument/pilatus/data',    
    'theta':   '{scan}/instrument/positioners/Theta',
    'chi':     '{scan}/instrument/positioners/Chi',
    'phi':     '{scan}/instrument/positioners/Phi',
    'tth':     '{scan}/instrument/positioners/TwoTheta',
    'temp':    '{scan}/measurement/SampleTemp',
    'delay':   '{scan}/instrument/positioners/LaserDelay',
    'energy':  '{scan}/instrument/positioners/DSCEnergy',
    'current': '{scan}/measurement/RingCurrent'
}


class DatasetFactory(DsFactoryBase):
    def __init__(self, empty=False, **instr):
        if empty == False:
            i = instrument_list.copy()
        i.update(instr)
        super().__init__(**i)


from nx5d.repo.filesystem import FilesystemWalker
from nx5d.repo.filesystem import DataRepository as FsDataRepoBase
from nx5d.repo.astor import DataProposal as AstorDataPropBase
from nx5d.repo.base import DataScanBase

class DsFactoryScan(DataScanBase):
    '''
    Scan class that relies on `DatasetFactory`-like loader to retrieve data
    '''
    def __init__(self, proposal, key, loader, base):
        #print('Scan URL:', base, key)
        super().__init__(proposal, key)
        self._loader = loader
        self._base_url = base
        self._scan_key = key


    def _get_raw(self):
        import h5py
        with h5py.File(self._base_url, 'r') as h5:
            return self._loader(h5, scan=self._scan_key).compute()


    def _get_summary(self):
        import h5py
        with h5py.File(self._base_url, 'r') as h5:
            tmp = h5[f'{self._scan_key}/instrument/specfile/scan_header'][0]
            scan_info = [
                k for k in filter(lambda x: len(x)>0,
                                  tmp.decode('utf-8').split(' '))
            ]

        from nx5d.xrd.udkm import opcast

        # type: (condition_proc, summary_proc)
        type_map = {
            'sRSM': (
                lambda x: (x[2] == 'a2scan') and (x[3] == 'th') and (x[6]=='tth'),
                lambda x: {
                    'intg': opcast(x[10]),
                    'th': [opcast(i) for i in x[4:6]],
                    'tth': [opcast(i) for i in x[7:9]],
                    'steps': opcast(x[9])
                }),
            
            'snapshot': (
                lambda x: (x[2] == 'acquire'),
                lambda x: {
                    'intg': opcast(x[4])
                }),

            'rocking': (
                lambda x: (x[2] == 'ascan') and (x[3] in ('th',)),
                lambda x: {
                    'intg': opcast(x[7]),
                    'steps': opcast(x[6]),
                    'range': [opcast(i) for i in x[4:6]]
                }),

            # adjustment
            'alignment': (
                lambda x: (x[2] == 'ascan') and (x[3] not in ('th',)),
                lambda x: {
                    'intg': opcast(x[7]),
                    'steps': opcast(x[6]),
                    x[3]: [opcast(i) for i in x[4:6]]
                }),

            'timescan': (
                lambda x: (x[2] == 'timescan'),
                lambda x: {}
            )
        }

        def _find_type(x):
            for stype, (chk, xtra) in type_map.items():
                if chk(x):
                    return stype, xtra(x)
            raise _unknown_scan_type()

        stype, xtra = _find_type(scan_info)
        x = { k:v for k,v in xtra.items() }
        x.update({'type': stype, 'description': '' })
        return x


class AstorDataProposal(AstorDataPropBase):
    def __init__(self, repo, key, url):
        '''
        Args:
          repo: `DataRepository` object reference (parent)
          key: the "???-cw??-?????-*" string, i.e. proposal key
          url: array access URL for this particular proposal
            subgroup; must have `{scan}` subkey for accessing scans.
        '''
        import functools
        super().__init__(
            repo=repo,
            key=key,
            url=url,
            scan_class=functools.partial(
                DsFactoryScan,
                loader=DatasetFactory(),
                base=url
            )
        )


    def recipe(self, stype):
        try:
            import nx5d.xrd
            return getattr(nx5d.xrd.kmc3, f"_kmc3_recipe_{stype}")
        except AttributeError:
            raise


class LocalRepository(FsDataRepoBase):
    '''
    Access to the intermediate KMC3 data repository.

    Expected data layout is "$ENTRY/YYQ-cw??-?????-*"
    The 5-digit number is translated into packs/proposals (pXXXXXX).
    '''

    def __init__(self, entry=None):
        '''
        Args:
          entry: entry point for the repository.
            If not specified, the contents of the env-var
            "NX5D_DATA_REPO" are used. Defaults to "." if
            the env-var is not defined.
        '''
        import os
        if entry is None:
            entry = os.environ.get('NX5D_DATA_REPO', '.')
        self._full_url = entry
            
        import functools

        parts = entry.split('#')
        if len(parts) == 1:
            self._entry_url = parts[0]
        else:
            self._entry_url, self._entry_scan = parts

        # Proposal number (BESSY internal) from key
        pnr = lambda k: f'{k[9:14]}'

        # Proposal author name (BESSY internal) from key
        pauth = lambda k: f'{k[15:]}'

        # Proposal handle (auth+nr, e.g. "baltrusch12224")
        phandle = lambda k: pauth(k)+pnr(k)
        
        super().__init__(
            self._entry_url,
            scheme=None,
            glob='???-cw??-?????-*',
            proposal_k2h=phandle,
        )


    def _proposal(self, key):
        from collections import defaultdict
        dd = defaultdict(lambda x: x)
        h5path = self._entry_url.\
            format(proposal='{key}').\
            format(key=key)
        return AstorDataProposal(repo=self, key=key, url=h5path)

        
def _kmc3_pilatus_proposals(base, **extras):
    # Loads Pilatus repo data.
    #
    # Returns a structure:
    #  { 'proposal':
    #       'ppath': '<path>',
    #       'pkeys': { 'key': [values...], 'key2': [values...] }
    #       'scans': { ... }
    #  }
    #
    # The contents of `keys` are formatting keys found in
    # the base URL pattern besides "proposal" and "scan".
    # The scan list may or may not be populated, depending
    # on whether "scan" is in the list of parse parameters
    # for "base".
    #
    # See _kmc3_pilatus_scans for the structure of scan data.
    #
    import glob, parse, pprint
    from collections import defaultdict
    from nx5d.xrd.udkm import opcast

    dd = defaultdict(lambda: '*')
    dd.update(extras)
    glob_pattern = base.format_map(dd)

    r = {}
    for f in glob.glob(glob_pattern):
        p = parse.parse(base, f)
        if p is None:
            raise RuntimeError(f'cannot parse: {f}')
        proposal = r.setdefault(p.named['proposal'], {})
        if 'ppath' in proposal and proposal['ppath'] != f:
            #print(f'duplicate proposal {p.named["proposal"]}: '
            #      f'{p.named} vs {proposal["pkeys"]}')
            pass
            
        proposal['ppath'] = f
        proposal['pkeys'] = {k:v for k,v in p.named.items()}
        scans = proposal.setdefault('scans', {})
        
        if "scan" not in p.named:
            continue

        #scan = scans.setdefault(p.named['scan'], {})
        #keys = scan.setdefault('skeys', {})
        #for k,v in p.named.items():
        #    vlist = keys.setdefault(k, [])
        #    vlist.append(v)

    return r


def _kmc3_pilatus_scans(base, scan, **explicit):
    # Return a list of scans within a proposal, according
    # to the base specification. Data format is
    # { 'scan': { 'spath':

    import glob, parse, pprint
    from collections import defaultdict

    class _interdict(defaultdict):
        @classmethod
        def __missing__(cls, key):
            return f'{{{key}}}'

    _imap = _interdict()
    _imap.update(explicit)
    _intermediate = base.format_map(_imap)
    glob_pattern = _intermediate.format_map(defaultdict(lambda: '*'))

    r = {}
    for f in sorted(glob.glob(glob_pattern)):
        s = parse.parse(_intermediate, f)
        if s is None:
            raise RuntimeError(f'cannot parse: {f}')
        scan = r.setdefault(s.named['scan'], {})
        scan['spath'] = f
        scan['skeys'] = { k:v for k,v in s.named.items() }

    return r


def _kmc3_parse_args(args):
    # Returns a (proposal, scan) from the argument list.

    if len(args)<=1:
        print(f'Usage: {args[0]} <propsal> [<scan> [<extas> ...]]')
        exit(-1)

    proposal = args[1]
    scan = None
    extras = None
        
    if len(args)>=3:
        if '=' not in args[2]:
            scan = args[2]
        else:
            print(f'Usage: {args[0]} <propsal> [<scan> [<extas> ...]]')
            exit(-1)

    if len(args)>3:
        extras = dict([a.split('=') for a in args[3:]])

    return proposal, scan, extras


def _kmc3_split_repo(repo):
    # Returns an (outer, inner) path split at '#' for a repo url
    parts = repo.split('#')
    if len(parts) == 2:
        return parts
    if len(parts) == 1:
        return (parts[0], '')
    raise RuntimeError(f'invalid repo URL format "{repo}"')


def _kmc3_scan_to_h5(h5scan, repo):
    os.makedirs(os.path.dirname(repo_target[0]), exist_ok=True)
    silx.io.convert.write_to_h5(
        infile=h5grp,
        h5file=repo_target[0],
        h5path=repo_target[1],
        mode="a",
        overwrite_data=True,
        create_dataset_args={
            'compression': 'lzf'
        }
    )    
    pass

        
def kmc3_from_pilatus(args=None, env=None):
    '''
    Imports KMC3 files from old Pilatus format (SPEC+TIFF) into data repo

    Synopsis:
    
      kmc3-from-pilatus <proposal> [<scan>]

    The application uses the following environment variables:

      - `KMC3_PILATUS_REPO` where the input data is to be read from.
        It needs to incorporate at least the `{proposal}` key, used
        both to glob for proposals by using "*", and to construct
        proposal paths upon request. Any other keys are parsed and
        kept for later use.
        It's expected to have a structure compatible with
        `nx5d.h5like.spec.SpecTiffH5`, essentially meaning that there's
        a SPEC-file somewhere, and a bunch of TIFF files which's names
        can be constructed by iterating throug the frame index.
        Example: "/home/jovyan/data/{year}/{proposal}"

      - `KMC3_PILATUS_SCANS` how to list for proposals of a specific
        scan. It needs to incorporate at least the `{scan}` keyword,
        any other keys are parsed and kept. Can use previously defined
        keys. Can also use the `{repo}` key, which will be replaced by
        the specific repository URL of the requested proposal.

      - `KMC3_PILATUS_TIFF` where to load the TIFF images of a specific
        scan (of a specific proposal). It needs to incorporate at least
        the keywords `{frameidx}`, designating the frame index for which
        a specific TIFF is intended. Can use previously defined keys,
        and additionally the `{repo}` key as above.

      - `KMC3_PILATUS_SPEC` where to load the SPEC file from. Can
        use previously defined keys, including the `{repo}` key.
    
      - `NX5D_DATA_REPO` env var as a target for where the data needs
        to land. The variable should be set to something
        like `s3://<s3-host>/<s3-bucket>/{proposal}/{scan}` or similar.
        It needs to incorporate at least the keys `{proposal}` and
        `{scan}`, but can also make use of extra keys of the other
        variables.
    
    The URL format can contain other keys and/or fixed format placeholders
    (like `{}`), but they will mostly be ignored or used internally, and/or
    passed over to other formatting operations.

    i.e.:
    
      - `<base>/{proposal}/{pkey}.spec` for main spec file
    
      - `<base>/{proposal}/pilatus/[S00000-00999]/S{scan:05d}/{pkey}-S{scan}-{frame}.tiff`
        for location of the TIFF image series for each scan.
        The `S00000-00999` part is probed (because KMC3 had data storage
        formats both with, and without, the corresponding intermediary
        folder).

    Here `{year}` is a KMC3-specific information parsed from the proposal
    key itself.

    The import action completely overwrites existing datasets. It uses
    `silx.io.convert.write_to_h5` repeatedly, once per scan.

    If you're using the NX5D package, there's an autocomplete BASH script
    available at `./contrib/slim-completion.sh`
    ("source ./contrib/slim-completion.sh").
    
    Args:
    
      proposal: the full proposal string (e.g. `232-cw10-122252-hua`)
    
      scan: optionally, glob pattern of which scan to import. Setting this
        to `*` results in all scans will be imported at once. Setting this
        to the empty string or omitting (the default), will re-import only
        the last scan still present at target, and all following scans
        present in the source file, resulting in "bringing the target file
        up-to-date" with the current state of the data.
    '''

    from nx5d.h5like.spec import SpecTiffH5
    import os, sys, glob, pprint, tqdm, parse
    
    if args is None: args = sys.argv
    if env is None: env = os.environ

    proposal, scan, extras = _kmc3_parse_args(args)
    
    repo_base = env['NX5D_DATA_REPO']

    pil_base = env['KMC3_PILATUS_REPO']

    pil_scans = env.get('KMC3_PILATUS_SCANS',
                        '{repo}/{instrument}/{scanlevel}/S{scan}')
    
    pil_tiff = env.get('KMC3_PILATUS_TIFF',
                       '{repo}/{instrument}/{scanlevel}/S{scan}/{proposal}_{scannr}_{frameidx}.tif')
    
    pil_spec = env.get('KMC3_PILATUS_TIFF',                       
                       '{repo}/{proposal}.spec')

    pil_proplist = _kmc3_pilatus_proposals(
        pil_base, **(extras if extras is not None else {})
    )

    if len(proposal)>0 and proposal[-1] == '?':
        print('\n'.join(filter(lambda x: x.startswith(proposal[:-1]), pil_proplist.keys())))
        return 0

    # This is the proposal dictionary we're looking for
    pil_prop = pil_proplist[proposal]
    pil_prop['scans'] = prop_scans = _kmc3_pilatus_scans(
        base=pil_scans,
        repo=pil_prop['ppath'],
        scan=scan if scan not in (None, '?') else '*'
    )

    if (scan is None) or (scan[-1] == '?'):
        if len(prop_scans) == 0:
            print(f'No scans for "{proposal}"')
            return 0
        
        if scan is not None:
            sl = filter(lambda x: x.startswith(scan[:-1]), prop_scans.keys())
        else:
            sl = prop_scans.keys()

        print('\t'.join(sl))
        return 0

    def scankeys(x):
        return {
            k:next(iter(v)) for k,v in prop_scans[x]['skeys'].items()
        }

    # Normally we would want (and need) to open the Spec
    # file only once per proposal; however, depending on
    # the exact base URL formats, there may be format keys
    # that make the TIFF file paths dependent on the scan
    # number (e.g. "scanlevel" key).
    #
    # To have our cake and eat it too, we try twice to
    # open the Spec file: once here, and once in the scan
    # loop.
    def open_experiment(fk):
        spath = pil_spec.format_map(fk)
        tpath = pil_tiff.format_map(fk)
        if not os.path.exists(spath):
            raise RuntimeError(f'{proposal}: no specfile at "{spath}"')
        return SpecTiffH5(spath, instrumentName='images',
                          framePathFmt=tpath, cache=False)

    import fnmatch, silx.io.convert

    for pname,pdata in pil_proplist.items():
        selected = fnmatch.filter(pdata['scans'].keys(), scan)
        if len(selected) == 0:
            continue

        print(f'Converting {len(selected)} scan(s) from "{pname}"')

        fmt_keys = pdata['pkeys'].copy()

        fmt_keys.update(**{
            # Updating keys promised by kmc3-from-pilatus doc
            'repo': pdata['ppath'],
            #'proposal': pname,

            # Updating keys promised by SpecTiffH5.
            'frameidx': '{frameidx}',
            'scanidx': '{scanidx}',
            'scannr': '{scannr}',
            'basename': pname,
            'dirname': pdata['ppath']
        })

        try:
            h5 = open_experiment(specfile, tiff_fmt)
        except NameError:
            h5 = None

        for sname in tqdm.tqdm(selected):
            iscan = int(sname)
            fmt_keys.update(pdata['scans'][sname]['skeys'])
            fmt_keys.update(**{
                'scan': sname,
                'iscan': iscan
            })

            def _save_scan():
                h5grp = h5[f'{iscan}.1']
                repo_target = _kmc3_split_repo(repo_base.format_map(fmt_keys))
                os.makedirs(os.path.dirname(repo_target[0]), exist_ok=True)
                silx.io.convert.write_to_h5(
                    infile=h5grp,
                    h5file=repo_target[0],
                    h5path=repo_target[1],
                    mode="a",
                    overwrite_data=True,
                    create_dataset_args={
                        'compression': 'lzf'
                    }
                )
            
            if h5 is None:
                with open_experiment(fmt_keys) as h5:
                    _save_scan()
                h5 = None
            else:
                _save_scan()
