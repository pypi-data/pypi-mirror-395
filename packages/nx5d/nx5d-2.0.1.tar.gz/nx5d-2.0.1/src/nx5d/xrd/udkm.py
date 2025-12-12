from nx5d.xrd.base import DatasetFactory as DSBase
from nx5d.repo.base import DataScanBase
from nx5d.xrd.signal import QMapper
from nx5d.repo.filesystem import FilesystemWalker
from nx5d.repo.filesystem import DataRepository as FsDataRepoBase
from nx5d.repo.filesystem import DataProposal as FsDataPropBase

import tifffile, xarray, numpy, logging, os, glob, urllib

logger = logging.getLogger(__name__)

def opcast(v):
    # dirty opportunistic cast
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v

class ScanTypeMismatch(RuntimeError):
    def __init__(self, scan_type):
        super().__init__(f'Scan type mismatch: {scan_type}')

class DatasetFactory(DSBase):
    '''
    DatasetFactory implementation for UDKM "air-gap" based data format.

    This isn't a HDF5-based format, but we'll still reuse the
    base class. The ._build_single() method is reimplemented
    and the 1st parameter (formerly "h5like") is re-interpreted.
    Everything else is reusable as-is from the base class.
    '''

    ## The saving format of UDKM is funny (to put it friendly) and unconsistent.
    ## It makes for a good human-readable format, fit for reverse-engineering
    ## in case of a zombie apocalypse. But it's less than ideal for atomated
    ## processing.
    ##
    ## From bits n pieces of information, here's what we know:
    ## 
    ## - *Generally* (but not always), files begin with one or several line(s)
    ##   of column description, TAB-seprarated; the column names themselves
    ##   contain all kinds of characters (besides TAB), and sometimes supplementary
    ##   information like units in brackets. Example:
    ##   ```
    ##   % Column\tColumnt 2\tColumn [3]\n
    ##   ```
    ##   We'll call  this the "column indicator".
    ##
    ## - *Sometimes* (mostly in "rockingcurves" files), a 2nd line containing even
    ##   more columns are named, which we'll call the "datapoint indicator":
    ##   ```
    ##   % StartTime\tEndTime\tImageName\n
    ##   ```
    ##
    ## - Then the data points are pouring in, two lines for each data point.
    ##   The first line is the timing and image name of the data point,
    ##   TAB-separated. The data points correspond to the "datapoint indicator":
    ##   ```
    ##   % 15:00:09.327\t15:00:12.637\timage00000.tif\n
    ##   ```
    ##   Note that sometime the "datapoint indicator" is missing (i.e. the line
    ##   denoting the columns), but the datapoint indication _data_ is nonetheless
    ##   delivered (e.g. for "RSS"-style "scans*.dat" files).
    ##
    ##   The 2nd line is the data itself, corresponding to the "column indicator"
    ##   (note the lack of a leading `% ` here):
    ##   ```
    ##   1.000000\t-5.000000\t1.000000\t13.220000\t0.144264\t842033.695276\t2165.333333\t0.000000\t0.000000\t...\n
    ##   ```
    ##   Note that the number of data entries per line exceeds the number of columns!
    ##   This is because, usually, the last column is something like a "Curve..." or
    ##   "Intensities...", and is usually just a processed version of the data already
    ##   contained in the .TIFF file (typically integrated along one direction).
    ##
    ##   (Of course we have no way of knowing which "column" is the one with multiple
    ##   values, but going forward we're just going to assume that it's the last one).
    

    ## We're listing all the indicator names here, and (manually) assigning them
    ## python-compatible names. We're using a flat structure here for simplicity.
    ## Implicitly, this assumes that there are no duplicates across different .dat
    ## file types (or, if there are, that they're always going to be translated
    ## the same).
    ## If that's not the case, somebody will need to break this up in a per-file
    ## dictionary :-)
    ##
    _default_indicators = {
        # column indicator names from rockingcurves*.dat:        
        'Loop':                 'loop',
        'Theta / deg.':         'theta',
        '2Theta + Corr / deg.': 'ttheta',
        'Crystal':              'crystal_v',
        'Crystal Calib':        'crystal_calib',
        'Rocking Curve':        'images',
        
        # datapoint indicator names from rockingcurves*.data:
        'StartTime':            'start_time',
        'EndTime':              'end_time',
        'ImageName':            'image_name',
        
        # column indicator names form scans*.dat:
        'Loop_Delay':           'loop_delay',
        'Delay':                'delay',
        'Loop_Theta':           'loop_theta',
        'Theta':                'theta',
        'Crystal [V]':          'crystal_v',
        'Crystal [ph/s]':       'crystal_calib',
        'Pilatus [ph/s]':       'cntrate',
	    'Repeats':              'repeats',
        'ImageNumber':          'image_number',
        'Intensities [ph/s]':   'images',
    }

    # Involuntarily (but usefully :-) the UDKM data are already typed.
    # As a type designator, we're using the presence of specific files.
    _scan_types = {
        'sRSM': [ 'rockingcurves{sfx}.dat' ],
        'tRSS': [ 'scans{sfx}.dat' ],
        'xRSS': [ 'allSteps{sfx}.dat' ]
    }
    
    def __init__(self, indicators=None):
        '''
        Initializes UDKM data retriever.

        Args:
            indicators: Optional dictionary to override default indicators
              (i.e. column names from UDKM .dat files). The keys must be
              verbatim column names -- without the TABs, but with all the
              punctuation, case-sensitive. The values must be python
              symbol names (i.e. preferrably lower-case, using underscore '_').
              The names will be used as data keys in the resulting xarray
              dataset.
        '''
        self.indicators = self._default_indicators.copy()        
        if indicators is not None:
            self.indicators.update(indicators)


    def _get_type(self, src, **keys):
        # Tries to determine the type of scan 'src' from presence or absence
        # of specific files.
        for k, markers in self._scan_types.items():
            for m in markers:
                try:
                    with open(os.path.join(src, m.format(**keys)), 'r') as f:
                        return k
                except FileNotFoundError:
                    pass

        raise RuntimeError(f'msg="uknown type" scan="{src}"')


    def typeof(self, src):
        '''
        Returns the scan type of scan at 'src' (efficiently, tries to open
        as little data as possible).
        '''
        return self._get_type(src, sfx=self._scan_suffix(src))


    def paramsof(self, src):
        '''
        Returns the contents of the params file.
        '''
        import pandas, io
        sfx = self._scan_suffix(src)
        comments = []
        kw = {}
        at_key = None
        params_file = os.path.join(src, f'parameters{sfx}.txt')
        try:
            with open(params_file, 'rb') as f:
                for line in f:
                    try:
                        txt = line.decode('utf-8').strip()
                    except:
                        txt = line.decode('windows-1252').strip()

                    if ': ' in txt:
                        k, v = txt.split(': ')
                        kw[k] = v
                        at_key = k
                    else:
                        if len(txt) == 0:
                            continue
                        if at_key is not None:
                            kw[at_key] += txt
                        else:
                            comments.append(txt)
            kw['Comments'] = ' '.join(comments)
            return kw
        except FileNotFoundError as e:
            logger.warning(e)
            return {}


    def _open_as_type(self, src, scan_type, **keys):
        # Tries to open a specific scan as type 'scan_type'.
        # Raises an error (typically FileNotFound) if file is
        # of a different type.
        # Returns a file handle (open(...)) on success.
        for m in self._scan_types[scan_type]:
            try:
                fname = m.format(**keys)
                #print(f'trying type {scan_type}, signature file {fname}, path {src}')
                fobj = open(os.path.join(src, fname), 'r')
                #print(f'success with {fname}')
                return fobj
            except FileNotFoundError as e:
                #print(f'fail for {fname}')
                logger.info(e)

        raise ScanTypeMismatch(scan_type)


    def _scan_suffix(self, src):
        return src[-6:]
        
    
    def _build_single(self, src, **fmtkeys):
        '''
        Reads a single UDKM experiment dataset.

        Args:
            src: The path / directory where the data is available
              (e.g. "/path/to/data/20250304/174356",
              or "C:\\path\\to\\data\\20250304\\174356").

            **fmtkeys:
        '''
        sfx = self._scan_suffix(src)
        
        for scan_type in ('sRSM', 'tRSS', 'xRSS'):
            try:
                with self._open_as_type(src, scan_type, sfx=sfx) as f:
                    logger.info(f'Trying as type: {scan_type}')
                    fields, images = self._parse_as_type(f, scan_type, base=src)

                    dvars = { k: ('index', v) for k, v in fields.items() }
                    dvars.update({ 'images': (('index', 'x', 'y'), images) })

                    r = xarray.Dataset(data_vars=dvars)

                    if scan_type in ('tRSS',):
                        logger.warning('msg="ACHTUNG, incomplete theta reconstruction"')
                        # ACHTUNG! FIXME: correction needs to be applied here!
                        r['ttheta'] = r.theta * 2

                    return r
                    
            except ScanTypeMismatch as e:
                #logger.warning(e)
                pass

            except Exception as e:
                logger.error(e)
                raise

        raise RuntimeError(f'msg="Don\'t know how to open scan" src={src}')


    def _parse_as_type(self, f, scan_type, base):

        # Parses the indicator lines without leading '% ' (i.e. "Head\tHead\t...\n")
        _make_indicators = lambda line: [
            self.indicators[k.strip()] for k in line.split('\t')
        ]

        # Parses a line like 'Data\tData\tData\t...\n' and assigns
        # the data to the specified indicator list
        _make_data = lambda line, indi: {
            k.strip(): opcast(v.strip())  for k,v in zip(indi, line.split('\t'))
        }

        # Returns image data array from file
        def _make_image(img_path, expected_shape=None):
            try:
                return tifffile.imread(img_path)
            except FileNotFoundError as e:
                missing.append(img_path)
                if expected_shape is None:
                    raise e
                return numpy.full(expected_shape, numpy.nan)

        # Data keys
        lkeys = None

        # Image timing metadata keys
        ikeys = None if scan_type in ('rsm',) \
            else ('start_time', 'end_time', 'image_name')
        imeta = None
        
        img_shape = None
        fields = {}

        missing = []
        images = []

        for line in f:
            if line.startswith('%'):
                # meta-information lines                    
                if lkeys is None:
                    lkeys = _make_indicators(line[2:])
                    continue
                elif ikeys is None:
                    ikeys = _make_indicators(line[2:])
                    continue
                else:
                    imeta = _make_data(line[2:], ikeys)
                    continue
            else:
                # numerical data lines
                pt = _make_data(line, lkeys)
                for k,v in pt.items():                    
                    fields[k] = numpy.append(fields.get(k, numpy.array([])), v)

            # Load the image
            img = _make_image(
                os.path.join(base, f"{imeta['image_name']}"),
                expected_shape=img_shape
            )
            if img is not None:
                img_shape = img.shape
            images.append(img)


        if len(images) > 0:
            logger.warning(f'msg="Some images missing, list follows"')
            if len(missing) > 0:
                msgi = f'{len(missing)}'
                logger.warning(f'msg="Missing images" '
                               f'total="{msgi}" '
                               f'base="{base}"')

        return fields, numpy.concatenate([i[None, ...] for i in images])


ExperimentTemplate = {
    # All the axes -- goniometer first (outer to inner), then detector.
    "goniometerAxes": {
        'theta': 'y-',
    },

    "detectorAxes": {
        'ttheta': 'y-',
    },

    "detectorTARAlign": (0.0, 0.0, 0.0),

    "imageAxes": ("y-", "z+"),
    "imageSize": (195, 487),
    "imageCenter": (97, 241),

    # This could also be used instead of 'imageChannelSize' below.
    # It's the same physical quantity, but in degrees/channel
    # instead of relative length.
    "imageChannelSpan": None,

    "imageDistance": 680.0,
    "imageChannelSize": (0.172, 0.172),  # same unit as imageDistance (mm)

    "sampleFaceUp": 'z-',
    "beamDirection": (1, 0, 0),

    "sampleNormal": (0, 0, -1),

    "beamEnergy": 8048.0,

}


ExperimentTemplate_new = {
    # All the axes -- goniometer first (outer to inner), then detector.
    "goniometerAxes": {
        'theta': 'y-',
    },

    "detectorAxes": {
        'ttheta': 'y-',
    },

    "detectorTARAlign": (0.0, 0.0, 0.0),

    "imageAxes": ("y-", "z+"),
    "imageSize": (195, 487),
    "imageCenter": (97, 241),

    # This could also be used instead of 'imageChannelSize' below.
    # It's the same physical quantity, but in degrees/channel
    # instead of relative length.
    "imageChannelSpan": None,

    "imageDistance": 680.0,
    "imageChannelSize": (0.172, 0.172),  # same unit as imageDistance (mm)

    "sampleFaceUp": 'z+',
    "beamDirection": (1, 0, 0),

    "sampleNormal": (0, 0, +1),

    "beamEnergy": 8048.0,

}

# OBSOLETE -- only for reference purposes
#class DataRun:
#    '''
#    Access to a single UDKM data run.
#
#    Offers easy access to raw data, cooked data, spice data,
#    and experimental information.
#    '''
#    def __init__(self, proposal, key, cache=False):
#        '''
#        Initializes a scan/run management class.
#
#        Args:
#
#          proposal: Parent proposal object
#        
#          key: The scan key
#        
#        '''
#        self._proposal = proposal
#        self._scan_key = key
#
#        try:
#            # If the scan can be interpreted as an integer, we're going to
#            # use it. Otherwise we'll just make up a value. (At this point,
#            # the user should know...)
#            # This functionality is probably better implemented upstream.
#            iscan = int(key)
#        except ValueError:
#            iscan = -1
#
#        #print('new UDKM run at base', self._proposal.scan_url)            
#
#        # proposal.scan_url here is a URL (i.e. with scheme n all), and we
#        # only need the path. At this point, we need to transform everything
#        # into a simple POSIX path.
#        import urllib
#        purl = urllib.parse.urlparse(self._proposal.scan_url.format(scan=key, iscan=iscan))
#        if purl.scheme != "file":
#            raise RuntimeError(f'Invalid scheme "{purl.scheme}" for UDKM legacy')
#        self._base = purl.path
#        
#        self._cache = True
#        self._factory = DatasetFactory()
#        self._raw = None
#        self._cooked = None
#        self._spice = None
#        self._mapper = None
#        self._exp_info = None
#
#    @property
#    def key(self):
#        return self._scan_key
#
#    @property
#    def type(self):
#        return self._factory.typeof(self._base)
#
#    @property
#    def summary(self):
#        return {
#            'type': self.type,
#            'description': self._factory.paramsof(self._base)['Comments']
#        }
#
#    @property
#    def raw(self):
#        if self._raw is None:
#            tmp = self._factory(self._base)
#            if self._cache in (True, 'raw', 'all'):
#                self._raw = tmp
#        else:
#            tmp = self._raw
#        return tmp
#
#
#    def invalidate_raw(self):
#        self._raw = None
#
#
#    @property
#    def exp_info(self):
#        if self._exp_info is None:
#            self._exp_info = ExperimentTemplate.copy()
#        return self._exp_info
#    
#    def cook(self, raw):
#        if self._mapper is None:
#            self._mapper = QMapper(**(self.exp_info))
#
#        run_type = self.type
#        if run_type == 'sRSM':
#            # RSM-data
#            return self._mapper.qmap(self.raw)
#        elif run_type == 'tRSS':
#            # RSS-data
#            c = raw.groupby(raw.delay).map(self._mapper.qmap, dims=('qy', 'qz'))
#            return c
#        else:
#            raise RuntimeError(f'msg="No recipe for run type" type={run_type}')
#
#
#    @property
#    def cooked(self):
#        if self._cooked is None:
#            tmp = self.cook(self.raw)
#            if self._cache in (True, 'all', 'cooked'):
#                self._cooked = tmp
#        else:
#            tmp = self._cooked
#        return self._cooked
#
#
#   @property
#    def spice(self):
#        logger.error('Spice access not available for UDKM')


class LegacyDataProposal(FsDataPropBase):
    def __init__(self, repo, key, url):
        '''
        Access to a UDKM data-pack (i.e. "a day").

        This is for the legacy repository format. Please use `DataProposal`
        and `ProjectRepository instead.

        Args:
          repo: Repository parent object
          key: Identifying key for this proposal
          url: The base URL of the repository
        '''
        super().__init__(repo,
                         key,
                         url,
                         glob='[0-9]'*6,
                         scan_class=DataScan,
                         scan_k2h=lambda p: f'r{p}')


    def _spice_repo(self, url=None):
        # Adding "recipes" and "exp_info", if not found.
        repo = super()._spice_repo(url)
        me = repo.proposal(key=self._proposal_key)
        have = me.collection.view(None)
        if "recipes" not in have.handles():
            from kmc3recipes.cooking import RecipeMap
            me.seed("recipes", __default__=None, **RecipeMap)
        if "exp_info" not in have.handles():
            me.seed("exp_info", **ExperimentTemplate)
        return repo


# Old name
DataPack = LegacyDataProposal


class LegacyRepository(FsDataRepoBase):
    '''
    Access to a complete UDKM data repository in pre-2026 format.

    Expected data layout is "$ENTRY/YYYY/YYYYMMDD/HHmmSS/...".
    The "YYYY/YYYYMMDD" is transtlated to packs (pYYMMDD),
    and the "HHmmSS" part is translated to runs (rHHmmSS).
    '''

    def __init__(self, entry=None):
        '''
        Args:
          entry: entry point for the repository. If not specified,
            the contents of the env-var "UDKM_DATA_REPO" are used.
            Defaults to "." if the env-var is not defined.
        '''
    
        if entry is None:
            entry = os.environ.get('UDKM_DATA_REPO', '.')
        
        logger.info(f'msg="UDKM legacy repo" url="{entry}"')
        
        super().__init__(f'file://{entry}',
                         glob='20??/20??????',
                         proposal_k2h=lambda k: f'p{k[-8:]}')


    def _proposal(self, key):
        # Construct an UDKM proposal based on `DataPack`, from key and URL.
        print(f'New UDKM proposal request {key} at {self.repo_url}')
        return DataPack(self, key, self.repo_url)



class DataScan(DataScanBase):
    '''
    Main scan class for classic UDKM scans.
    '''
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        pu = urllib.parse.urlparse(self.url)
        self._scan_path = pu.path
        self._loader = DatasetFactory()
        
    def _get_raw(self):
        ds = self._loader(self._scan_path)
        po = self._loader.paramsof(self._scan_path)
        # Try this to assign 'po' to data arrays instead of attrs:
        # ds = ds.assign({
        #    'pkey': [k for k in po.keys()],
        #    'params': ('pkey', [v for v in po.values()])
        # })
        return ds.assign_attrs(po)

    def _get_summary(self):
        po = self._loader.paramsof(self._scan_path)
        return {
            'type': self._loader.typeof(self._scan_path),
            'description': po.get('Comments', ''),
            'steps': len(glob.glob(f'{self._scan_path}/*tif')),
        }



class DataProposal(FsDataPropBase):
    def __init__(self, repo, key, url):
        '''
        Access to a UDKM project-style data proposal.
        
        Args:
          repo: Repository parent object
          key: Identifying key for this proposal
          url: The base URL of the repository
        '''
        super().__init__(repo,
                         key,
                         url,
                         glob='20??????/??????',
                         scan_class=DataScan,
                         scan_k2h=lambda p: f'r{p[2:8]}{p[9:]}')


    def _spice_repo(self, url=None):
        # Adding "recipes" and "exp_info", if not found.
        repo = super()._spice_repo(url)
        me = repo.proposal(key=self._proposal_key)
        have = me.collection.view(None)
        #print('checking spice')
        if "recipes" not in have.handles():
            #from kmc3recipes.cooking import RecipeMap
            me.seed("recipes", dict(
                __default__=None,
                tRSM="pymod:///kmc3recipes.cooking#TRSM",
                sRSM="pymod:///kmc3recipes.cooking#sRSM",
                xRSS=None,
                tRSS=None,
                rocking="pymod://kmc3recipes.cooking#sRSM"
            ))
        if "exp_info" not in have.handles():
            me.seed("exp_info", **ExperimentTemplate)
        return repo


class ProjectRepository(FsDataRepoBase):
    '''
    Access to new-style UDKM repository ("project-based").

    The folder structure here is .../YYYYMM_description/ for proposals,
    and .../YYYYMMDD/HHmmSS/ for scans within a proposal.
    '''

    def __init__(self, entry=None):
        '''
        Args:
          entry: entry point (absolute folder!) for the repository. Defaults to
            the contents of the 'UDKM_PROJECT_REPO' environment variable.
        '''

        if entry is None:
            entry = os.environ['UDKM_PROJECT_REPO']
        
        from os import path
        ap = path.abspath(path.expanduser(entry))
        super().__init__(
            url=f'file://{ap}',
            glob='20[0-9][0-9][0-1][0-9]_*',
            proposal_k2h=lambda x: f'{"".join([k.lower() for k in filter(lambda i: i.isupper(), x[7:])])}{x[2:6]}',
            proposal_class=DataProposal,
            proposal_kwargs={}
        )                 

DataRepository = LegacyRepository
