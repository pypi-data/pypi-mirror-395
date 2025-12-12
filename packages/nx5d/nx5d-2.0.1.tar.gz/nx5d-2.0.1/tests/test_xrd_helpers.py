#!/usr/bin/python3

from nx5d.xrd.xrd_helpers import *
import pytest

import numpy as np
from xarray import DataArray

def test_stdwidth1d_ndarray(test_ndarray):
    '''
    Test for stdwidth()
    '''

    center = (np.array(test_ndarray.shape)/2).astype(int)
    
    v = stdwidth1d(test_ndarray, center)

    # We're measuring the variance ("width") with regards to the
    # actual center of the data patch, so this should always essentially
    # be smaller than half the field.
    # This being random data, it *should* have a width larger than 1
    # grid point, though...
    assert (v <= np.abs(center.max()))
    assert (v >= 1.0)

    
def test_stdwidth1d_xarray(test_xarray):
    '''
    Test for stdwidth()
    '''

    # alias
    dta = test_xarray

    center = [ (x, dta.coords[x].values[0]+(dta.coords[x].values[-1]-dta.coords[x].values[0])/2 ) \
                     for x in test_xarray.dims ]
    
    v = stdwidth1d(test_xarray, center=dict(center))

    # We're measuring the variance ("width") with regards to the
    # actual center of the data patch, so this should always essentially
    # be smaller than the field.
    c_coord = np.array([dta.coords[x].values[-1]-dta.coords[x].values[0] for x in dta.dims])
    assert (v <= np.abs(c_coord.max()))


    
@pytest.fixture
def test_ndarray():
    ''' Returns a an ndarray of variable size and shape (i.e. dimensions) '''

    ## ...up to 7 dimensions should prove the point.
    ## Configurable for debugging.
    
    min_dims = 2
    max_dims = 2 #7

    min_size = 2
    max_size = 10 #20
    
    dims = min_dims + int(np.random.random() * (max_dims-min_dims))
    shp  = min_size + (np.random.random(dims) * (max_size-min_size)).astype(int)
    return np.array(np.random.random(shp.prod())).reshape(shp)


@pytest.fixture
def test_ndcenter(test_ndarray):
    ''' Returns a random 'center' coordinate that lies within the array '''
    return (np.random.random(len(test_ndarray.shape)) * test_ndarray.shape).astype(int)
    

def test_sqdist_ndarray(test_ndarray, test_ndcenter):
    '''
    Tests sqdistance() on an ndarray (i.e. no named axes)
    '''
    
    assert ((test_ndcenter < test_ndarray.shape).all())
    
    sqd1 = sqdistance(center=test_ndcenter, shape=test_ndarray.shape)
    
    axlist = tuple([range(s) for s in test_ndarray.shape])
    sqd2 = sqdistance(*axlist, center=test_ndcenter)

    # No distance can be longer than the diagonal across all dimensions
    assert (sqd1.max() <= (np.array(test_ndarray.shape)**2).sum())
    assert (sqd2.max() <= (np.array(test_ndarray.shape)**2).sum())
    
    # The square distance result has exactly one point for every input point
    assert (sqd1.shape == test_ndarray.shape)
    assert (sqd2.shape == test_ndarray.shape)
    
    assert ((sqd1[tuple(test_ndcenter)] == sqd2[tuple(test_ndcenter)]).all())
    
    # Distance at center is always zero
    assert((sqd1[tuple(test_ndcenter)] == 0).all())
    assert((sqd2[tuple(test_ndcenter)] == 0).all())
                                                                      
                                                                      
def test_sqdist_ndtuple(test_ndarray, test_ndcenter):
    '''
    Test whether sqtistance() accepts tuples as arguments
    '''
    axlist = tuple([range(s) for s in test_ndarray.shape])
    sqd = sqdistance(*axlist, center=tuple(test_ndcenter))
    assert (sqd.shape == test_ndarray.shape)
                                                                      
                                                                      
@pytest.fixture
def test_xarray(test_ndarray):
    ''' Creates an `xarray` with named axes based on a random ndarray '''
    
    axis_names = ['physics', 'trustee', 'warning', 'ethnic',
                  'tree', 'text', 'contraction', 'shell' ]
    
    return DataArray(data=test_ndarray,
                     coords=[np.array(range(s))*0.1-(s/20) for s in test_ndarray.shape],
                     dims=axis_names[:len(test_ndarray.shape)])
    

@pytest.fixture
def test_xcenter(test_xarray):
    '''
    Generates a random single-point center coordinate based on an
    array with named axes. The coordinate tuple has named dimensions.
    '''
    
    pos = {}
    for d in test_xarray.dims:
        ax = test_xarray.coords[d].values
        r = np.random.random()
        c = ax[0] + r*(ax[-1]-ax[0])
        pos[d] = float(c)

    return pos


def test_sqdist_xarray(test_xarray, test_xcenter):
    '''
    Tests the sqdistance() function with xarray-like named axes.
    '''
        
    ## This is for more specific testing / debugging.
    #shape  = (5, 5)
    #data   = np.ones(shape)
    #axes   = [(np.array(range(s))-s/2)*0.1 for s in shape]
    #center = {'x': 0, 'y': 0 }
    #xdata  = DataArray (data=data, coords=axes, dims=['x', 'y'])
    
    center = test_xcenter
    xdata  = test_xarray
    
    sqd = sqdistance(*xdata.coords.items(), center=center)
    
    assert (sqd.max() <= (np.array(xdata.shape)**2).sum())
    
    # The square distance result has exactly one point for every input point
    assert (sqd.shape == xdata.shape)
    
    # Calculate distance (N-dim diagonal) between two ajacent axis coordinates.
    # This will give us a very crude estimate of an error measure which is
    # (1) smaller than a pixel, but
    # (2) still large enough such that an interpolation of the array value
    # at that specfic point will still fit well within that error value.
    
    pix_diag = np.sqrt(np.array([ (x[1].values[1]-x[1].values[0])**2 for x in xdata.coords.items() ]).sum())
    maxerr = pix_diag*0.5 / len(xdata.shape)
    
    #print ("### distances:\n", np.sqrt(sqd.values))
    #print ('### pixdiag:', pix_diag)
    #print ('### maxerr:', maxerr)
    #print ('### value(s) at center:', sqd.interp(center).values)
    #print ('### center coordinates:', center)
        
    # Distance at center is always zero
    assert( (sqd.interp(center) < maxerr).all())

    # Make sure sqdistance() accepts a list of tuples as center coordinates
    sqd2 = sqdistance(*xdata.coords.items(), center=center.items())
    assert ((sqd2 == sqd).all())

    # Make sure sqdistance() accepts a dict() center coordinates
    sqd3 = sqdistance(*xdata.coords.items(), center=dict(center.items()))
    assert ((sqd3 == sqd).all())

    # Make sure sqdistance() accepts a list of tuples as axes
    #sqd3 = sqdistance(*tuple( [(d,xdata.coords[d]) for d in xdata.dims] ),
    #                  center=center)
    #assert ((sqd2 == sqd3).all())
