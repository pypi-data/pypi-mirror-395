#!/usr/bin/python3

import time
from xarray import DataArray, Dataset
from xarray import concat as xr_concat


import numpy as np

import logging

import time

from tqdm import tqdm

# Goniometer coordinate system definitions in SPEC:
#    https://www.certif.com/spec_manual/fourc_4_1.html
#
# Coordinate system in xrayutilities:
#    https://journals.iucr.org/j/issues/2013/04/00/rg5038/index.html

class InsufficientData(RuntimeError):
    # raised when data sets are missing
    pass

class InsufficientAngles(InsufficientData):
    # specifically for angle datasets
    pass

class UnsuitableData(RuntimeError):
    # raised when data format is bad
    pass
    
class QMapper:
    ''' Base class for all Xrayutilities based Q-space mapper.

    This essentially just initializes the experimental setup
    for xrayutilities and prepares for accepting "useful" data.
    The relevant Xrayutilities algorithm wrappers are also
    implemented here.

    This is a fully functional implementation with a clean
    separation between static setup data (experiment geometry)
    and measurement data (angles and images). Subclasses may still
    implement more specific usage APIs.

    Example
    ```

    # Defining an experimental geometry. We put this in a dictionary
    # for clarity, but we could just as well pass the parameters to
    # QMapper(...) below one by one.
    exp_setup = {
        'beamDirection': (0, 1, 0),
        'beamEnergy': 9600.0,
        'imageAxes': ('x-', 'z-'),
        'imageCenter': (90, 245),
        'imageChannelSize': (0.172, 0.172),
        'imageDistance': 720.0,
        'imageSize': (195, 487),
        'sampleFaceUp': 'z+',
        'sampleNormal': (0, 0, 1)

        # keys here will be used to find the angles in the xarray.Dataset
        'goniometerAxes': {
            'phi': 'x+',
            'chi': 'y+',
            'omega': 'z+'
        },

        # These last two keys of the detector axes will be ignored,
        # because angle spec is None. Yet we still need to define them
        # even if the detector doesn't have an Azimuth or Rotation axis.
        'detectorTARAxes': {
            'twotheta': 'x+',
            'a': None,
            'r': None
        },
    }

    # We demonstrate the layout of an xarray Dataset suitable for Q-mapping.
    # In a real example, instead of generating the data, we'd read it
    # (e.g. from a HDF5 file)
    raw_data = xarray.Dataset(
        data_vars={
          'chi':      ('index', np.array(...)),
          'phi':      ('index', np.array(...)),
          'omega':    ('index', np.array(...)),
          'twotheta': ('index', np.array(...)),
          'pilatus':  (('index', 'x', 'y'), np.array(...)),
        },
        coords={
          'index': np.array(range(N)), # N is the number of images/angles here
          'x': np.array(range(195)),   # 195 is the image width, see exp_setup above
          'y': np.array(range(487))   # 487 is the image height in pixels
        })

    # Defining the mapper
    mapper = QMapper(**exp_setup)

    # This is the most simple approach: call .qmap() and let it figure out
    # useful defaults (which it will, given the Dataset above).
    q_data = mapper.qmap(raw_data)

    # Different approach: specify explicitly which image to transform...
    q_data = mapper.qmap(raw_data, images="pilatus")

    # ...or which angle sets to use...
    q_data = mapper.qmap(raw_data, angles=("chi", "phi", "omega", "twotheta"))

    # ...or both.
    q_data = mapper.qmap(raw_data, angles=("chi", "phi", "omega", "twotheta"),
                         images="pilatus")

    # Control Q-space grid size
    q_data = mapper.qmap(raw_data, qsize=(100, 100, 200))

    # Or reduce the number of dimensions (i.e. 2D Q-space map)
    q_data = mapper.qmap(raw_data, dims=("qx", "qz"))

    # Or both at the same time (using a dictionary for qsize instead of a tuple)
    q_data = mapper.qmap(raw_data, qsize={"qx": 100, "qz": 200})
    ```

    This will result e.g. in transforming a raw_data dataset like this:
    ```
    >>> raw_data
    <xarray.Dataset>
    Dimensions:   (index: 64, x: 195, y: 487)
    Coordinates:
      * index     (index) int64 0 1 2 3 4 5 6 7 8 9 ... 55 56 57 58 59 60 61 62 63
      * x         (x) int64 0 1 2 3 4 5 6 7 8 ... 187 188 189 190 191 192 193 194
      * y         (y) int64 0 1 2 3 4 5 6 7 8 ... 479 480 481 482 483 484 485 486
    Data variables:
        phi       (index) float64 0.0 0.0 0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0 0.0
        chi       (index) float64 0.0 0.0 0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0 0.0
        theta     (index) float64 12.0 12.01 12.02 12.03 ... 12.6 12.61 12.62 12.63
        twotheta  (index) float64 24.0 24.01 24.02 24.03 ... 24.6 24.61 24.62 24.63
        pilatus   (index, x, y) float64 0.0 0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0 0.0
    ```

    into something like this (in the default case):
    ```
    >>> q_data
    <xarray.DataArray (qy: 64, qx: 195, qz: 487)>
    array([[[0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.],
    ...
            [0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.]]])
    Coordinates:
      * qy       (qy) float64 -0.5787 -0.574 -0.5693 ... -0.293 -0.2883 -0.2836
      * qx       (qx) float64 -0.2423 -0.2409 -0.2395 ... 0.0337 0.03513 0.03657
      * qz       (qz) float64 1.72 1.721 1.722 1.723 ... 2.279 2.28 2.281 2.282
    ```
    '''

    def __init__(self, **experiment_setup):
        ''' Initializes the experimental geometry.

        The arguments to `.__init__()` are inspired from the xrayutitlities
        `Experiment` classes, but they're intended to be fairly generic
        and represent the actual physics, not a specific coded implementation
        of it. They should be the same for all backends, even if different from
        xrayutilities.
        
        Args:
            **experiment_setup: parameters for the experimental setup. Refer
              to `.init_experiment()` for a complete documentation of the
              parameters.

        '''

        self.init_experiment(**experiment_setup)
        self.Ang2Q = self.hxrd.Ang2Q

        # additional gridder / ang2q setup variables
        self.gridderDict = {}
        self.ang2qDict = {}


    def init_experiment(self,
                        beamEnergy: float = None,
                        beamDirection=None,
                        goniometerAxes=None,
                        detectorAxes=None,
                        detectorTARAlign=None,
                        imageAxes=None,
                        imageCenter=None,
                        imageChannelSize=None,
                        imageChannelSpan=None,
                        imageDistance=None,
                        imageSize=None,
                        sampleFaceUp=None,
                        sampleNormal=None,
                        roi=None):
        '''
        Initializes the experiment setup representation.

        This is typically an xrayutilities HXRD object or similar,
        with specified device and sample geometry. The optional parameter `roi`
        restricts angle-to-Q conversion to solely this region, if it is
        specified. This is a good way to save significant amounts of computing
        time.

        Args:
        
          beamEnergy: the energy of the incoming X-ray beam, in eV.

          beamDirection: direction of the X-ray beam. 
        
          goniometerAxes: the direction of each of the goniometer axes,
            in the `[xyz][+-]` notation. This is a variable-sized array, as there
            can be several axes in any goniometer, and `xrayutilities` apparently
            magically knows what to do.
            This can hold an arbitrary number of angles, the only restriction
            (according to `xrayutilities` docs)
            being that these must be in from the outer to the inner rotations.
            This can either be a simple enumerable (list or tuple), to specify
            only the axis orientations; or this can be a dictionary, to *also*
            specify the names in addition to the orientation.

          detectorAxes: detector rotation axes, from outer to inner (similarly
           to `goniometerAxes`).

          imageAxes: the direction of the image axes (x and y) at zero angles.
            The positive direction of the axes should coincide with increasing pixel
            index in the data.

          imageCenter: this is the position of the center pixel, either absolute
            (integer pixel numbers), or relative to the sensor size (as specified in
            `imageAxes`). If the number is in the range 0.0..1.0, then relative
            positioning is assumed.

          imageChannelSize: for Q transformation, ultimately the relation between
            every specific on the detectors and the angle
            of the incoming beam activating that specific pixel is needed. There
            are two distinct ways of specifying this: either using the "channel span",
            i.e. the size, in degrees, of each pixel, in horizontal/vertical direction,
            or by a distance parameter (from detector to sample) and a pixel size.

            `imageChannelSpan` is either a single number or a 2-tuple specifying
            how many degrees one channel takes. `imageChannelSize` specifies the
            spatial size of a pixel relative to the distance between the sample
            and the sensor.

          imageChannelSpan: (overrides `setup["imageChannelSpan"]`),
            see `imgeChannelSize`.

          imageDistance: (overrides `setup["imageDistance"]`),
            distance of the detector from the center of rotation.

          imageSize: (overrides `setup["imageSize"]`), width and height of one detector
            image.

          sampleFaceUp: (overrides `setup["sampleFaceUp"]`),
            direction of the "sample surface facing up", a.k.a.
            "sampleor" (sample orientation) in `xrayutilities` lingo.
            This is the orientation of
            the sample surface at zero angles. This is either an axis notation
            (`[xyz][+-]`) or one of the special words `det`, respectively `sam`.

          sampleNormal: (overrides `setup["sampleNormal"]`), not sure
            what this is... in `xrayutilities`.

        Returns: the internal representation of the experiment (typically an
        xrayutilities.Experiment instance, when xrayutilities is used as a backend).
        The internal representation is also stored within the object.
        '''
        
        def __2tuple(data, name=""):
            ## Returns a 2-tuple (X, Y) from a variety of data sets:
            ## - from a 2-tuple :-) or an array with size 2
            ## - from an array (N, 2) (returns the tuple of the first elements)
            ## - from an array or tuple (2, N) (returns the first element)
            if not hasattr(data, "__len__"):
                raise UnsuitableData(f"{name}: needs to be a 2-tuple")
            if len(data) == 2:
                if hasattr(data[0], "__len__"):
                    return ([data[0][0], data[1][0]])
                else:
                    return ([data[0], data[1]])
            if len(data) > 2:
                return data[0]
            raise UnsuitableError(f"Oops: don't know how to handle {name}: {data}")


        ## Axes can be either dict() or enumerables; try to sort them out.
        ax_spec = lambda ax_set: ax_set if not hasattr(ax_set, "keys") else [ax_set[k] for k in ax_set]
        ax_keys = lambda ax_set: [] if not hasattr(ax_set, "keys") else [k for k in ax_set]
        
        setupAxesKeys = ax_keys(goniometerAxes) + ax_keys(detectorAxes)

        if detectorTARAlign is None:
            detectorTARAlign = (.0, .0, .0)
        

        # beamEnergy is usually supposed to be a scalar, but sometimes an array
        # (one for each image) will be supplied. In that case, retrieve only the first.
        beamEnergy = beamEnergy if not hasattr(beamEnergy, "__len__") else beamEnergy[0]

        from xrayutilities import HXRD as xu_HXRD
        from xrayutilities import experiment as xu_experiment        

        qconv = xu_experiment.QConversion(sampleAxis=ax_spec(goniometerAxes),
                                          detectorAxis=ax_spec(detectorAxes),
                                          r_i=beamDirection,
                                          en=beamEnergy)

        self.hxrd = xu_HXRD(idir=beamDirection,
                            ndir=sampleNormal,
                            sampleor=sampleFaceUp,
                            qconv=qconv,
                            # Workaround for buggy xrayutilities: repeat the beam energy
                            en=beamEnergy)

        imageCenter = __2tuple(imageCenter, 'imageCenter')
        imageSize = __2tuple(imageSize, 'imageSize')
        imageDistance = imageDistance[0] if hasattr(imageDistance, "__len__") \
            else imageDistance

        logging.debug("image distance %r, size %r, center at %r" % \
                      (imageDistance, imageSize, imageCenter))
        
        if imageCenter[0] <= 1 and imageCenter[1] <= 1:
            # It's a floaring-point number, relative to the detector size

            # similar considerations for imageSize as for imageCenter: expected to be
            # a 1D array with length 2, but will also accept a 2D array
            # with shape (N, 2).
            
            # FIXME: really, REALLY need to fix this. This is really ugly.
            imgs = imageSize
            assert imgs is not None
            assert imgs[0] is not None
            assert imgs[1] is not None            
            imageCenter = tuple([c*s for c,s in zip(imageCenter, imgs)])

        chSizeParm = {}
        if imageChannelSpan is not None:
            # channelSpan is degrees/channel, but need to pass channels/degree to Ang2Q
            imageChannelSize = self.__2tuple(imageChannelSpan, 'imageChannelSpan')
            chSizeParm = {'chpdeg1': 1.0/imageChannelSpan[0],
                          'chpdeg2': 1.0/imageChannelSpan[1] }

        elif imageChannelSize is not None:
            # Ang2Q takes one explicit distance parameter, but we're assuming that
            # channelSize is relative to the distance itself (putting the distance
            # always at 1.0 units)
            imageChannelSize = __2tuple(imageChannelSize, 'imageChannelSize')
            logging.debug("pixel size: %r" % (imageChannelSize,))
            chSizeParm = { 'pwidth1':  imageChannelSize[0],
                           'pwidth2':  imageChannelSize[1],
                           'distance': imageDistance }

        else:
            raise RuntimeError("Experiment setup needs either the "
                               "channel span or channel size")

        if roi is None:
            roi = (0, imageSize[0], 0, imageSize[1])

            
        self.hxrd.Ang2Q.init_area(detectorDir1=imageAxes[0],
                                  detectorDir2=imageAxes[1],
                                  cch1=imageCenter[0],
                                  cch2=imageCenter[1],
                                  Nch1=imageSize[0],
                                  Nch2=imageSize[1],
                                  tilt=detectorTARAlign[0],
                                  tiltazimuth=0,
                                  detrot=detectorTARAlign[2],
                                  roi=roi,
                                  **chSizeParm)

        ## save some relevant setup parameters for later use
        ## (e.g. for auto-detecting datasets in .qmap())
        self.setupRoi = roi
        self.setupImageSize = imageSize
        self.setupImageAxes = imageAxes

        # only if we have all axes names
        self.setupAxesKeys = setupAxesKeys \
            if len(setupAxesKeys) == len(goniometerAxes)+len(detectorAxes) \
               else []

        logging.debug(f'Remembering setup axes keys: {self.setupAxesKeys}')
        
        return self.hxrd


    def setupGridder(self, **gridderDict):
        self.gridderDict = {}
        self.gridderDict.update(gridderDict)


    def setupAng2Q(self, **ang2qDict):
        self.ang2qDict = {}
        self.ang2qDict.update(ang2qDict)
    

    def qmap(self,
             xdata,
             images=None,
             angles=None,
             qsize=None,
             dims=None,
             retain=True,
             output=None,
             dask_compute=False):
        '''
        Performs Q-space mapping on `xdata`.
        
        The detector image data to map into Q-space (see `images` and `xdata`
        parameters) must have the image same size as the `imageSize` parameter
        that was passed to `.__init__()` of no region-of-interest (`roi`)
        was specified. If a `roi` was specified to `.__init__()`, then
        the image data must be the size of the `roi`, and the corresponding
        pixel index must start with the lower numbers of the corresponding
        `roi` dimension.
         
        Args:
            xdata: `xarray.Dataset` with detector data to be transformed
              and angles.

              By default, the name of the detector data (array)
              within the set is extracted from the `images` parameter,
              or is guessed automatically by comparing the 2nd and 3rd
              dimension with `imageSize`. If multiple matching detector
              image sets are found, the first that matches is used.

              The name of the angles are used by reading the `goniometerAxes`
              and `detectorTARAxes` from `.__init__()`, but can be overridden
              by the `angles` parameter.

            images: a string representing name of the detector data to transform
              within the `xdata` dataset.

            angles: a tuple of strings representing names of the angle datasets
              within `xdata`. If this is specified, it must firs t list all goniometer
              angles (from outer to inner), then all detector axes, as a flat
              names tuple (i.e. non-nested). All the angles datasets must have the
              same first dimension as the images dataset.

            qsize: Can be either a tuple `(w, h)`, or `(w, h, d)` of the resulting Q
              image, or a dictionary `{'qx': w, 'qy:..., ...}`.
              If it is `None`, the size of the original angular image dimension(s)
              is used for a 3D Q-mapping.

            dims: List with dimension names "qx", "qy" or "qz", or any combintion
              thereof, for resulting Q image. This effectively dictates what
              kind of Q-mapping is perform ed (1D for a single dimension name,
              2D if two names are specified, or 3D of all 3 are specified), and which
              projection (i.e. `("qx", "qy")`, or `("qz", "qx")`, ...).
              The spatial designations (x, y or z) are in consistency with the
              corresponding axis definitions of the `.__ini__()` parameters, where
              each reciprocal space (Q-) coordinate is correctly defined as perpendicular
              on the other two real space coordinates in `.__init__()`.
              If this is `None` (the default value), the keys of `qsize` are used;
              if those are *also* `None` (also the default value), then a 3D Q-space
              mapping is performed.
              
            retain: if True, extra data variables and coordinates
              from `xdata`, which are not being processed during the Q-mapping (i.e.
              everything else besides image data and angles), is being transfered
              over to the output data. This effectively retains per-transformation
              metadata. The default is "auto", which results to `False` here,
              but `True` in `.qmap_groupby()`.
              
            output: Name of the output array in the resulting dataset. If `None`,
              it will be the same as the name of the input data.

            dask_compute: will run `.compute()` on the input dataset first, if it
              is a Dask array.
        
        Returns: an `xarray.Dataset` (or `DataArray`?) with the designated detector
          data (see `images`) on a corresponding reciprocal space grid (see `qsize`),
          and their corresponding Q-axes values.
        '''

        image_name  = self._select_image_name(xdata, images)
        angle_names = self._select_angle_names(xdata, angles)        
        grid = self._select_grid_size(qsize, dims, xdata[image_name].shape)

        is_dask = np.array([(xdata[k].chunks is not None) for k in xdata]).any()
        if is_dask and dask_compute==True:
            input = xdata.compute()
        else:
            input = xdata

        return self._invoke_area_qconv(input,
                                       image_name,
                                       angle_names,
                                       grid,
                                       retain=retain,
                                       output=output if output is not None else image_name)
    
    
    def qmap_single(self, xdata, *args, **kwargs):
        '''
        Convenient wrapper for `.qmap()` to use when data only has a single image.
        
        "Regular" `.qmap()` will choke, as it is expecting a batch of angular pixel
        data, and a batch of angles. On single images, there's only one of each
        (each angle, image etc), and there's no 3rd dimension.
        
        The easy thing to do is simply extend `xdata` by an extra dimension. However,
        one thing we *also* want to do is modify implicit settings for `dims` to
        produce a 2D Q-map (since that's what the user will be expecting).
        
        NOTE: deprecated, try using `.groubpy(squeeze=False)` instead.
        '''
        default_dims = tuple([f'q{x[0]}' for x in self.setupImageAxes])
        qdata = self.qmap(xdata.expand_dims('index'), *args, **kwargs)
        return qdata
    
    
    def qmap_groupby(self,
                     data,
                     groupby=None,
                     combine=None,
                     auto_compute=False,
                     concat_params=None,
                     *args, **kwargs):
        '''
        Invokes the Q-space mapping on every member of a `.groupby()` result.
        
        Think of this as a fancy `xdata.groubpy(...).map(QMapper().qmap())` call.
        The split-process-combine pattern of `.groupby()` is very powerful and
        allows to write expressive data analysis code -- which we want. However,
        combining results of `.qmap()` usually lead to unintended results, simply
        because every single call comes with its own set of qx, qy and qz
        coordinates.
        
        Mostly, these are "the same" in the physical sense, but `xarray` doesn't
        recognize them as the same because of minor numerical variations. To
        combine them (and still have some failsafe / restored functionality when
        they're actually *not* the same, just similar), we scale and transform the
        coordinate vectors into integers after `.qmap()` invocation, but before
        combining. Then after combination, we re-scale them back to their original
        magnitude and transform them to float.
        
        Args:
            data: `xarray.Dataset` or `DatasetGroupBy`. If it's a dataset, it is
              grouped according to the `groupby` parameter(s). Otherwise the groups
              are used as they are.
              
            groubpy: string or enumerable to pass to `.groupby()`. Only used if
              `data` is not a `DatasetGroupBy`.
              
            combine: how to combine data after having transformed each group item
              through `.qmap()`. The following options are accepted:
                - `None` or "*none*" does not recombine, just returns
                  a list of result objects.
                - "*qcoord*" assumes that all Q-coordinates, to all of the transformed
                  group items, are the same, and variations are just owing to numerical
                  differences. Recombination is therefore performed explicitly by
                  `.qmap_groupby()` by taking the first set of Q-coords, and
                  overriding/reusing it for every other group item.
                - "*groupby*" goes with whatever the `.groubpy()` function does.
                  It only works when the `groubpy` parameter is not `None`.
                
              *args: passed to `.qmap()`.
              
              **kwargs: passed to `.qmap()`. If the `retain` argument is set to "auto",
                it is modified to `True`.
        
        '''

        if combine is None:
            combine  = "qcoord" if groupby is None else "groupby"

        # set "retain" default
        if kwargs.get('retain', 'auto') == 'auto':
            kwargs['retain'] = "data_vars"
        
        ## Step 1: splitting (if necessary)
        if hasattr(data, "groups"):
            xgroups = data
        else:
            is_dask = np.array([(data[k].chunks is not None) for k in data]).any()
            input = data.compute() if (is_dask and auto_compute in (True, 'early')) else data
            if groupby is None:
                raise RuntimeError(f'Input data is {type(data)}; if that\'s not a DatasetGroupBy, '
                                   f'you need to specify a groupby=... grouping criterion.')
            xgroups = input.groupby(groupby, squeeze=False)


        ## Helper: runs invoke_qmap(), optionally running .compute() on the input data set.
        ## This is necessary because we actually have two distinct types of 'auto_compute':
        ##    - whole dataset (a.k.a. "early"), or
        ##    - group-by-group (a.k.a. "late").

        def do_qmap(data, *args, **kwargs):
            is_dask = np.array([(data[k].chunks is not None) for k in data]).any()
            if is_dask and auto_compute in (True, 'late'):
                input = data.compute()
            else:
                input = data
            return self.qmap(input, *args, **kwargs)
            
        
        ## Step 2a: Q-mapping and combining in one go (implicitly via .map())
        if combine in ("groupby",):
            return xgroups.map(do_qmap, *args, **kwargs)


        # Alternatively, Step 2b: first Q-mapping..
        qlist = []
        for l in tqdm(xgroups):
            qlist.append( do_qmap(l[1], *args, **kwargs) )

         
        # Step 3: ... then combining.
        if combine in (None, False, "none"):
            return qlist

        if combine in ("concat",):
            if concat_params is None:
                concat_params = {}
            return xr_concat([q.set_coords(groupby) for q in qlist],
                             dim=groupby, **concat_params)

        
        raise RuntimeError(f'You are not supposed to ever end up here (combine={combine}).')


    def _invoke_area_qconv(self, xdata, image_name, angle_names, grid,
                           ang2qObj=None, qquant=None, retain="data_vars",
                           output=None):
        ''' Actual (internal) invocation of the Q-conversion.

        Parameter sorting & processing happens before this. Here the
        actual breakdown of the xarray data into (for xrayutilities usable)
        numpy arrays happens. For small data this is straight-forward
        by just calling `.values` on the data.
        However, but subclasses might want to reimplement this for more
        sophisticated treatment (e.g. using Dask arrays? threads?...
        split-process-combine patterns?)
        
        This function *can*, but *is not intended* to be called from outside
        QMapper. There are some specific arguments used to enhance "user
        experience", in particular when working with large data / Dask clusters,
        but they require intimate knowledge of QMapper's internals.
        
        Args:
            xdata: the `xarray.Dataset` to work on (must contain images and angles)
            image_name: name of the image data var to transform
            angle_names: list of angle data vars, each for one angle, in the
              correct order (see `xrayutilities` or `.__init__()`)
            grid: dictionary with grid size(s) in Q-space
            ang2qObj: `Ang2Q` object from `xrayutilities`. If not specified,
              `self.Ang2Q` is used (which has been created at `.__init__()`
              or `.init_experiment()` time)
            qquant: factor to use for Q-coordinate quantization. If this
              is different from `None`, then the Q-coordinates are multiplied
              by this factor and cast to integer after Q-mapping, but before
              returning the final result. This feature is used internally in
              `.qmap_groupby()` in order to make direct comparison of Q values
              easier, and thus recombination of `.groubpy()` data pieces.
              Steer away from this if you don't know what you're doing.
            retain: if `True` (default here), all data variables and coordinates
              from `xdata` which weren't used in the transformation are retained
              in the output. 
            output: Which name to choose for the output Q-mapped images.
        '''
        
        tmp_i = xdata[image_name] #.values
        tmp_a = [xdata[a].values for a in angle_names]
        result_name = output if output is not None else image_name
        qdata = self._area_qconv(tmp_i, tmp_a, grid, result_name,
                                 self.gridderDict, self.ang2qDict, self.Ang2Q)
                
        if retain in (None, False, "none"):
            return qdata
        
        ## copy extra data and coordinate dimensions over.
        ## ACHTUNG: disabling this, as this will also copy index coordinates,
        ##          which will massively interfere with .qmap_groupby()'s
        ##          attempts to restore indices. Not sure how to deal with
        ##          this yet. (Maybe we should filter out index+index parts?)
        ##
        ## index = xdata.dims[0]
        ## index_parts = xdata.get_index(index)
        ##   ^^^ like this?
        ##
        #if retain in ("all", "coords", True):
        #    logging.warning(f'retain={retain}, but will cowardly refuse to retain coords')
        #    xcoords = filter(lambda x: (x not in qdata.coords), xdata.coords)
        #    new_coords = { k:xdata.coords[k] for k in xcoords }
        #    qdata = qdata.assign_coords(new_coords)
        
        if retain in ("all", "data_vars", True):
            xvars = filter(lambda x: (x not in qdata.data_vars and\
                                     x not in angle_names and\
                                     x != image_name),
                           xdata.data_vars)
            extra_vars = { k:xdata.data_vars[k] for k in xvars }
            for k in extra_vars.keys():
                if len(xdata[k].dims) > 0:
                    qdata[k] = xdata[k].mean(dim=xdata[k].dims[0])
                else:
                    qdata[k] = xdata[k]
        
        #print(f"qconv data: {[k for k in qdata.keys()]}, retain: {retain}")
        return qdata
        

    def _verify_data(self, image_data, angle_data):
        # check angles / images for dimension integrity and get loud if they don't match
        for a in angle_data:
            if a.shape[0] != image_data.shape[0]:
                logging.error('One full set of angles is expected for each image, but we got this instead:')
                logging.error(f"Images: {image_data.shape}")
                for a in angle_data:
                    logging.error(f"Angles: {a.shape}")
                raise UnsuitableData('Dimension mismatch on data')
        

    def _select_grid_size(self, qsize, dims, data_shape):
        ## Returns a dictionary with the Q coordinate axes we want to have
        ## (i.e. qx, qy, qz...) and their respective sizes in Q-space.
        ## Defaults to a full 3D Q-map of the same size as the original data.

        # first we need to determine the axis names: self.setupImageAxes defines how
        # the image coordinates Width and Height are named; the rest is the remaining
        # one.
        all_axes = ['x', 'y', 'z']
        tmp = [i[0] for i in self.setupImageAxes]
        for t in tmp:
            assert t in all_axes
        full_axis_set = [f'q{x}' for x in filter(lambda x: x not in tmp, all_axes)] \
            + [f'q{x}' for x in tmp]

        default_qsizes = { q:s for q,s in zip(full_axis_set, data_shape) }

        # Common mistake: when specifying only one axis (1D gridding), sometimes
        # people don't want, or remember, to properly write tuples as ("axis",).
        # The error message of trying to iterate through a string instead of
        # an enumerable is also quite cryptic. We try to catch that and
        # "do the right thing".
        if isinstance(dims, str):
            dims = (dims,)
        
        # names: dims takes precedence; if qsize has names, we use them
        # only for identifying data, if dims i s defined; otherwise we
        # use them to collect labels, too.
        # if all fails, we fall back on full_axis_set for names.
        names = dims or ([k for k in qsize.keys()] \
                         if hasattr(qsize, 'keys')
                         else full_axis_set)

        all_q_axes = tuple([f'q{x}' for x in all_axes])
        for n in names:
            if n not in all_q_axes:
                raise RuntimeError(f'Requested Q-axis "{n}" not in accepted pool {all_q_axes}')

        if hasattr(qsize, "keys"):
        # qsize is a dict()-like
            return dict(filter(lambda x: x[0] in names, qsize.items()))
        
        elif hasattr(qsize, "__getitem__"):
            # qsize is a simple tuple/array
            sizes = qsize if qsize is not None else data_shape
            if len(sizes) != len(names):
                raise RuntimeError(f'Requested Q dimension names ({names}) '
                                   f'and sizes ({sizes}) mismatch')
            return { q:s for q,s in zip(names, sizes) }
        
        elif qsize is None:
            return { q:default_qsizes[q] for q in names }

        else:
            raise RuntimeError(f'What to do with qsize={qsize}?')

            


    def _select_angle_names(self, xdata, angles):
        ##
        ## Returns a list of angles, according to `angles` (it not None),
        ## or according to the setup goniometerAxes / detectorTARAxes.
        ##
        if angles is None:
            if self.setupAxesKeys is None:
                raise InsufficientAngles(f'No angle data specified -- you need to either set `angles`,'
                                         f'or modify the axes specifications to contain axis names.')
            angles = self.setupAxesKeys
            
        return angles


    def _select_image_name(self, xdata, images):
        ##
        ## Selects the suitable image data vector from `xdata`. Essentially,
        ## we either use what `images` tells us to, or try to auto-guess from
        ## the detector image geometry+roi of the setup data.
        ##
        ## Returns a 3D image array (xarray?).
        ##
        if images is not None:
            image_data = xdata[images]
            if len(image_data.shape) != 3:
                logging.error(f'Data set "{images}" has wrong dimensionality. Expected: 3D image data, '
                              f'got {image_data.shape} instead. '
                              f'Continuing, but this is most likely not what you want to do.')
            roi_size = (self.setupRoi[1] - self.setupRoi[0],
                        self.setupRoi[3] - self.setupRoi[2])
            if image_data.shape[-2:] != roi_size:
                logging.error(f'Data set {images} has wrong image size (expecting '
                              f'{image_data.shape[-2:]}, got {roi_size}). '
                              f'Continuing, but this might crash.')
                
            return images
        
        else:
            for (img_name, img_data) in xdata.data_vars.items():
                _size = np.array((self.setupRoi[1] - self.setupRoi[0],
                                  self.setupRoi[3] - self.setupRoi[2]))
                if len(img_data.shape) != 3:
                    logging.debug(f"Skipping {img_name}: shape != 3D")
                    continue ## data has wrong dimension
                if (np.array(img_data.shape[1:3]) != _size).all():
                    logging.debug(f"Skipping {img_name}: img_size != {_size}"
                                  f" -> {img_data.shape[1:3]}")
                    continue ## image does not match ROI / setup image size
                logging.debug(f'Auto: detector image data is {img_name}')
                return img_name
            
        raise InsufficientData(f'No suitable detector image found among data '
                               f'vars {[k for k in xdata.data_vars]}')

        
    def _calc_qcoord(self, ang2q, angles, aqdict, gridSize):
        # calculates a Q-coordinate grid
        qcoord = ang2q.area(*angles, **(aqdict or {}))

        qindex = { 'qx': 0, 'qy': 1, 'qz': 2 }
        return [qcoord[qindex[d]] for d in gridSize.keys()]
        
        #return qcoord

    
    def _calc_qmap(self, images, qcoord, gridSize, gridderDict):
        # Calls the gridder to calculate the Q-images.
        # Returns the gridder object array (containing Q-data and Q-axes)
 
        # Call scheme of all the xrayutilities Gridders is pretty similar:
        #   FuzzyGridder1D/2D/3D(...grid sizes...)(qx, qy, qz, ...)

        import xrayutilities as xu
        Gridder = getattr(xu, "FuzzyGridder%dD" % len(gridSize))
        grd = Gridder(*[g[1] for g in gridSize.items()])
        grd(*qcoord, images.values, **(gridderDict or {}))
        return grd

    def _retr_qdata(self, gridder):
        return gridder.data
        
    def _retr_qaxis(self, gridder, index=None, name=None):
        # Retrieves xaxis, yaxis, zaxis from gridder.
        # FIXME: Retrieving by index (x, y, z) or retrieving by name?
        # Note that 'name' here is "qx", "qy", ...

        ## By index:
        return getattr(gridder, f"{'xyz'[index]}axis")

        ## By name:
        #assert name in ('qx', 'qy', 'qz')
        #real_name = name[1]
        #return getattr(gridder, f"{real_name}axis")
        
    def _area_qconv(self,
                    images,
                    angles,
                    gridSize,
                    result_name,
                    _gridderDict=None,
                    _ang2qDict=None,
                    _ang2qObj=None):
        '''
        Front to the ang-to-Q conversion, currently only for area data. Parameters:
        `datasets` is either empty, or a single data label. (No multiple label support
        yet.)
        
        Args:
            images: 3D array of images to transform, 1st dimenson number of images,
              dimnesions 2 and 3 as width/height of images. `QMapper` is Dask-aware,
              so if the `images` array is a Dask array, the most compute-intensive
              step (gridding) will be performed in a `dask.delayed()` wrapper
              and a Dask array will be returned as the Q-mapped images.

            angles: list of all necessary angles, in the correct order (first
              goniometer from outer to inner, then available TAR angles)

            gridSize: Python dictionary with Q-space directions as keys, and number
              of data points in Q-space as values

            `_gridderDict`: If specified, this is a dictionary with extra named
              parameters to be passed on to the gridder. Note that this is not portable,
              only works as long as we're using xrayutilities under the hood.

            _ang2qDict: Extra set of parameters to be passed to the data-specific
              `Ang2Q` function (typically `Ang2Q.area()` for stacks of 2D datasets).
        '''
        
        if len(images.shape) != 3:
            raise RuntimeError(f"Don't know how to transform objects of shape {images.shape}")
        
        # For transforming strings to dimension indices
        #qindex = { 'qx': 0, 'qy': 1, 'qz': 2 }

        # Call scheme of all the xrayutilities Gridders is pretty similar.
        if images.chunks is None:
            qcoord   = self._calc_qcoord(_ang2qObj, angles, _ang2qDict, gridSize) 
            grd      = self._calc_qmap(images, qcoord, gridSize, _gridderDict)
            grd_data = self._retr_qdata(grd)
        else:
            import dask
            qcoord   = dask.delayed(self._calc_qcoord)(_ang2qObj, angles, _ang2qDict, gridSize) 
            grd      = dask.delayed(self._calc_qmap)(images, qcoord, gridSize, _gridderDict)
            grd_data = dask.array.from_delayed(dask.delayed(self._retr_qdata)(grd),
                                               shape=tuple([d[1] for d in gridSize.items()]),
                                               dtype=float)
        
        # ...the tricky part is creating the DataArrays. Specifically,
        # retrieving the q coordinates from the gridder. They are in `grd`
        # attributes called 'xaxis', 'yaxis', ... according to dimension.
        # We always use qx/qy/qz for dimension keys.
        coords = {}
        for i,axname in enumerate(gridSize.keys()):
            if images.chunks is None:
                axvals = self._retr_qaxis(grd, index=i, name=axname)
            else:
                #print(f'gridSize: {gridSize}, data shape: {shp}')
                import dask                
                axvals = dask.array.from_delayed(
                    dask.delayed(self._retr_qaxis)(grd, i),
                    shape=(gridSize[axname],),
                    dtype=float)
                
            # The xrayutilities Gridder will return a scalar instead of
            # a proper array of any of the dimensions that have length 1. But
            # we need a proper array to store this as a coordinate axis.
            coords[axname] = axvals if len(axvals.shape) > 0 else axvals[None,...]
    
        data_dims = tuple([k for k in coords.keys()])

        da = Dataset(data_vars={result_name: (data_dims, grd_data)},
                     coords=coords)
 
        return da


class LazyQMap(QMapper):
    '''
    QMapper subclass which accepts data at initialization time.

    The idea is to follow up with a later call to a class
    instance (i.e. use the `.__call__()` operator) to trigger a
    Q-space mapping after some processing has been applied.
    To do this, `LazyQMap` stores the data in an internal `xarray.Dataset`
    of its own, the `.xdata` property.
    The raw / authoritative data (i.e. XRD images) is additionally
    accessed by the `.data` property, which behaves like a Python
    `dict()`, while `.angles` gives access to the desginated angles
    (goniometer and detector axes).
    
    The `.__init__()` method requires at least the experimental setup
    to be passed -- see documentation of `.__init__()` for details.
    
    All of the computed data being *lazily* evaluated means that any
    processing that must take place on the raw (i.e. untransformed)
    data can -- and must -- take place before first access to any
    of the `q...` properties. E.g. for intensity normalization, you
    could do simething like: `qmapper.xdata['img'] *= intensity` and
    only then proceed to accessing `.__call__()`.
    '''

    def __init__(self, setup=None, **data):
        ''' Initializes the Q-mapper with default settings, data, or both.

        Args:

            setup: This is expected to be an experiment definition dictionary,
              largely the same as the parameters of `QMapper.init_experiment()`.
              Additionally, this dicttionary also accepts the following keys:
                - `detectorTARAngles`: data for the tilt, azimuth and rotation angles.
                  Only required (and accepted) for angles that are defined as not `None`
                  in the `detectorTARAxes`. The parameter can be one of:
                   - A dictionary with angle name(s) as keys, and data array(s)
                     as values, for each of the directions: tilt, azimuth, and rotation.
                     Only directions with are marked with something different than `None`
                     in `detectorTARAxes` are accepted.   
                   - A tuple of strings (keys) for the corresponding angle names, if
                     the angle data is not supplied separately but is instead included
                     in the `data` container.
                - `goniometerAngles`: similarly to `detectorTARAngles`, this describes the
                  angles by which the goniometer can be positioned.
                  Can be one of:
                    - A dictionary with angle names as keys, and dara arrays as values,
                      from outer-most to inner-mot angle. *All* goniometer angles
                      named in `goniometerAxes` must be listed here.
                    - A tuple with strings, representing data-vars, if angles are
                      not supplied separatetly but within the `data` parameter itself.
                  Order is essential, it must be the same as the axis order in
                  `goniometerAxes`.

            **data: This is a series of named parameters, each containing data
              of the same length in the first dimension. This data can be either
              detector images, angles, or any kind of additional data.
        
        '''

        # Make a clean setup dicitonary which we can pass to superclass:
        #
        #  - filter out angles data (goniometerAngles and detectorTARAngles
        #
        #  - translate Axes (goniometerAxes and detectorTARAxes) to dict(),
        #    containing proper axes names
        #
        #  - (take angle information and store it in the .xdata Dataset)
        #
        
        s = { k:setup[k] for k in filter(lambda x: not x.endswith('Angles'), setup) }
        clean_setup = s.copy()

        # compile angle key list (if we don't have one)
        self._angle_keys = []
        for x in 'goniometer', 'detector':
            self._angle_keys += [k for k in setup[f'{x}Axes'].keys() ] \
                if hasattr(setup[f'{x}Axes'], "keys") else \
                   [k for k in setup[f'{x}Angles']]

        super().__init__(**clean_setup)

        self.xdata = self.__make_dataset(**data,
                                         **(setup['goniometerAngles']),
                                         **(setup['detectorAngles']))

        self._data_keys = tuple([k for k in data])


    @property
    def angles(self):
        ''' dict-based access to all the "angles" fields (mimics old API).
        '''
        return { k:self.xdata[k].values for k in self._angle_keys }


    @property
    def data(self):
        ''' dict-based access to all the "data" fields (mimics old API).
        '''
        return { k:self.xdata[k].values for k in self._data_keys }
    

    def __make_dataset(self, **dsets):
        ''' Creates an `xarray.Dataset` of data sets within `dsets`.
        The first dimension of all `dsets` is required to be the same.
        This is introduced as the first dimension in the `xarray` dataset,
        with the name "index".
        '''
        
        __arrayify = lambda x, n: x if hasattr(x, "__len__") else np.array([x]*n) 

        tmp = next(iter(dsets.items()))
        try:
            if not 'index' in dsets:
                dsets['index'] = np.array(range(tmp[1].shape[0]))

            xdata = Dataset(coords={'index': dsets['index']})
            for k,p in dsets.items():
                if k == 'index':
                    continue
                
                data = __arrayify(p, tmp[1].shape[0])
                dims = ["index"] + [f"{k}_{i}" for i in range(1,len(data.shape))]
                xdata[k] = (dims, data)

        except:
            logging.error(f"Error with dataset: {tmp}")
            raise

        return xdata

    
    def __getitem__(self, label):
        return self.xdata[label]


    def __call__(self, data_key,
                 qsize=None,
                 dims=None,
                 _gridderDict=None,
                 _ang2qDict=None):
        ''' Executes a Q-space mapping on the `data_key` array of the internal `.xdata`.

        Args:
        
            data_key: string with the data variable name to execute the mapping on

            qsize: Grid size(s) for the resulting Q-space map. Unlike the base class's
              `.qmap()` call, this supports only tuples of integers -- no dicts.

            dims: Dimension names to control the mapping. This is a tuple of combintations
              of "qx", "qy" and "qz".

            _gridderDict: update the `.gridderDict` before the mapping (i.e. a dictionary
              with extra parameters to pass to the gridder). This is strongly dependent
              on the unterlying (xrayutilities) implementation.

            _ang2qDict: update the `.ang2qDict` before the mapping (i.e. a dictionary
              with extra parameters to pass to the angular converter).
              This is strongly dependent on the unterlying (xrayutilities) implementation.

        Returns: an `xarray.Dataset` with detector data converted into Q-space,
          see also `super().qmap()` for details (...for which this method is
          typically just a wrapper).
        '''
        
        #valid_kw = { 'qimg', 'dims', '_gridderDict', '_ang2qDict' }
        #for i in kw:
        #    assert kw in valid_kw
        
        if _gridderDict is not None:
            self.setupGridder(**_gridderDict)

        if _ang2qDict is not None:
            self.setupAng2Q(**_ang2qDict)

        # LazyQMap also accepts simple x/y/z values, but QMapper does not.
        # Need to prepend a 'q' in front of single letters.
        if dims is not None:
            dims = tuple([ (f'q{x}' if len(x)==1 else x) for x in dims ])
            
        return self.qmap(self.xdata,
                         angles=self._angle_keys,
                         images=data_key,
                         qsize=qsize,
                         dims=dims,
                         retain="data_vars")


    
## Example for a class that does more than LazyQMap (namely accept angle offsets
## in its constructor), but still uses LazyQMap under the hood.
class OffsetQMap(LazyQMap):
    def __init__(self, offsets=None, **kwargs):
        super().__init__(**kwargs)
        if offsets is not None:
            for k,v in offsets.items():
                self.angles[k] += v
