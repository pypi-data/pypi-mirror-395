#!/usr/bin/python3

from xarray import Dataset, DataArray
from numpy import array as np_array
from nx5d.h5like.tools import HdfCarver

""" Contains various types of slicer generators to use with the `.streaks()` method
of `nx5d.scan.ScanReader`.
"""

__all__ = [ "s_length", "s_delta" ]

def s_length(val, offset=0, end=None):
    '''Generator for `slice()` objects which return sequential data pieces of lenth `val`,
    i.e. essentially `slice(0,val), slice(val,2*val), ...`.

    Since we don't know how long the full dataset will be, this continues forever,
    unless the parameter `end` is set to a maximum value. The assumption is that
    higher application layers will know when to stop retrieving data.
    The `ScanReader`, for instance, will stop once the `EmptyDataset` exception
    is encountered (...which is the case when a HDF5-like data container returns
    a dataset with length 0 in the first dimension).
    '''
    while (end is None) or (offset<end):
        yield slice(offset, offset+val, None)
        offset += val


def s_delta(val, offset=0):
    '''Generator for `slice()` objects with specified stride,
    i.e. `slice(0,None,val), slice(val,None,val), ...`.
    '''
    for i in range(0, val):
        yield slice(offset+i, None, val)


class Pabst:
    ''' The "Patten-based streaker" builds streaks by evaluating patterns in HDF5 data.

    "Streaking" is the act of repeatedly applying a parametrized set of filters
    on data, typically until *all* data has been covered once. For instance:
    an `s_delta` streak applies the "give me every N-th dataset" filter repeatedly --
    on first run starting with the 0th (then 0+Nth, then 0+2Nth, ...), then starting
    with the 1st (then 1+Nth, then 1+2Nt, ...).
    In simple cases this can be done without knowledge of that the main data itself is
    (e.g. detector images), or parameters associated with the main data (e.g. angles
    or temperatures). But a lot more powerful streaker generators can be built if
    slicing decisions can me made on the basis of data contents.

    This what `Pabst` does, and the main mechanism to achieve that is recursive
    refinement of slicing parameters. This is a two-step process: first, parameters
    relevant for the *definition* of the streaks must be read from the data source;
    second, the slicing objects must be built and presented in a way as to be
    used in `.streaks()` of `nx5d.scan.ScanReader`.
    '''

    def __init__(self, h5like=None, **params):
        '''Initializes the recursive refinement streaker with necessary parameter data.

        Args:
            h5like: A HDF5-like object, or a factory which creates one. If this is
              a callable, it is interpreted as the latter.

            **params: Each parameter name is a key by which subsequent calls
              to refinement methods can refer to data. The contents of the
              parameters need to be addresses usable by `HdfCarver`.
        '''


        # FIXME: Pabst is going to be used something like this:
        #
        #     reader.streaks(slicer_gen=Pabst(...).set(0,1).length(20), ...)
        #
        # Now inside .streaks(), two things could happen. Either using
        # the slicer generator directly:
        #
        #     with dataSource() as h5:
        #         for s in slicer_generator: ...
        #
        # Or checking whether the slicer generator is actually a callable,
        # and use that as a "factory" for a generator which also receives
        # a h5like as a parameter:
        #
        #     with dataSource() as h5:
        #
        #        sgen = slicer_gen(h5) \
        #                  if hasattr(slicer_gen, "__call__") \
        #                  else slicer_gen
        #
        #        for s in sgen: ...
        #
        # In the first case, the h5like would have been already created/used
        # *outside* of the .streaks() function, namely when creating the Pabst
        # (i.e. something like: .streaks(Pabst(h5like, ...), ...). And then
        # presumably the same h5like would've been opened later again, *within*
        # the .streaks() call.
        #
        # The latter has the advantage that we need to open the H5-like (which is
        # sometimes expensive, in particular when using fake h5py APIs) only once,
        # within the .streaks() function, and we get to reuse it. But this would
        # mean that Pabst must not use it here, in the __init__(), and must
        # actually reuse it only within the __call__().
        #
        # NOTE: also, note that for the true HDF5 format, the official HDF5 reader
        # implementation (which is also used by h5py) has a botched up memory
        # management which relies on a *global* lock -- yes, "global" as in
        # "library wide", even when acting on *different* HDF5 files. This means
        # that for very large datasets, it is actually less desireable to
        # stremline opening of files, and that more desireable to repeatedly
        # re-open files (even if it's the same file) over and over again, if this
        # can be done from different processes (as different processes, being in
        # different memory namespaces, will circumvent the library-wide locking).
        # However, intelligently making use of this feature actually requires
        # employing a multi-processing toolkit within Python, e.g. "multiprocess",
        # and this is something which is going to require extra work and
        # consideration in using with .streaks() anyway -- something we don't do
        # yet.
        #
        # So we will go the "open HDF5 as little as possible" approach for now,
        # which means we'll store the h5like and parameter template here, and
        # actually only use them on __call__().
        #

        self._h5like = h5like
        self._params_template = params
        self._refine = []


    def moo(self, **kwargs):
        self._refine.append(kwargs)
        return self


    def __call__(self, h5like=None):
        ''' Triggers the refinement, optionally using the specified `h5like`.
        '''

        # We prefer the supplied one, but will gladly take the stored one
        # (i.e. supplied with __init__) if none is supplied here.
        h5obj = h5like or self._h5like
        if hasattr(h5obj, "__call__"):
            with h5like() as h5:
                params = HdfCarver(self._params_template)(h5)
        else:
            params = HdfCarver(self._params_template)(h5obj)

        # At this point, self.params hs a dict() containing data.
        # What we need to do now is loop through the data items
        # and yield the slices -- one at a time. What we need to
        # to *before* that is apply the refiners. We like to work
        # on an xarray.Dataset().
        tmp = next(iter(params.items()))
        xdata = Dataset({'INDEX': np_array(range(tmp[1].shape[0]))})
        for k,p in params.items():
            dims = ["INDEX"] + ["%s_%d" % (k,i) for i in range(1,len(p.shape))]
            xdata[k] = (dims, p)
        
        return xdata

        #print("xdata coords:", xdata.coords)
        #print("xdata:", xdata)

        #print("idx 3:", xdata.sel(idx=3))

        # xdata now has all the relevant data.
        # (hopefully) self._refine is a list of dictionaries (key, value)
        # to refine the index list with. Iterate through it.
        #result = xdata
        #for ref in self._refine:
        #    print("refine:", ref)
        #    #result = result.sel(**ref)

        #return result
