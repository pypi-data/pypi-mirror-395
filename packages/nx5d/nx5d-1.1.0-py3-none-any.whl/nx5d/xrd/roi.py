#!/usr/bin/python3

import numpy as np

'''
Helps working with N-dimensional region of interests (ROIs) in data.
'''

class Roi:
    '''
    Roi represents a region of interest in N dimensions.
    It can be initialized in a variety of ways:
      - By explicitly specifying start and end points
      - By specifying a start point and the extent
      - By specifying a center and an extent
    Once set up, slicers can be generated that select the
    corresponding data points from each dimension of an
    N-dimensional array.
    '''
    
    def __init__(self, start=None, size=None, center=None, end=None,
                 itype=None, dims=None):
        '''
        Initializes the ROI. Each of the parameters can be iterables
        (arrays, lists, tuples) or scalars. All have to have the
        same dimension and type.
        
        The ROI coordinates can be integers (default) or other types,
        e.g. floating point numbers. The slicers that are returned
        by the `Roi.s` property will have a matching type.
        
        Parameters:
        
          - `start`: The start point (or corner) of the ROI.
          
          - `center`: As an alternative to `start`, the center point
            of an ROI can be specified with this parameter.
          
          - `end`: This represents end point (or corner) of the ROI,
            if the start point is known.
          
          - `size`: This is the extent of the ROI. If `start` was
            specified, the ROI extends to `start+size`. Size can
            be negative, in which case the end point will be before
            start. If on the other hand `center` was specified,
            then `size` is just the total extent of the ROI. Then
            the sign of `size` is ignored, only its magnitude in
            every direction is used.
            
          - `itype`: The data type (`numpy` lingo `dtype`) of the
            index values. The outgoing slicers are going to be
            of the same value. If it is `None` (default), the
            type of the input data is matched.
            
          - `dims`: If specified, it's the name of the
            dimensions. If available, the `Roi.ds` property will
            return an indexing dictionary using the dimension names
            as keys, suitable for slicing an `xarray`.
        '''
        
        ## Internally we only work with "bottom-left" and "top-right"
        ## values, i.e. the lowest and the highest of each dimension ¯\_(ツ)_/¯
        
        self.__is_scalar = not hasattr(start or center, "__iter__")
                    
        if start is not None:
            start = np.array((start,) if self.__is_scalar else start)
                
        if size is not None:
            size = np.array((size,) if self.__is_scalar else size)
                
        if center is not None:
            center = np.array((center,) if self.__is_scalar else center)
                
        if end is not None:
            end = np.array((end,) if self.__is_scalar else end)
    
        # Need to recyle the data type of the input
        dtype = itype or np.dtype(type(start[0] if start is not None else center[0]))
        
        corner1 = np.array(start) if start is not None \
                    else (np.array(center)-np.abs(np.array(size))/2).astype(dtype)
        
        corner2 = np.array(end, dtype=dtype) if end is not None \
                    else corner1 + np.array(size)
        
        #print(corner1, corner2)
        
        self.bl = np.array([np.min(np.array([a,b])) for a,b in zip(corner1, corner2)])
        self.tr = np.array([np.max(np.array([a,b])) for a,b in zip(corner1, corner2)])
        
        #print (self.bl, self.tr)
        
        self.dims = dims
        
    @property
    def s(self):
        '''
        Returns a tuple if slice() objects, one for each dimension
        '''
        if self.__is_scalar:
            return slice(self.bl[0],self.tr[0])
        else:
            return tuple([slice(s,e) for s,e in zip(self.bl, self.tr)])
        
    @property
    def ds(self):
        '''
        Returns a dictionary with dimension names as keys and
        slicer objects (similarly to `Roi.s`) as values.
        '''
        return { k:v for k,v in zip(self.dims, self.s) }
