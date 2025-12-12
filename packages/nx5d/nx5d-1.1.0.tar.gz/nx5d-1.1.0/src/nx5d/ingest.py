#!/usr/bin/python3

from pathlib import Path
import h5py
import logging
import traceback
logger = logging.getLogger(__name__)

'''
This is about writing to NX(-like) backends with limited permissions.

We're focusing on the `nx5d` data model (i.e. frame dimension first,
everything after, scan/run structure, measuring one frame at a time).
On top of that, we're implementing a `.push()` or `.append()`
functionality. We're encompassing the pushing of data points by a
`.initialize()` and a `.finalize()` call.
'''



class IngestUrlError(Exception): pass

class IngestDeviceExists(Exception): pass

class H5ScanSink:

    def __init__(self, source, scan, **devices):
        
        self.data_sink = source
        self.scan_spec = scan
        
        scan_path = f'{self.data_sink.group_path}/{self.scan_path_element}'
        logger.info(f'Scan {scan}: requiring path "{scan_path}" in "{self.data_sink.file_path}"')

        with h5py.File(self.data_sink.file_path, 'a') as h5:
            self.scan_path = self._ensure_nxentry(scan_path, h5).name

        logger.info(f'Scan {scan}: {self.data_sink.file_path}::{self.scan_path}')

        self._datapath = {}

        try:
            for name,dspec in devices.items():
                self.ensure_device(name, **dspec)
        except Exception as e:
            logger.error(f'Sink: {e}, traceback: {traceback.format_exc()}')


    @property
    def scan_path_element(self):
        ''' Return the part of the HDF5 path which designates the scan only. '''
        return f'{self.scan_spec}.1'


    def _ensure_nxentry(self, path, h5obj, attr_defaults=None):
        #
        # Recursively makes sure that `path` exists in h5obj.
        # Returns a tuple (obj, name) of the deepest element.
        # Note that if h5obj is `None`, the `obj` return value
        # will also be an invalid object handle. You can use `name`
        # to find it again once you re-open the file.
        #

        if attr_defaults is None:
            attr_defaults = { 'NX_class': 'NXentry' }
        
        i = path.find('/')
        first = path[:i] if i > 0 else path
        g = h5obj.require_group(first)

        for k,v in attr_defaults.items():
            try:
                a = g.attrs[k]
            except KeyError:
                logger.info(f'Defaulting to "{k}" -> "{v}" for "{g.name}"')
                g.attrs[k] = v

        if i > 0 and i < len(path):
            return self._ensure_nxentry(path[i+1:], h5obj=g)
        else:
            return g

        
    def _subpath(self, *pelems):
        # returns a path made up of path elements 'pelems' within
        # the root of the current scan
        return '/'.join([self.scan_path] + list(pelems))


    def ensure_device(self, name, shape, dtype, dims=None, create_args=None):
        ''' Makes sure the necessary groups and datasets exist for device.

        This creates:
        
          - A NDF5 group `instrument/{name}` if it doesn't exist
        
          - A dataset `instrument/{name}/data`, which has the shape
            `(0, <shape>)`, and is extensible in its first dimension
            (i.e. to expand on the `0`).

          - A HDF5 soft-link `measurement/{name}` pointing to
            `instrument/{name}/data`

          - If `dims` is not `None`, ... (FIXME: need to expand this
            into CDF4 / xarray territory!)

        Args:

            name: string, the name of the device
        
            shape: tuple, describing N-1 dimensions of the device. A 0-th
              dimension with length 0, editable, will be added in front.
              Generally, the shape of all dimensions except the first one
              (which is automatically added) is fixed, i.e. `maxshape`
              parameter for `.create_dataset()` is the same as the shape
              itself. However, we also accept `None` as a shape designation,
              in which case we automatically translate that to size `0`
              and `maxshape` of `None` for that particular dimension.

            dtype: Data type of the device. Since we don't have any data
              yet at this stage, the parameter is mandatory.
        
            dims: If this is different from `None` (the default), then the
              data is written in CDF4-like format, with intrinsic scaling.
              This is expected to be a `dict` with dimention names
              as its keys (strings), and the data types as the values.
              If any of the value(s) are `None`, then `dtype` is automatically
              assumed for the data type. The key `"frame"` is reserved for the
              0-th dimension and its data type is `int`, if not otherwise
              specified.
        '''

        if create_args is None:
            create_args = { 'compression': 'lzf' }

        if dims is not None:
            logger.error(f'`dims` keyword not yet implemented!')


        with h5py.File(self.data_sink.file_path, 'a',
                       **self.data_sink.h5args) as h5:
            
            dev_grp = self._ensure_nxentry(self._subpath('instrument', name), h5,
                                           attr_defaults={'NX_class': 'NXinstrument'})


            shape_len = tuple([s if s is not None else 0 for s in shape])
            shape_max = tuple([s for s in shape])

            try:
                data = dev_grp.create_dataset(f'{name}', dtype=dtype,
                                              shape=(0, *shape_len),
                                              maxshape=(None, *shape_max))
                meas_grp = self._ensure_nxentry(self._subpath('measurement'), h5,
                                                attr_defaults={'NX_class': 'NXcollection'})
                meas_grp[name] = h5py.SoftLink(data.name)    

            except ValueError:
                data = dev_grp[f'{name}']
                s = tuple([i for i in shape_len])
                if data.shape[1:] != s:
                    logger.error(f'For {dev_grp.name} / {name}, required shape is {s} (from: {shape}), found {data.shape[1:]}')
                    raise IngestDeviceExists()

            self._datapath[name] = data.name


    def _append_to_device(self, name, data, h5):
        dset = h5[self._datapath[name]]
        if data.shape != dset.shape[1:]:
            raise RuntimeError(f'Data for "{name}" expected '
                               f'with shape "{dset.shape[1:]}" '
                               f'got shape {data.shape} instead.')
        dset.resize((dset.shape[0]+1, *dset.shape[1:]))
        dset[-1] = data


    @property
    def devices(self):
        return tuple([k for k in self._datapath.keys()])


    @property
    def url(self):
        return f'{self.data_sink.url}{self.scan_path_element}'


    def append(self, data=None):
        ''' Appends one single data point to the scan, across all dimensions.

        Args:

            data: the data. The preferred way is to pass a dicitonary of
              arrays in `data`, or an `xarray.Dataset`. Each dataset must
              have the shape that was initially specified with at
              the beginning (see `.ensure_device()`).
        '''
        with h5py.File(self.data_sink.file_path, 'a') as h5:
            for k in self.devices:
                self._append_to_device(k, data[k], h5)
    

class H5DataSink:
    '''
    HDF5 data sink for a single scan (run).

    Writes to HDF5 files. Tries to adhere to the ESRF-esque data
    layout. We're using "scan" and "run" pretty interchangably here,
    although they mean different things.
    '''

    def __init__(self, h5like=None, h5file=None, h5group=None, **h5args):
        ''' Initializes the sink.
        
        Args:
            h5like: File path or a string "<file>::<group>", or "<file>#<group>"

            h5file: string or Path, refers to the HDF5 file only. (FIXME: h5 object?)

            h5group: string, the group path inside the HDF5 file
        '''

        # this is a string/path, we need to open it
        if (h5like is not None) and \
           not hasattr(h5like, 'create_dataset'):
            f, g = self._url_split(h5like)
                
            self.h5like = None
            self._own_h5 = True

        # This is a HDF5 file / group that is already open
        else:
            f, g = None, None
            self.h5like = h5like
            self._own_h5 = False

            
        self.file_path = Path(f) if f is not None \
            else Path(h5like) if h5like is not None \
                 else None
        self.group_path = g or "/"

        self.h5args = h5args or {}

        self._open_scans = {}        


    @property
    def url(self):
        ''' Returns a copy of the current URL top-level sink URL. '''
        return f'{self.file_path}{self._url_split}{self.group_path}'

        
    def _try_split(self, text, s):
        parts = text.split(s)
        if len(parts) > 2:
            raise IngestUrlError(f'H5-like path contains multiple # or ::, don\'t know how to split')

        if len(parts) == 2:
            return parts

        return parts[0], None


    def _url_split(self, url):
        try:
            f1, g1 = self._try_split(url, '#')
        except IngestUrlError:
            f1, g1 = None, None

        try:
            f2, g2 = self._try_split(url, '::')
        except IngestUrlError:
            f2, g2 = None, None

        if g1 is not None:
            self._url_split = '#'
            return (f1, g1)
        elif g2 is not None:
            self._url_split = '::'
            return (f2, g2)
        elif f1 == f2:
            self._url_split = '#'
            return f1, "/"

        raise IngestUrlError(f'Cannot parse url {url} -- did you have multiple # or :: in it?')


    def open_scan(self, scan, **devices):
        if scan not in self._open_scans:
            self._open_scans[scan] = H5ScanSink(self, scan, **devices)
        return self._open_scans[scan]
