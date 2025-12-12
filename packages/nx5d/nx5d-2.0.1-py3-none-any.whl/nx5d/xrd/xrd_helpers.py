#!/usr/bin/python3

from scipy import ndimage
import numpy as np
from xarray import DataArray
import logging

logger = logging.getLogger(__name__)

__all__ = [ "series_cntrmass", "sqdistance",  "stdwidth1d", "series_stdwidth1d" ]

'''
Helpers for X-ray diffraction data analysis
'''

def series_cntrmass(data, series=None):
    ''' Calculates N-1 dimensional center of mass for an N-dimensional array.

    Args:
    
        data: This is expected to be an `xarray` with at least 2
           named dimensions, or a list of N-dimensional arrays.

        series: If `data` is an `xarray`, this is expected to be a string
           naming the axis along which to break data apart and form
           a series of.
           
           If data is a `numpy` array or a regular (nested) list,
           `series` is expected to be an axis index.
           
           If data is an iterable (e.g. a list of arrays), then `series`
           must remain `None`, and the `data` iterable already defines
           the series.

           In all cases, if `series=None` (the default), the center of
           mass series will be built along the 1st dimension.
    
    Returns: a 2D `xarray.DataArray`. The first dimension has the same length as the
        length of the series (i.e. the length of the `series` dimension).
        The 2nd dimension hs a length of N-1, where N is the number of dimensions
        of the original data series.
        Each entry being an N-1 dimensional coordinate of the center of mass in 
        the respective plane.
    '''
    
    
    # The difficult part is going to be that ndimage's center_of_mass()
    # returns a fractional (!) positional (!!) index, i.e. one that's
    # related to the position.
    
    # Push the dimension we want to keep to the begging (that's
    # apparently the only one we can iterate over)
    if series is not None:
        view = data.transpose(series, ...)
    else:
        view = data
        
    index_list = []

    if hasattr(view, 'dims'):
        # ...if input is a single DataArray
        
        if len(view.shape) <= 1:
            raise RuntimeError(f'Input data must be a sequence of datasets (i.e. multiple arrays),'
                               f' or a multi-dimensional array.')
        
        other_axes = [o for o in view.dims[1:]]
    else:
        # ...if input series is actually a list of (1D) datasets
        other_axes = list(next(iter(data)).dims)

    
    ## iterate along `axis` and collect all the COMs in index_list
    for img in view:
        try:
            com = ndimage.measurements.center_of_mass(img.data)
            ci  = np.floor(com).astype(int)
            cf  = com-ci
        except ValueError as e:
            # All-zero datasets produce errors (there's no useful definition
            # of a COM on an all-zero dataset). It's the upper layer's responsibility
            # to fix this, but we want to give the user a little bit more information
            # to go on.
            logging.error(f'Error: {str(e)}: this is probably because you have all-zero datasets')
            raise
        
        # iterate over each COM coordinate of the N-1 dim 
        #index = [ view.coords[c].values[i] + f*(img.coords[c].values[i+1]-img.coords[c].values[i])
        #             for c,i,f in zip(other_axes, ci, cf) ]

        index = [ img.coords[c].values[i] + f*(img.coords[c].values[i+1]-img.coords[c].values[i])
                     for c,i,f in zip(other_axes, ci, cf) ]
        
        index_list.append(index)

    # We return a 2D DataArray. In the first dimension, we have one entry
    # for each of the COM sets. We're naming this as the original axis
    # was named (if 'series' is defined), or simply 'plane' if the data sets
    # were passed on as a list.
    # The 2nd dimension is a string list of all the other dimension names
    # (so that we know how to attribute the COM components).
    
    if series is not None:
        series_coords = view.coords[series].values
        series_dim = series
    else:
        series_coords = [i for i in range(len(view))]
        series_dim = 'plane'
        
    coords = {
        series_dim: series_coords,
        'axis': other_axes
    }
        
    return DataArray(data=index_list, coords=coords)


def sqdistance(*axes, center, shape=None):
    '''
    Takes a list of axes and a location desginated `center` and returns
    a N-dimensional array with all the squared distances from `center`
    to each of the points. The array dimensions are assumed to be
    equivalent in size.
    
    Parameters:
    
      - `*axes`: Axis objects, one per parameter. One axis object
        can either be an `xarray` coordinates tuple `(dim, values)`
        with `dim` as a string identifyer and `values` as the axis
        values; or they can be plain iterables (regular `numpy` 1D
        arrays or lists).
        
      - `center`: needs to be 1-dimensional vector with N values,
        if `axes` items are regular `numpy` arrays or iterables.
        Otherwise 
        It represents the point relative to which the squared distance
        of all other points is calculated.
        Despite its name it does not need to be, and typically is
        not, the actual center of the field.
        
      - `shape`: Instead of explicitly specifying a list of axes,
        a single vector continaing an N-dimensional array shape
        can also be specified. In that case, the axes will be
        constructed as regular indices ranging from `0` to `len(shape[n])`
        
    Returns: N-dimensional array of size `len(axes[0]) * len(axes[1]) * ... * len(axes[n])`
    contraining the squared distance to `center` for each point.
    '''
        
    if (not axes or len(axes) == 0) and shape is not None:
        # numpy array style shape. We don't actually have axis
        # values, we need to build them first. `center` is a
        # 1D-array (one coordinate per axis) we can juse for
        # indexing.
        axvalues = [[i for i in range(s)] for s in shape] 
        cvalues = tuple(center)
        return_numpy = True
        
    elif isinstance(axes[0], tuple) and len(axes[0]) == 2 and isinstance(axes[0][0], str):
        # Named axes, `xarray` or `pandas` style. Each axis element
        # is either one `xarray` Axis object (with values in the .values
        # property) or a (name, values) axis tuple.
        # `center` is either a dict, or a list of (key, val) tuples.
        axvalues =  [ (x[1].values if hasattr(x[1], "values") else x[1])   for x in axes]
        cobj = dict(center)
        cvalues = tuple([cobj[x[0]] for x in axes])
        return_numpy = False
        
    else:
        # numpy array, explicit axes. Each axis is a 1D-iterable
        # and `center` is a 1D-tuple (one coordinate per axis).
        axvalues = axes
        cvalues = center
        return_numpy = True
    
    sqdist = np.abs(axvalues[0] - cvalues[0])**2
    for ax,c in zip(axvalues[1:], cvalues[1:]):
        sqdist = sqdist[...,None]
        sqdist = sqdist + np.ones(sqdist.shape) * (ax-c)**2
    
    if return_numpy:
        return sqdist
    
    return DataArray(data=sqdist, coords=[(x[0], x[1].values) for x in axes])
    
    
def stdwidth1d(data, center):
    ''' Calculates the standard deviation a.k.a. "peak width".

    This is defined as the square-root of the
    [variance](https://en.wikipedia.org/wiki/Variance#Discrete_random_variable)
    of an experimental data array with respect to the value located in the
    same array at index position called `center`.

    For 1-dimensional arrays of discrete points, the variance is essentially
    defined as `(Xi-M)**2`, i.e. the squared sum of the differences of the
    poins `Xi` from a mean value `M`. It's a measure of how much each
    value differs from the mean.

    For N-dimensional data, the statistical reasoning is more complex and
    evolves around [the covariance matrix](https://en.wikipedia.org/wiki/Covariance_matrix).
    This function does *not* implement the covariance matrix version
    (serach for `stdvariance()` instead), but only the simple 1D version.
    If fed with a multiple N-dimensional input, it *still* only calculates
    one variance, which can essentially be interpreted as an "average variance"
    along all dimensions.
    
    Args:
    
        data: The data for which to calculate the standard width.
          This can either be:
            - an N-dimensional `numpy` array
            - an N-dimensinonal `xarray.DataArray`
        
        center: The center of mass relative to which to calculate the
          deviation. This can be:
    
            - an N-tuple capable of indexing `data`. This is expected,
              if `data` is an numpy array.

            - a dictionary with dimension names as keys, and positions
              (coordinate lists/arrays) as values, or...

            - ...a single `(dim, value)` tuple, or...

            - ...an `xarray.DataArray` with positions / center-of-mass
              coordinates.
      
    Returns: One single value, represending the sum of suqare distances
    weighted by the function value at the respective place, if
    `axis=None`. If `axis` is specified, then the result will be a
    1-dimensional array containing standard widths along `axis`.
    '''
    
    # Preparing the coordinate axis array of `data' -- for an xarray
    # we just build (name, values) tuples of its dims; for numy arrays,
    # we generate an integer index corresponding to the length.
    if hasattr(data, "coords"):
        axes = [(d, data.coords[d]) for d in data.dims]
    else:
        axes = [range(i) for i in data.shape]
        
    pos = center
        
    sqdist = sqdistance(*axes, center=pos)
    sqvar  = (sqdist * data / data.sum()).sum()
    
    return np.sqrt(sqvar)


def series_stdwidth1d(data, center, axis=0):
    '''
    Wrapper for `stdwidth1()` to act on a collection of data sets at once.
    #
    '''
    pass
