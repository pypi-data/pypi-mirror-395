#!/usr/bin/python3

import silx.io.commonh5 as ch5
import numpy as np

from os import path, walk
from glob import glob
from itertools import chain
from nx5d.h5like.spec import SpecH5LazyTiffNode, H5Group

import h5py
import re

import logging

''' Selected data formats for the PETRA3 synchrotron at DESY.
'''

def read_fio(f):
    ''' Reads a FIO file and returns an xarray dataset.

    Returns:
        Two dictionaries `(parameters, columns)`, where `parameters` contains all the
        `%p` section data of the FIO file, and `columns` contains arrays with all
        the `%d` section data.
    '''

    # Parameters (%p section stuff).
    # Eacy line is a key=value entry containing either a number, or an array as value.
    def param_eval(data):
        ''' Parse a %p line: return either a single float value, or an array. '''

        parts = data.split('=')
        assert len(parts) == 2
        
        key = parts[-2].strip()
        val = parts[-1].strip()

        try:
            if val[0] == '[':
                return {
                    key: np.array([
                        float(i.strip(',')) for i in val.strip('[]').split(' ')
                    ])
                }
            else:
                return {key: float(val)}
        except Exception as e:
            logging.error("Don't understand parameter '%s': %s" % (key, str(e)))
            return {key: val.encode('utf-8')}


    # Columns data (%d) stuff.
    # Data line is either a "Col ..." line, specifying ("Col", index, name, data_type)
    # or is an acutal space-separated list of items (numbers).
    data_types = { 'DOUBLE': float }   # Data type translators; so far, only DOUBLE
    data_column_types = []             # Here we'll store the types (one for each column)
    data_column_names = []             # Here we store the names; used for dict keys,
    def data_eval(data):
        dl = data.split(' ')
        if dl[0] == "Col":
            data_column_types.append(dl[3])
            data_column_names.append(dl[2])
            return None
        return { data_column_names[i]:\
                 np.array([data_types[data_column_types[i]](d)]) \
                 for i,d in enumerate(dl) }

    
    # Reading FIO file in several "states" demarked by the '%...' magic.
    # Each "state" has a parsing function associated with it.
    cur_state = None    
    read_states = { '%c': lambda l: None,
                    '%p': param_eval,
                    '%d': data_eval }


    # Here we store the final data
    data_dict = { "%p": dict(),
                  "%d": dict() }
    
    with (open(f) if isinstance(f, str) else f) as ff:
        for line in ff:
            l = line.strip()
            
            if l.startswith('!'):
                continue
            
            if l.startswith('%'):
                cur_state = l
                continue

            # Transform data according to current state (comment, params, column data)
            line_dict = read_states[cur_state](l)

            if line_dict is None:
                continue

            # Store data into data_dict; if there's already a key present, it's assumed
            # to contain an array item (typically only the case with column data) and
            # we just append the new item to that.
            for k,v in line_dict.items():
                ex = data_dict[cur_state].get(k, None)
                data_dict[cur_state][k] = v if ex is None else np.concatenate((ex, v))

    return data_dict['%p'], data_dict['%d']
            

class DictDataGroup(ch5.Group):
    ''' Encapsulates / creates a HDF5-like node from a Python dictionary.
    '''

    def __init__(self, name, parent, data, attrs=None):
        super().__init__(name, parent, attrs)
        
        for k,v in data.items():
            dset = v if isinstance(v, np.ndarray) else np.array(v)
            self.add_node(ch5.Dataset(k, parent=self, data=dset))


class FioGroup(ch5.Group):
    ''' Inserts a FIO file as a HDF5 group.
    '''

    def __init__(self, fio, parent, name="fio", attrs=None):
        super().__init__(name=name, parent=parent, attrs=attrs)

        for grp,data in zip(("parameters", "data"), read_fio(fio)):
            catGroup = DictDataGroup(parent=self, name=grp, data=data)
            self.add_node(catGroup)            



class H5pyRebaseGroup(ch5.Group):
    ''' Represents a HDF5-like group which is, in fact, an already existing h5py.Group.

    Essentially overrides all `ch5.Group` methods and properties to hand
    all calls over to the h5py node.
    '''

    def __init__(self, h5node, name, parent, attrs=None):
        super().__init__(name=name, parent=parent, attrs=attrs)
        self.h5node = h5node

    @property
    def attrs(self):
        return self.h5node.attrs

    def _is_editable(self):
        return False

    def __setitem__(self, *args):
        return self.h5node.__setitem__(*args)

    def __getitem__(self, *args):
        return self.h5node.__getitem__(*args)

    def __contains__(self, *args):
        return self.h5node.__contains__(*args)

    def __lens__(self):
        return self.h5node.__len__()

    def __iter__(self):
        return self.h5node.__iter__()

    def keys(self):
        return self.h5node.keys()

    def values(self):
        return self.h5node.values()

    def items(self):
        return self.h5node.items()

    def visit(self, *a, **kw):
        return self.h5node.visit(*a, **kw)

    def visititems(self, *a, **kw):
        return self.h5node.visititems(*a, **kw)
        
            
class FioH5Base(ch5.File):
    ''' Bastard HDF5 API fake for the "FIO" data format, e.g. for PETRA3/P08.

    Currently (as of: April 2023) the data format appears to be this:
    
      - A master `.fio` file appearing somewhere on the filesystem, containing
        variables with scalar data, variables with vector data, and some
        "scanning values" a.k.a. positioners. This is an ASCII file with
        a proprietary format, but not terribly complicated to parse.

      - A folder with the same base name as the `.fio` file (only without the
        `.fio` extension), on the same level as the file; it contains one
        or more subdirectories with detector names (e.g. `lambda/`)

      - There appear to be two formats in use for the detector data: HDF5
        or TIFF images.

        For the HDF5 version, Within the subdirectory, one or more `.nxs`
        files (Nexus/HDF5 files) usually containing detector data. Currently,
        the following subfolder structure has been seen in the wild:
        ```
        $ tree .
        .
        ├── m3_2507_00342
        │   └── lambda
        │       └── m3_2507_00342_00000.nxs
        ├── m3_2507_00342.fio
        ├── m3_2507_00744
        │   └── lambda
        │       ├── ct_file_00000.nxs
        │       └── m3_2507_00744_00000.nxs
        └── m3_2507_00744.fio
        ```
        We don't have exact information as to what the `ct_file_00000.nxs` is.
        Also, we don't have exact information as to what the `_00000.nxs`
        trail of the `.nxs` file is.

        For the TIFF files, a subfolder containing TIFF files is available,
        with a name similar, but slightly different from the FIO file
        (can be inferred by parsing the individual FIO constituents).
        For instance:
        ```
        $ tree .
        .
        ├── s1_1161_00484.fio
        └── s1_1161_484
            ├── s1_1161_00484_00000.tif
            ├── s1_1161_00484_00001.tif
            ├── s1_1161_00484_00002.tif
            ...
        ```

    This is the base class containing the FIO information. Subclasses
    `FioH5` and `FioTiff` implement one, respectively the other version
    '''

    def __init__(self, fio, fiogrp=None, h5extra=None):
        ''' Loads FIO (text) file, underlining its data with existing HDF5 data.

        Normally with every `.fio` file comes a directory of the same name, containing
        subdirectories named after a detector, containing HDF5 files of the same
        (or a similar) name.
        This can be overriden, or augmented with other files, using the `h5glob`
        parameter.

        Args:
        
            fio: The `.fio` file path.
        
            fiogrp: The HDF5 group name of the `.fio` file. For uniformity, we
              propose `fio`. But if this is `None`, we're using the FIO base name
              of the file (i.e. the filename only component, without extension).

            h5extra: Python `dict()` with target HDF5 folder as key, and HDF5 file
              paths as values, for HDF5 data files to integrate. If the path
              name does not begin with `/` or `.`, the data path of the current
              FIO file is prepended.      
        '''
        super().__init__()

        # base of the filename (no dirs, no extension)
        self.fio_base = '.'.join(path.basename(fio).split('.')[:-1])

        self.fio_dir = path.abspath(path.dirname(fio))

        if fiogrp is None:
            fiogrp = self.fio_base

        self.fioGroup = FioGroup(fio, name=fiogrp or fio_base, parent=self)
        self.add_node(self.fioGroup)

        dkey = next(iter(self.fioGroup["data"].keys()))
        self.fio_num_frames = len(self.fioGroup["data"][dkey])

        logging.debug(f'{fio} with {self.fio_num_frames} data frames')


class FioH5(FioH5Base):
    ''' Implements a H5-like API for .fio files with detector images in HDF5.

    This uses the `FioH5Base` to initialize a H5-like API for a FIO
    file, then tries to offer a view of the associated HDF5 files
    from within this interface.
    
    Seamlessly integrating HDF5 files ("overlaying" hierachical structures)
    with the parameters of the FIO
    files would be the king's version, but it is tricky for various reasons:
    
      - What do we do on ambiguous parameters? Error and bail out?

      - How do we easily iterate through all the sub-groups? (HDF5 has several
        distinct ways of retrieving subnodes: ["path"]["subpath"], ["path/subpath"],
        and several `.visit...()` functions.)

    We therefore stick to a simpler version for now and bring everything under the
    same HDF5 API hood (a.k.a. `FioH5`), but we don't overlay results. Instead, we
    give each component -- the FIO file for one, and each HDF5 file next -- its
    own node in the root namespace of `FioH5`.
    
    For convenience we're also bein opinionated about the HDF5 layout by default,
    rewarding a `./<basename>/<detector>/<basename><extra>.nxs` layout by
    auto-detecting such files, and automatically integrating them as
    `/<detector><extra>/...` in `FioH5`.

    On top of that, extra HDF5 files need to be integrated by manually specifying
    a key-value map of folder name to file path.

    Usage example:
    
    ```
    In [1]: from nx5d.h5like.petra3 import FioH5
    
    In [2]: fh = FioH5("m3_2507_00744.fio")
    
    In [3]: fh.keys()
    Out[3]: odict_keys(['fio', 'lambda_00001', 'lambda_00002', 'lambda_00000'])
    
    In [4]: fh['fio/data/om'].shape
    Out[4]: (61,)
    
    In [5]: fh['lambda_00000/entry/instrument/detector/data'].shape
    Out[5]: (61, 516, 1554)
    ```

    Usage with the nx5d `ScanReader`:
    
    ```
    In [7]: reader = ScanReader(FioH5, ("/var/home/florin/tmp/Downloads/"
                                        "P08_data/example/raw/m3_2507_00744.fio",))

    In [8]: d1 = reader.read(slice(None), omega="@/fio/data/om",
                       images="@/lambda_00000/entry/instrument/detector/data")
    ...
    ```

    (Note that the example "m3_2507_00744.fio" provided as test data with this package's
    source code does _not_ have a dataset named `data` -- it's called `"mock_data"`
    instead, and has a reduced shape of `"(61, 100, 100)"` for size reasons.)
    '''

    def __init__(self, fio, fiogrp='fio', h5extra=None):
        ''' Loads FIO (text) file, underlining its data with existing HDF5 data.

        Normally with every `.fio` file comes a directory of the same name, containing
        subdirectories named after a detector, containing HDF5 files of the same
        (or a similar) name.
        This can be overriden, or augmented with other files, using the `h5glob`
        parameter.

        Args:
        
            fio: The `.fio` file path.
        
            fiogrp: The HDF5 group name of the `.fio` file. For uniformity, we
              propose `fio`. But if this is `None`, we're using the FIO base name
              of the file (i.e. the filename only component, without extension).

            h5extra: Python `dict()` with target HDF5 folder as key, and HDF5 file
              paths as values, for HDF5 data files to integrate. If the path
              name does not begin with `/` or `.`, the data path of the current
              FIO file is prepended.      
        '''
        super().__init__(fio, fiogrp)

        # base directory of where the current FIO file's HDF5 stuff is located
        self.fio_h5dir = path.join(path.dirname(fio), self.fio_base)        

        # Searching for <base>/<device>/<base><extra>.nxs. This will produce a
        # nested dict(): { 'device': { 'extra': <file path...> } }.
        extra_re = re.compile(self.fio_base+"(.*)[.]nxs")
        devices = {
            path.basename(device) : {
                extra_re.match(path.basename(f)).groups()[0] : f
                for f in glob(path.join(device, self.fio_base+"*.nxs"))
            } 
            for device in glob(path.join(self.fio_h5dir, '*'))
        }

        # This is a flat {<device><extra>: <file path>, ...} map.
        flat_devices = { dev+ext:devices[dev][ext] \
                         for dev in devices \
                         for ext in devices[dev] }
        
        if h5extra is not None:
            devices.update(h5extra)

        # Open the full list of HDF5 files specified as a base.
        self.h5sub = { k:h5py.File(p, 'r') for k,p in flat_devices.items() }
        
        self.h5nodes = { }
        for h5name,h5file in self.h5sub.items():
            node = H5pyRebaseGroup(h5file["/"], name=h5name, parent=self)
            self.add_node(node)
            self.h5nodes[h5name] = node


    def _get(self, name, getlink):
        # Overrides original _get() from silx.io.commonh5.File()
        # to deal with H5pyRebaseGroup(). We essentially
        # end up here when we have a multi-path __getitem__
        # (e.g. self["h5file/entry"], where "h5file" is the rebase
        # group, and "entry" a node within that group.
        
        # Quick n dirty strategy is to just check the first element
        # of "name" against the self.h5sub keys, and just pass the
        # rest on to the subnode, if found.

        paths = name.split('/')
        first = paths[0]
        rest = '/'.join(paths[1:])
        
        if first in self.h5nodes.keys() and len(paths) > 1:
            return self.h5nodes[first].__getitem__(rest)
        else:
            return super()._get(name, getlink)
        

class FioTiff(FioH5Base):
    ''' Loas a FIO file into an HDF5 API and imports TIFF data as detector images.

    NOTE: Uses components from `nx5d.spech5`, and a lot of copy-pasta code.
    Should probably be consolidated at one point.

    Use like this:
    ```
    f = FioTiff('path/to/my_fio_file.fio')
    f['my_fio_file/detector/data'][()]
    ...
    ```

    The Fio-H5 layout, by default, is rougly this:
    ```
      . <fiobase>
      ├── detector
      │    └── data (the TIFF files as a FxNxM dataset)
      ├── data
      │    ├── ...  (angles and other paramters)
      │    ...
      └── parameters
           ├── ...  (fio header parameters0
           ...
    ```
    
    You know the rest of the drill.
    '''
    
    def __init__(self, fiofile, fiogrp=None):
        ''' Loads the FIO file `fiofile` with associated TIFF data.

        The TIFF files will be searched in a subdirectory of the same name,
        under a detector device subfolder
        (i.e. `{basename}/{device}/{basename}_{index}.tif`). but with a slightly

        Args:
        
            fiofile: The FIO file path.

            fiogrp: The HDF5 group name to use for the FIO file. If none
              is specified, the base name of the file (no path, no extension)
              will be used.
        '''
        super().__init__(fiofile, fiogrp)

        tiffpath = path.join(self.fio_dir, self.fio_base, '*')
        devices = [ path.basename(g) for g in glob(tiffpath) ]


        for device in devices:
            tiffPartialFmt = "{fiodir}/{base}/{device}/{base}_{frameidx}.tif".format(**{
                "fiodir": self.fio_dir,
                "base": self.fio_base,    
                "device": device,
                "frameidx": "{frameidx:05d}"
            })

            self._adopt_scan(device, tiffPartialFmt)
            

        self._enter_cnt = 0
        self._enter_data = None


    def __enter__(self, *args, **kwargs):
        '''
        Opening / closing a SpecTiffH5 is pretty expensive. We usually want to
        employ with-guards (enter/exit) when doing that, but the original SpecH5
        does not support "nested" guards (i.e. entering/exitting multiple
        times on the same object).

        This is an extension to do just that. (Need to check if h5py.File supports
        this... the original Python open() / file object definitely does.)
        '''
        if self._enter_cnt == 0:
            self._enter_data = super().__enter__(*args, **kwargs)
        self._enter_cnt += 1
        return self._enter_data


    def __exit__(self, *args, **kwargs):
        if self._enter_cnt > 0:
            self._enter_cnt -= 1
        if self._enter_cnt == 0:
            super().__exit__(*args, **kwargs)


    def _adopt_scan(self, instrumentName, tiffFormat, dataNodeArgs=None):
        # place data inside "instrument/<name>/data"
        parent = self.fioGroup
        
        parent.add_node(H5Group(parent=parent, name=instrumentName,
                              attrs={'NX_class': 'NXinstrument'} ))
        instrObj = parent[instrumentName]

        instrObj.add_node(SpecH5LazyTiffNode(tiffPathFmt=tiffFormat,
                                             numFrames=self.fio_num_frames,
                                             name="data",
                                             parent=parent,
                                             **(dataNodeArgs or {})))
