#!/usr/bin/python3

from pandas import MultiIndex
from xarray import Dataset, Coordinates
from dask import array as da

import nx5d.h5like.h5pickle as h5py

'''
Experiment geometry defintion dictionary as needed by `LazyQMap`.
Strongly influenced by typical `xrayutilities` API. This was 
the correct geometry at one point in time (for proposal 3381/Bargheer
in April 2023), but might have changed for *your* experiment.
'''
ExperimentTemplate = {
    "goniometerAxes": {'omega': 'y-', 'chi': 'z+', 'phi': 'x+'},
    "detectorAxes": {'twotheta': "y-"},

    "imageAxes": ("y-", "x+"),
    "imageSize": "$/detector_size",
    "imageCenter": "$/detector_centre",

    # same unit as imageChannelSize
    "imageDistance": "@/sdd",

    # same unit as imageDistance (mm)    
    "imageChannelSize": ("@/pixel_size", "@/pixel_size"),

    "imageSize": "@/detector_size",

    'sampleFaceUp': 'x-',

    'beamDirection': (0, 0, 1),
    'sampleNormal': (1, 0, 0),

    "beamEnergy": "@/photon_energy",
}

'''
Template for loading of angle data from DAMNIT HDF5 files
'''
DmnAnglesTemplate = {
    'goniometerAngles': {'omega': '@/omega', 'chi': '@/chi', 'phi': '@/phi'},
    'detectorTARAngles': {'twotheta': '@/twotheta', }
}

'''
Template for loading if detector (image) data form DAMNIT HDF5 files.
ACHTUNG, these are typically still giant amounts of data (10k+ images).
Loading these as a numpy array from HDF5 is a BadIdea(tm). Typically,
you'd want to reference them as Dask arrays and apply some further
reduction before holding them in memory.

See `dmn_load_dataset()` as an entry point to a better workflow.
'''
DmnImagesTemplate = {
    'images': "@/images"
}

def dmn_load_dataset(h5like, *small_keys, index_keys=None, **large_keys):
    ''' Loads a DAMNIT-like HDF5 file into an xarray dataset.
    
    DAMNIT-like HDF5 files have a flat structure with (essentially) flat structure,
    where each data set has the same length N and data only differs in additional
    dimensions (i.e. angular data and/or other metadata being essentially
    1-dimensional arrays of length N, while detector images are huge 3D datasets
    with NxWxH items).
    
    The first dimention is either indexed by a numerical sequence (defaults to
    `range(N)`), or by more complex `pandas.MultiIndex` structures. If it needs
    to be a multi-index, then the data keys which make up the multi-index
    can be specified.
    
    The `small_keys`, i.e. 1-dimensional data, is typically referenced directly,
    to be fully loaded into memory.
    
    The `large_keys`, i.e. multi-dimensional data which potentially busts memory
    limits, is loaded as `dask` arrays, and needs to be specified with either a
    3-tuple reprenting the Dask chunking, or at least an integer parameter
    specifying the chunking along the 1st ("index") axis. If it's the latter,
    chunking along the other two dimensions is taken from the dataset's `.shape`
    (i.e. no chuking is performed along higher dimensions).
    
    Args:
    
        h5like: HDF5-like object to read data from; it's expected to be either
          a `h5py.File()` object or a node.
        
        *small_keys: each additional positonal parameter is expected to be a
          string, denoting a dataset to load the "default way" (i.e. will
          ultimately end up as an numpy array, fully into RAM).
        
        index_keys: list or tuple of strings which make up the first dimension
          index. Default (`None`) will lead to creating of an integer counter
          as index.
          
        dmetric_keys: list with detector metric datasets (obsolete?)
            
        **large_keys: each additional named parameter is interpreted to designate
          a dataset (as key) which is to be referenced lazily (e.g. as a Dask
          array). The value represents chunking -- a single integer uses that
          chunk size in the first dimension and reuses the full length in all other
          dimensions, and a tuple is used as a full chuking specification for
          `dask.array.from_array(..., chunks=...)`.
          
    Returns: an `xarray.Dataset` with the requested data.
    '''
    
    if index_keys is not None:
        mindex_obj = MultiIndex.from_arrays([h5like[k] for k in index_keys],
                                            names=tuple([k for k in index_keys]))
        coords = Coordinates.from_pandas_multiindex(mindex_obj, 'index')        
    else:
        index = range()
        coords = {'index': index}
            
    data_vars = {}
    
    # This is the data we'll reference directly in the h5like dataset.
    # It'll eventually end up as numpy arrays (i.e. fully in memory)
    for k in small_keys:
        data = h5like[k]
        sh = h5like[k].shape
        data_coords = ['index'] + [f"{k}_{i}" for i in range(1,len(sh))]
        data_vars[k] = (data_coords, data)
        
    # This is the data we'll reference only as dask arrays.
    # The value to the keys are chunking information.
    for k,chk in large_keys.items():
        sh = h5like[k].shape
        data_coords = ['index'] + [f"{k}_{i}" for i in range(1,len(sh))]
        if hasattr(chk, "__getitem__"):
            chunks = chk
        else:
            # take chk as chunking along the 1st dimension, and keep all
            # the other dimensions as they are
            chunks = tuple([int(chk)] + [*sh[1:]])
        data = da.from_array(h5like[k], chunks=chunks)
        data_vars[k] = (data_coords, data)
    
    return Dataset(data_vars=data_vars, coords=coords)
