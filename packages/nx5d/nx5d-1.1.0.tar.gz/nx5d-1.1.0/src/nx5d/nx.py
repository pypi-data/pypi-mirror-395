#!/usr/bin/python3

'''
This module contains code to export various data formats
parsed by EDFnx (EDF format, Runlog format, ...) to HDF5/Nexus
files.
'''

from nx5d import runlog

import h5py
import numpy
import re
import fabio
from os import path

def _np2nx_type(np_type):
    '''
    Returns a HDF5 data type string, given a numpy type.
    '''
    if 'U' == np_type.kind:
        return numpy.dtype(np_type.str.replace('U', 'S'))
    else:
        return np_type
    

def _c2n_require_group(h5root, h5path, autodefault=True):
    '''
    copy2nexus helper - calculates a HRD5 path and creates
    the corresponding Nexus group(s). Returns a h5py HDF group object.
    Parameters:
      - `h5root`: Top level object, owner of the group, relative starting
        point for `h5path`.
      - `h5path`: String path description, possibly with Nexus
        group types.
      - `autodefault`: If set to `True`, each level receives a
        "@default" HDF5 attribute for the subsequent path element
        (Nexus standard).
    '''
    pathchain = []
    for i in h5path.split('/'):
        pathchain.append(list(i.split(':')))

    for pair in pathchain:
        if len(pair) == 1 and len(pair[0]) > 0:
            pair.append("NXentry" if pair != pathchain[-1] else "NXdata")
    
    base = h5root
    sub = None

    # The 1st element in the pathchain will be an empty string if
    # the path starts with '/'. Need to jump that.
    for d in (pathchain if len(pathchain[0][0]) > 0 else pathchain[1:]):
        sub = base.require_group(d[0])
        if 'NX_class' not in sub.attrs.keys():
            sub.attrs['NX_class'] = d[1]
        if 'default' not in base.attrs.keys() and autodefault:
            base.attrs['default'] = d[0]
        base = sub

    # full path: "/".join([i[0] for i in pathchain])
    # pathchain: pathchain

    return sub or base


def copy2nexus(dataobj, h5obj=None, h5group=None,
               h5path='/entry:NXentry/data:NXdata',
               nxsignal='auto',
               nxaxes='auto',
               nxautodefault=True,
               typeConverter=_np2nx_type):
    '''
    Takes an EDFnx data object (`dataobj`) and inserts it into a
    Nexus-compliant HDF5 file.

    The HDF5 file, and position (path) therein of the new data, can
    be specified in two ways:
      - either by specifying a HDF5 file object (via `h5obj`),
        and optionally an (absolute) path therein,
      - or by specifying a HDF5 group (via `h5group`), and
        optionally a (relative) path therein.

    The parameters are as follows:
      - `dataobj`: The EDFnx data object.
      - `h5obj`: The HDF5 object to contain the data. Default is `None`,
        but either this or `h5group` must be specified. If both are
        specified, this consists an ambiguity and an exception is raised.
      - `h5group`: The HDF5 object to contain the data. Default is `None`,
        see `h5obj` for details.
      - `h5path`: Path within the HDF5 file to contain the data. The format
        of the path is `[/]group[:type][/subgroup[:subtype]][/...]`. `type`
        is typically one of the
        [Nexus group classes](https://manual.nexusformat.org/classes/index.html#all-class-definitions).
        The leading `/` is optional when `h5obj` is set. If the class is not
        specified for a particular group path component, all groups are
        assumed to be `NXentry`, except for the last one, which is `NXdata`.
        If the group already exists, it's not being created.
      - `nxsignal`: The default data signal column; this is set as the default
        of the corresponding NXdata group. Special options include `None`
        (i.e. don't set the default), or 'auto' (the default), meaning
        that the algorithm will choose one by some meaningless heuristic.
      - `nxaxes`: Similar to `nxsignal`, but will set the axis instead of the
        signal attribute.
      - `nxautodefault`: Auto-sets the default descendency path (Nexus lango:
        `"@default"` attribute) for every path element.
      - `typeConverter`: This is a function that takes a `numpy.dtype` as an
        argument and returns another `numpy.dtype`. It is used to transform
        data types (mostly strings) since the HDF5 format chokes on specific
        kinds of data (e.g. unicode strings).
    '''

    grp = _c2n_require_group(h5group if h5group is not None else h5obj,
                             h5path, autodefault=nxautodefault)

    for k in dataobj.attrs.keys():
        grp.attrs[k] = dataobj.attrs[k]


    # Handle explicit nxsignal/nxaxes.
    # We don't check whether the columns really exist.
    if nxsignal not in [None, 'auto']:
        grp.attrs['signal'] = nxsignal
    if nxaxes not in [None, 'auto']:
        grp.attrs['axes'] = nxaxes
        
    for dname in dataobj.keys():
        
        a = dataobj[dname]
        dtype = typeConverter(a.dtype)
        
        grp.require_dataset(name=dname, data=a.astype(dtype), shape=a.shape, dtype=dtype)

        # Handle nxaxes/nxsignal as the 1st, respectively 2nd unused
        # floating-point data type.
        if a.dtype == numpy.dtype(float):
            if 'axes' not in grp.attrs.keys() and nxaxes == 'auto' and nxsignal != dname:
                grp.attrs['axes'] = dname
            elif 'signal' not in grp.attrs.keys() and nxsignal == 'auto' and nxaxes != dname:
                grp.attrs['signal'] = dname

                

def test_c2n_reqgroup():

    # The Nexus standard expects to have at least one NXentry-class folder,
    # with at least one NXdata-class subfolder. Obviously, some of these
    # paths make this impossible. 
    for p in [ "/entry/through/the/gates/of/hell",
               "/entry:NXentry/through:NXentry/the/gates/of/hell:NXdata",
               "entry/through/the/gates/of/hell",
               "",
               "foo/bar",
               "foo" ]:
        
        h5 = h5py.File('jinkies', driver='core', backing_store=False, mode='w')
        grp = _c2n_require_group(h5, p)
        
        assert grp.parent is not None
        
        # For easier testing, longer paths all have the same form (see above)
        if len(grp.name) > 10:
            assert grp.name == "/entry/through/the/gates/of/hell"

        # For paths with insufficient subgroups, the NX_class attribute
        # is botched up. Make sure we don't test that in those cases.
        if grp.name != '/':
            assert grp.attrs["NX_class"] == "NXdata"
        if grp.parent.name != '/':            
            assert grp.parent.attrs["NX_class"] == "NXentry"
            
        h5.close()
    
    
def test_c2n_runlog():
    '''
    Tests the generation of a HDF5/Nexus file.
    This doesn't actually validate the Nexus file itself (as this
    depends a lot on the nx* parameters within the `make_nexus()`
    function call). It just makes sure the code runs and essentially
    contains the data as expected
    '''

    r = runlog.RunlogFile("./test_data/run105.log")
    h5 = h5py.File('jinkies', driver='core', backing_store=False, mode='w')
    
    copy2nexus(r, h5obj=h5)

    h5data = h5["/entry/data"]
        
    for k in r.keys():
        assert h5data[k].shape == r[k].shape

    for k in r.attrs.keys():
        assert r.attrs[k] == h5data.attrs[k]


def zip2nexus(logobj, dirbase,
              h5obj=None,
              h5pathfmt_data='/scan-{__scan__:04}:NXentry/data:NXdata',
              h5pathfmt_vars='/scan-{__scan__:04}:NXentry/vars:NXinstrument',
              scanFormatter=lambda d: int(d["__index__"])+1,
              datapathFormatter=lambda d: u'%s.edf' % d["file"],
              datanameFormatter=lambda d: u'edfmap',
              typeConverter=_np2nx_type):
    '''
    Takes a RunlogFile object (or any EDFnx compatible) and integrates all
    the corresponding external data, and the Logfile data lines, into
    the specified HDF5/Nexus target (via `h5obj` and `h5pathfmt`).

    The ideas behind this are the following assumption:
    
      - The "real" experimental data is not contained within
        the Logfile (i.e. `logobj`) but in external files
        (e.g. EDF or TIFF files)
    
      - A "logfile" is actually only an experimental summary, holding
        named instrumental parameters; the data column (names) within a
        Logfile are just keys for named parameters, and each line
        within the data vectors represent setup values for one specific
        scan of the experiment.

    Following this, `zip2nexus` goes through each data line and loads
    the corresponding external data, saving it into the HDF5 object
    at its specific place. The metadata as specified by the columns
    of the data line are stored, together with the external data,
    as attributes of that specific NDF5 subgroup.

    Parameters:
    
      - `logobj`: Logfile data object, e.g. a `RunlogFile()` instance

      - `dirbase`: The base path (i.e. path without the file name component)
        of the file on which `logobj` is based. This is used as the base
        path for the `datapathFormatter`.

      - `h5obj`: HDF5 object that will be the root of the newly injected
        data. It may contain other data. It is expected to implement
        a `h5py` compatible interface to handle datasets and subgroups
        (i.e. `require_dataset()`, respectively `require_group()`)

      - `h5pathfmt_scan`: Path name template for the scan top folder,
        relative to the root of `h5obj`.
        The scan number will be inserted at the position of the `{__scan__}`
        parameter. All the header keys of the `RunlogFile` keys are also
        available as parameters, aswell as `{__index__}`, the iteration
        index of the data lines starting with 0.
        Default is `/scan-{__scan__}:NXentry`.

      - `h5pathfmt_data`: Template for the data folder, relative to the
        `h5obj` root. Same variables as for `h5pathfmt_scan`
        are available, default is `/scan-{__scan__}:NXentry/data:NXdata`.

      - `h5pathfmt_vars`: Template for the instrumental setup variables
        folder, relative to the root of `h5obj`.
        Same variables as for `h5pathfmt_scan`
        are available, default is `/scan-{__scan__}:NXentry/vars:NXinstrument`.

      - `scanFormatter`: This is a function receiving a dictionary as input
        (all columns of the `logobj` data, with the values of the
        corresponding data line as data, and `__index__` as the line index)
        and expected to output a numerical scan key (e.g. int(5) for the
        5th scan).

      - `datapathFormatter`: This is a function receiving a dictionary as input
        (all columns of the `logobj` data, with the values of the
        corresponding data line as data, and `__index__` as the line index,
        and `__scan__` as the scan key) and expected to output a file path
        relative to the folder of the logfile, as string.

      - `datanameFormatter`: This is a function receiving a dictionary as input
        (all columns of the `logobj` data, with the values of the
        corresponding data line as data, and `__index__` as the line index,
        and `__scan__` as the scan key) and expected to output a name for
        the dataset.

      - `typeConverter`: This is a function that takes a `numpy.dtype` as an
        argument and returns another `numpy.dtype`. It is used to transform
        data types (mostly strings) since the HDF5 format chokes on specific
        kinds of data (e.g. unicode strings).
    '''

    header = logobj.keys()
    
    for index, line in enumerate(zip(*(logobj.values()))):
        values = {k: v for (k,v) in zip(header, line) }
        values['__index__'] = index
        values['__scan__'] = scanFormatter(values)

        # Saving the data.
        datapath = datapathFormatter(values)
        name     = datanameFormatter(values)
        
        fab = fabio.open(path.join(dirbase, datapath))
        
        h5datagrp = _c2n_require_group(h5obj, h5pathfmt_data.format(**values))
        h5data = h5datagrp.require_dataset(name=name,
                                           data=fab.data,
                                           shape=fab.data.shape,
                                           dtype=fab.data.dtype)
        h5datagrp.attrs["signal"] = str(name)
        h5datagrp.attrs["axes"] = [ ".", "." ]
        
        h5varsgrp = _c2n_require_group(h5obj, h5pathfmt_vars.format(**values),
                                       autodefault=False)

        # Copying EDF file metadata into the HDF5 data folder. For
        # conveninence, trying to guess some of the field types
        # (int and float). Everything else stays 
        for (k,v) in fab.header.items():

            final_v = v
            try:
                final_v = int(v)
            except ValueError:
                try:
                    final_v = float(v)
                except ValueError:
                    final_v = v

            old_type = type(final_v)
            old_dtype = numpy.dtype(old_type)
            new_dtype = typeConverter(old_dtype)
            new_type = new_dtype.type                    
            data_array = numpy.array([final_v], dtype=new_dtype)

            try:
                existent = h5datagrp[k]
                if existent.shape != data_array.shape:
                    raise RuntimeError("Request to update key %s be updated with "
                                       "incompatible data %r" % (k, data_array))
                    
                existent[:] = data_array[:]
            except KeyError:
                h5datagrp.create_dataset(name=k, data=data_array)
                

        # Saving the runlog metadata
        for k,v in values.items():
            if k in [ '__index__', '__scan__' ]:
                continue

            # Nexus/HDF5 has problems with u'' strings. Recycling
            # the typeConverter(), which works from/to numpy.dtype().
            # Yes, this could be a oneliner, but breaking it down makes
            # it easier to understand.
            old_type = type(v)
            old_dtype = numpy.dtype(old_type)
            new_dtype = typeConverter(old_dtype)
            new_type = new_dtype.type
            data_array = numpy.array([v], dtype=new_dtype)

            try:
                existent = h5varsgrp[k]
            except KeyError:
                h5varsgrp.create_dataset(name=k, data=data_array)
        
    

def test_z2n_runlog():
    '''
    Tests the `zip2nexus()` function on `RunlogFile` data.
    '''

    rlog = runlog.RunlogFile("./test_data/short_run04.log")
    h5 = h5py.File('jinkies', driver='core', backing_store=False, mode='w')

    # Need to change the datapathFormatter here because the logfile+edf
    # combination in this particular example is actually a scam (we
    # removed all the actual data from EDF files and replaced it with
    # a 10x10 numpy array of undefined data).
    zip2nexus(rlog, "./test_data", h5,
              datapathFormatter=lambda d: "short_%s.edf" % d["file"])


    no_scans = 0
    for i in rlog.values():
        no_scans = len(i)

    # Just a quick n dirty test if the number of data files pans out.
    assert no_scans == len(h5.keys())

    # (If we've made it this far, then at least the test didn't raise
    # any exceptions :-)
    #
    # Feel free to add more assertions and/or tests as you find more
    # corner cases to be handled.
    

if __name__ == "__main__":

    from sys import argv
    from os import path
    from sys import exit

    if len(argv) < 3:
        print ("Usage: %s <logfile> <hdf5file>" % argv[0])
        exit (-1)

    rlog = runlog.RunlogFile(argv[1])
    h5 = h5py.File(argv[2], mode='a')

    zip2nexus(rlog, path.dirname(argv[1]), h5)

    h5.close()
