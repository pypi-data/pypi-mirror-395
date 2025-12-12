The `nx` module
---------------

Quick n'dirty way of converting a ESRF Runlog File with associated EDF files
to HDF5/Nexus:
w```
$ ./nx5d/nx.py ~/my-experiment/run03/run03.log ~/run03.hdf5
```

The resulting HDF5 can be loaded e.g. with
[PyMCA](http://pymca.sourceforge.net/).

Note that this kind of data saving (i.e. via a Reflog file) is obsolete.
The corresponding beamline at ESRF has switched to a more ESRF-esque Nexus
file format, provided via their in-house
[beamline control system](https://www.esrf.fr/BLISS). While the `nx` module may
still be useful for legacy data, the preferred way of dealing with ESRF data
post-2022 within the `nx5d` framework is using
[the `DataSource` module](#the-datasource-module).
