The `DataSource` module
-----------------------

### The NX5 data model

The `DataSource` module of `nx5d` assumes that the experimental data consists
of several measurement parameters (angles, temperatures, delay times, detector
images etc) which are all accessible via an HDF5 file interface. While the
package was developed with peculiarities of the Nexus standard in mind, it
makes no assumptions about the actual Nexus compliance of those files.
Quite generally, the experimental data is expected to:

  - represent a series of unrelated scans, a single-parameter scan
    (e.g. angle dependent detector images), or multi-parameter scan
    (i.e. angle-delay time),
  - be at distinct paths within the HDF5 file, one path per measurement
    parameter or result (e.g. angle or detector image)
  - be cotained within *one* HDF5 dataset for *all* the parameters
    of one measurement series (as opposed to: split across several
	datasets, e.g. one dataset per parameter)
  - contain the series dimension / counter as the *first* (a.k.a. outermost)
    dimension, if a particular parameter is not a scalar (e.g. a 2D detector
	image per scan).
	
One single HDF5 may contain arbitrarily many measurement sets, as
long as there are provided means of separation of their data sets.
	
Here's an example of an ESRF-compatible HDF5 data file layout:

  - `S01/measurement/rayonix`: 3-dimensional dataset, with dimensions
    being [`frame-nr`](#nx5d-terminology) x `width` x `height`.
  - `S01/instrument/positioners/hphi`: a 1-dimensional array (with `frame-nr`
    elements) for the Phi angle of a goniometer
  - `S01/instrument/positioners/lxt_ps`: a 1-dimensional array (of `frame-nr`
    length) specifying a delay time
  - `S01/measurement/sbcurr`: a 1-dimensional array (again, `frame-nr` size)
    with ring current values).


### `nx5d` terminology

We are using the following terms:

  - *data frame*: the result of one particular experimental data
    acquisition step, i.e. one image at one specific set of angles,
	one temperature, one delay time etc.
	
  - *scan*: systematic variation of measurement parameters, e.g.
    moving to specific sets angles, one position after the other.
	A scan may be 1-dimensional or linear if one specific set of
	parameters is moved from positian A in parameter space to
	position B; or it can be N-dimensional or rasterized if the
	parameters move in a raster-like manner.
	
  - *data set*: several data frames that are somehow related, e.g.
    all the frames that result from acquiring data at each position
	of a scan.


### Using `DataSource` to read data

A `DataSource` object represents one specific scan We need a file
name and a HDF5 path within that file:

```
>>> from nx5d.scratch.source import DataSource
>>> src = DataSource("/path/to/file.h5", "S01")
```

The `src` object will open the file, possibly try to read specific
experimental parameters like beam energy, center pixel location etc,
and save the (filepath, scanpath) tuple for later use. (As a general
policy `nx5d` will not keep the data files open longer than necessary
to allow analysis during continuous measurement mode.)

#### Reading data in "manual mode"

To access data, we need to define a dictionary of the datasets
we're interested in. Then we can proceed to read out data frames
using [Python `slice` objects](https://docs.python.org/3/c-api/slice.html):

```
>>> frmap = {
...  "img":   lambda s: "measurement/rayonix",
...  "hphi":  lambda s: "instrument/positioners/hphi",
...  "delay": lambda s: "instrument/positioners/lxt_ps"
... }
>>>
>>> data = src.read(slice(0,10), addrproc=frmap)
{
  "img": [ndarray(...), ndarray(...), ...],
  "hphi": [value, value, ...]
  "delay": [value, value, ...]
}
```

The result of this operation will be a data dictionary (here `data`)
containing the same keys as the dataset dictionary we used as 
input, and they value to each key being an array of corresponding
values from the HDF5 file. `DataSource` is (mostly) very unopinionated
about the contents of the datasets, it will simply return what it
sees: if the HDF5 field was, for instance, a 3D dataset, the resulting
data item will be a 2D image; if it was a 1D array, the item will be
a scalar value.

Here we requested 10 items (via the object `slice(0,10)`), so what
we obtain is an array containing just as many entries.
The angle `data["hphi"][0]` belongs to image `data["img"][0]`
and so on.

### Reading data in "chunked mode"

Another, more useful, way to obtain data is not to read it frame
by frame, but to allow the `DataSource` to chunk it together
according to the experiment we were performing.

Let's assume, for instance, that we've performen an experiment
with Phi values between 10 and 14 (increment of 1 degree), and
with delay times between 0 and 4 (increment of 1 ps). Then
our data is structured as follows:

  - *Images* as a list of 25 images: `[ndarray(), ndarray(), ...]`
  - *Angles* as a list of 25 angles, repeating as as 5 ramps:
     `[10, 11, 12, 13, 14, 10, 11, ... 10, 11, 12, 13, 14]`
  - *Delay times* as a list of 25 times, repeating tuples of 5x the same
    delay time:
     `[0, 0, 0, 0, 0, 1, 1, ... 4, 4, 4, 4, 4]`.

This is because of the scanning / rastering nature of the experiment.

We can now read chunks of data that belong to the same delay time,
but different angles, as follows:

```
>>> chunks = [ c for c in src.chunks(length=5, addrproc=frmap) ]
[ Chunk(), Chunk(), ... Chunk() ]
>>>
>>> len(chunks)
5
```

We obtain "data chunks". One such data chunk is a specifc object
(`DataSource.Chunk`) which encapsulates the data map (e.g. via
the `Chunk.data[...]` member and offers a number of extra members:
  
  - a `qimg` member, which is a representation of the data found
    in the `"img"` part of the data map, but transformed into Q
	coordinates according to the angles. This uses the
	[Gridder classes](https://xrayutilities.sourceforge.io/examples.html#using-the-gridder-classes) of XrayUtilities; this means that the `qimg` member always
	returns one single image containing all the images of this chunk
	superimposed on one another according to their correct Q
	coordinates.
	
  - `qxaxis` and `qyaxis` members, which represent the coordinate
    axes along one, respectively the other detector axis. Note
	that these may or may not be the *real* Qx and Qy axis, depending
	on your experiment geometry.
	
The Q representation is lazily evaluated, i.e. calculated on the first
access of either of the `qimg`, `qxaxis` or `qyaxis` parameters, and
cached thereafter.

Note that part of the guaranteed API behavior is that the underlying
data (images or angles) can be altered *before* the first call to any
of the `q` members; in that case the altered data will be the basis
for transformation. This is e.g. useful when background processing
(substracting, normalization etc) is to be performed before the Q
transformation.

Substraction of an intensity offset of 10 counts, for instance,
would work like this:
```
>>> chunks = [ c for c in src.chunks(length=5, addrproc=frmap) ]

>>> intensity_offset
>>> for c in chunks:
...    for i in c.data['img']:
...        i -= intensity_offset

>>> [ c.qimg for c in chunks ]
```

Once the calculation of Q data of a specific `Chunk` has been triggered,
there is no way to trigger a recalculation with altered data. You need
to re-read the chunk from its corresponding `DataSource`.

#### Bugs and pitfalls

Currently (August 2022) this is working code, but still only as
proof-of-concept kind of thing. It is *highly* tailored to the ID09
beamline of ERSF. Specific internals of the `DataSource` and `Chunk`
implementatino make use of "folklore" about data naming and layout
schemes, and initialisation of the corresponding XrayUtilities `Experiment`
object for angle transformation.

You *will* have to dig heavily into the code to adapt it for other
beamlines. That said, the code is fairly short, so success is likely :-)

One of the immediate next steps planned for `nx5d` is better generalisation
of the experimental layout to make adaptation to other beamlines easy.


### XRD helpers

Functions in `nx5d.scratch.xrd_helpers` implement helpers for statistical
data analysis, e.g. calculating center of mass and
[statistical variance](https://en.wikipedia.org/wiki/Variance#Discrete_random_variable)
of coordinates. These may be useful for peak position analysis without
the need of a specific fitting method.


### Other useful code snippets

Be sure to try the `Roi` class from `nx5d.scratch.roi`. Essentially,
it allows to define a region-of-interest in N dimensions and easily
obtain a (set of) slicing object(s) to access the data within
that region of interest:

```
>>> from nx5d.scratch.roi import Roi
>>> data = range(100)
[0, 1, 2, ... 100]

>>> r = Roi (start=10, end=20)
>>> data[r.s]
[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

>>> r = Roi (center=50, size=5)
>>> data[r.s]
[ 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
```
