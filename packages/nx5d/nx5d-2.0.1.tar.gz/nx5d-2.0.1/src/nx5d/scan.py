#!/usr/bin/python3

import time
from numpy import array as np_array

import logging

from nx5d.h5like.tools import *

__all__ = [ "ScanReader" ]

'''
The Scan-Streak-Frame concept uses the following HDF5 API elements
to implement sophisticated iteration and slicing helpers:

  - Accessing of data using slicers and the indexing operator (`__getitem__`).

  - `__getitem__` access works both for selecting paths / subpaths, or selecting
    data containers within paths, or slicing parts of the data container itself,
    i.e. sub-access to limited parts of the images (i.e. only specific
    region-of-interests) via slicing. Examples:
    ```
      data["detector"] -> directory containing the "acme" subdirectory

      data["detector/acme"] -> directory, containing the "images" dataset
      data["detector"]["acme"] -> same as above

      data["detector/acme/images"] -> the dataset itself
      data["detector"]["acme"]["images"] -> same as above

      data["detector/acme/images"][3] -> image no. 3 from the dataset

      data["detector/acme/images"][3][60:160,60:160] -> a 100x100 pixel area centered
                                                        around pixel 110x110 of image no. 3

    ```

  - The HDF5 taxonomy (i.e. the '.attrs' dictionary

  - We're not using any HDF5 specific properties or Python attributes.
'''
    
class ScanReader:
    '''
    Loads data from one X-ray diffraction (XRD) scan run and offers
    convesion of images to Q space for further analysis.
    
    The idea is to open/initialize metadata (experimental parameters,
    ROIs, sizes, ...) on construction, and then subsequently "pull out"
    image data. This is supposed to work on a "live" file, i.e. one
    being measured and having data added to it.

    It assumes that data is available in a HDF5-like interface.
    It opens/closes the data object with every use to account for
    parallel use by data acquistion and/or other consumers.

    The assumptions to the data are, essentially (see also `nx5d.xrd.kmc3`):

      - All relevant datasets (frame images, angles etc) are organized
        as (arrays) of datasets with the first coordinate corresponding
        to the progression of frames, i.e. Nx(WxH) for images N for a
        particular angle etc.

      - The frame number progression (index starting with 0) corresponds
        to one or two experimental scan parameters, i.e. time delay (for
        pump-probe experiments), or a particular tilt angle. The `Chunk`
        object reflects this.

      - Instrument definition and angles are compatible with `xrayutilities`,
        the package used for the Q-space conversion.

      - The data has a Nexus-like / ESRF-style layout; this means that
        all relevant measurement data is under a specific folder of type
        "NXcollection" (typically called "measurement", but this is
        configurable), and all relevant parameterisation is stored under
        another folder (typically "instrument/positioners", but again,
        configurable). Data specification is expected relative to these
        folders.

      - Quite generally, the assumption is that we're interested in one or
        more measurement sets, and each of those depends on a subset of
        positioners.
    
    '''
    
    def __init__(self, H5pyLike, scan,
                 h5kwargs=None,
                 pathKeys=None,
                 **dreq):
        '''
        Initializes the object and basic experimental parameters.
        Needs the following:

          - `H5pyLike`: A class or a factory which generates a `h5py`-like object for
            data access. Defaults to `h5py.File`, but objects with a similar API
            (e.g. the `silx.io.spech5.SpecH5` kind of loaders) are also accepted.        

          - `scan`: A parameter list that contains information to be passed to
            `H5pyLike` in order to locate the scan within the data container.
            If the first item in that list is a string (i.e. a file path), then
            the format "resource[#path]" is accepted to pass on both the file name
            ("resource") and the path inside the container ("path"). All other
            items are passed on as unnamed arguments to `H5pyFile`.
            A typical example of this is for instance
            `("/path/to/file.h5#scan23", "r")` if `H5pyLike` is a `h5py.File`
            object. For convenience, if `H5pyLike` is indeed a `h5py.File`.

          - `h5kwargs`: `None` by default, but can be passed a dictionary of named options
            to be passed on to `loader` in addition to the resource locator string.

          - `pathKeys`: Dictionary with shortcuts of standard (?) paths. Currently,
            `ScanReader` recognizes and uses the following paths:
        
              - "measurement": Where the data is

              - "positioners": Where the positioners are (e.g. angles)

          - `dreq`: This is a list of "data request" named parameters, i.e. each key is
            a measureables, to which the value is a list of other measureables or
            poisitioners. The names of the data are relative to `measurablePath`,
            respectively `positionerPath`. The data labels may also contain a path
            component (e.g. "detector/image"), in which case all path separators
            ("/") will be replaced by underscore when data naming is performed
            ("detector_image").

            FIXME: not exactly sure how this is supposed to work. There are two main
            problems with it.
        
             1. The angles: designation of axes (goniometer, detector and image)
                are already in the 'setup' parameter. But the _actual_ angles themselves
                are not. So we have two options here: squeeze them in 'setup' (in which
                case: what is this parameter for?), or squeeze them here (in which case:
                in which order? See also 2...)

             2. The data itself: most of the time the data is the actual detector
                image / frame data. But sometimes we have data of secondary interest,
                e.g. SBcurrent (ring curren) or similar, e.g. for normalization. *This*
                data does not depend on any kind of angles or positioners... or may
                only depend on _some_ positioners. How do we model that?
        '''

        self.pathKeys = pathKeys or {'measurement': 'measurement',
                                     'positioners': 'instrument/positioners',
                                     'instrument': 'instrument' }
        
        self.h5kwargs = h5kwargs or {}

        self.dataSource = self.__source_factory(scan, H5pyLike)

        self.setupTemplate = dreq.get("setup", {})

        self.requiredDatasets = dreq.copy()

        
    def __source_factory(self, params, H5pyLike):
        # Implements magic to parse out the '#path' part of the filename.
        # Returns a callable that creates a usable h5py-like object
        # for querying scan data.

        self.H5pyLike = H5pyLike
        fileUrl, fileArgs = (None, tuple())

        if isinstance(params, str):
            fileUrl = params
        elif isinstance(params, tuple):
            fileUrl, fileArgs = params[0], params[1:]
        else:
            fileUrl = params

        if isinstance(fileUrl, str):
            tmp = fileUrl.split('#')
            if len(tmp) >= 1:
                filePath = tmp[0]
            if len(tmp) == 2:
                self.h5scan = tmp[1]
            else:
                self.h5scan = "/"
            self.h5args = tuple([filePath] + list(fileArgs))
        else:
            self.h5scan = "/"
            self.h5args = (fileUrl,)

        logging.debug("Loading: %r, args: %r, kw: %r" % (self.H5pyLike, self.h5args, self.h5kwargs))

        return lambda: self.H5pyLike(*(self.h5args), **(self.h5kwargs))


    def __defPath(self, locator):
        ''' Translates "syntactic sugar" when specifying certain HDF5 data locators.
        
        Takes a HDF5 locator as accepted by `HdfCarver` and if it's
        a string, or a tuple (str, slice, ...) adds default paths in front
        of the string if necessary (e.g. turns "data" into "@{measurement}/data").

        Everything else is returned unchanged.

        Args:
            locator: eiter a string containing a HDF5 address (`"@..."`), or a tuple
              `("...", slice(), ...)` containing a HDF5 address as its first element
              and only slice objects for every other element.

        Returns:
            The locator, translated to contain a proper HDF5 addressing ("@..."),
            or verbatim if it's not a string or a slicing tuple.
        '''

        path_mangler = lambda p: p if (p.find('/')>=0 or p[0]!='@')\
            else '@%s/%s' % (self.pathKeys['measurement'], p)
        
        if isinstance(locator, str):
            return path_mangler(locator)
        
        elif isinstance(locator, tuple) and isinstance(locator[0], str):
            return (path_mangler(locator[0]), *(locator[1:]))

        else:
            return locator


    def read (self, frameSlicer, _h5like=None, lean=False, **dataKeys):
        '''
        Returns a bunch of image(s) starting with `start`
        (default: last image taken). If `number` is None,
        all the images to the end of the scan are read.
        Parameters:
        
          - `frameSlicer`: A slice object for selecting frames within a scan
            series.

          - `roiSlicer`: Additional slicer or tuple of slicers to apply to the
            a data frame, e.g. for selecting only specific parts of the data
            frame (region-of-interest). Note that this slicer will be applied
            to *all* data keys to retrieve (see also the `dataKeys` parameter
            below), to the extent to which they have the correct dimensionality.

          - `_h5like`: A h5py-node-like object to use for reading. If none is
            specified, the one generated by the internal `dataSource()[scan]`
            factory is used. Meant only for internal use (e.g. by `.streaks()`)
            and may disappear in the future, but is otherwise safe for any kind
            abuse. The reasoning is that sometimes fake h5py-like objects
            are expensive and open (more so than HDF5 objects), so re-use might
            improve speed.

          - `lean`: If `True`, the "required datasets" (i.e. those that were
            specified with `__init__()`) are omitted from the result. The
            default is `False`.
        
          - `**dataKeys`: Data sets to retrieve; the name of the parameter will
            result in a key, and the value of the parameter should refer to the
            corresponding HDF5-like dataset path. This is passed to
            `HdfCarver`, so please also refer to the documentation
            of that class.
        
        '''        
        data = {} if lean else self.requiredDatasets.copy()
        data.update({k:self.__defPath(v) for k,v in dataKeys.items()})
        
        carver = HdfCarver(data, paths=self.pathKeys)
        
        if _h5like:
            return carver(_h5like, slicer=frameSlicer)
        else:
            with self.dataSource() as h5:
                return carver(h5[self.h5scan], slicer=frameSlicer)
    

    def streaks(self, slicer_generator=None, by=None, _h5like=None, retry=0, **dataKeys):
        '''Uses `read()` to return chunks of the data as specified by `slicer_generator`.
        
        The `addrproc` and `sliceproc` parameters are passed on to `read()`.
        
        Args:
            slicer_generator: enumerable (array, list, generator function...) which
              creates `slice()` objects, one for every streak of the family.
              See `nx5d.streaks` for a list of easily available slicer generators.
              Tip: `numpy.s_` can be used here for one-off streaks.
              This defaults to `slice(None)`, which returns all the data in one
              swoop. If this is a callable, it is interpreted as a factory function
              for a slicer generator, i.e. the actual generator is created calling
              this function with the h5py-like node as its sole parameter.
        
            _h5like: h5py-like object to use for reading. If none is specified
              (default), then the internal `dataSource()` method is being used,
              which initializes a new h5py object as specified in `__init__()`.
        
            retry: If non-zero or not `None`, file opening/reading
              is retried on `OSError` type of exceptions up to `retry`
              number of seconds (fractional number also possible)

            **dataKeys: labels (as keys) and HDF5-paths compatible with
              `HdfCarver` (as values) for the data we're interested
              in.

        Returns: this is a generator function. Each generator invocation yields
          a dictionary with the keys from `dataKeys`, and values loaded
          from the HDF5-like object, conforming to the corresponding slice
          object from `slicer_generator`.
        '''

        with _h5like or self.dataSource() as h5:
            scan = h5[self.h5scan]

            # Courtesy to the user: if the slicer generator is a callable,
            # treat it, in fact, as a factory (for a slicer generator).
            slc_gen = slicer_generator(scan) if hasattr(slicer_generator, "__call__") \
                else slicer_generator
            
            for slicer in (slc_gen or (slice(None),)):
                begin = time.time()
                while True:
                    now = time.time()
                    try:
                        yield self.read(slicer, **dataKeys, h5like=scan, lean=False)
                        break

                    except OSError:
                        if not retry or (now-begin) > retry:
                            logging.error("Final error, %f seconds after initial start" % (now-begin))
                            raise
                        else:
                            logging.debug("OSError, retrying for another %f seconds" % (now-begin-retry))

                    except DatasetEmpty:
                        logging.debug("End of dataset")
                        return

    
    def numFrames(self, dataset, _h5like=None):
        '''
        Reads (returns) the number of frames from the HDF5 file
        for the dataset refered to by `dataset`.
        '''
        
        carver = HdfCarver({'data': self.__defPath(dataset)}, paths=self.pathKeys)

        if _h5like:
            return carver(_h5like, nodeOnly=True)['data'].shape[0]
        else:
            with self.dataSource() as h5:
                return carver(h5[self.h5scan], nodeOnly=True)['data'].shape[0]
