#!/usr/bin/python3

import logging

""" Facilitate HDF5 simulation and generation from "plain" Python data.

Nx5d data models evolve around the HDF5 API. This module is dedicated
to exposing the result of data processing, i.e. plain Python data,
numpy-(like-)arrays etc, as h5py-like objects. The simplest way of doing
that is *actually* storing those data in true h5py HDF5 file -- be they
in memory (`h5py.File(... driver='core')`) or on-disk.

The straight-forward method of doing that is invoking `concat_h5()`
from this module, which adds a dataset, or a subtree (referenced by
a python `dict`) in a h5py file. Compatible with the nx5d *Scan/Streak/Frame*
mindset, the `concat_h5()` method concatenates new data to already existing
datasets, along the first dimension.
"""

def concat_h5(h5like, data, path="/", dset_args=None):
    ''' Concatenates the data from `data` into the HDF5-like `h5like`.

    The concatenation is done by *actually* extending an existing dataset along
    its first dimension. For this, the data to be concatenated needs to have
    matching sizes in all other dimensions (and in particular have the same
    dimensionality) as the existing dataset.

    Apparently nother way how this could've been achieved is by storing the
    incoming datasets separately and (re-)creating a virtual dataset over
    and over again.

    Args:
        h5like: a `h5py.File` like object.

        data: a set of possibly nested Python containers containing data.
          As such, `data` might be:
          - An array-like (in which case `path` needs to be something different
            than the default "/", and this is treated like a single dataset)
          - An enumerable (in which case we don't know what to do with it,
            but we feel like we should to *something*, so there's that...)
          - A dictionary / hashable, in which case this function is recursively
            called for every item, replacing `path` by the hashable key,
            and `data` by the hashable value)

        path: The path at which to insert `data` within the HDF5 object.
          If `data` is an array-like, it is concatenated to the possibly
          existing dataset at `path` along the first dimension. If it
          is a hashable, then `path` is expected to be an HDF5 group node
          (or is created as one, if it doesn't already exist) under which
          to create datasets as instructed by the hashable.

        dset_args: Keyword arguments to pass to `h5py.Group.create_dataset()`
          when creating new datasets. This is `None` by default, meaning that
          no extra parameters will be passed. But subsequently adding datasets
          -- which is the primary scope of this function -- requires HDF5
          datasets to be created as chunked, and to have `maxshape` in the
          required dimension set accordingly. For this reason, `concat_h5()`
          will automatically assume `maxshape=(None, ...)` if nothing else
          is specified for `maxshape`, which will also automatically enable
          chunking (according to h5py documentation).

    Returns: `None`

    Raises:
    
        - `TypeError` if any of the required nodes already exits in the HDF5-like
          but is not of the expected type (dataset or group), or of a compatible
          shape
    
        - Any exception which `h5py.Group.create_dataset()` or `.resize_dataset()`
          might also raise, in particular `RuntimeError` if parameters are not
          compatible, e.g. the datasets are initially created without the ability
          to be extended.
    '''

    if dset_args is None:
        dset_args = {}

    if data is None:
        # Special case: ignore datasets that are 'None'. This is mainly
        # a feature for unit testing, but it's also sensible behaviour.
        return
    
    elif hasattr(data, "shape"):
        try:
            dset = h5like[path]
            
            if not hasattr(dset, "shape"):
                raise TypeError("%s exists in HDF5-like and is expected to be a "
                                "dataset, but it isn't" % path)

            if dset.shape[1:] != data.shape[1:]:
                raise TypeError("%s exists in HDF5-like but has shape %r incompatible with %r " % \
                                (path, dset.shape, data.shape))

            new_size = dset.shape[0]+data.shape[0]
            
            logging.debug("Extending dataset '%s' in '%s' to %d" % (path, h5like.name, new_size))
            dset.resize(new_size, axis=0)
            dset[-data.shape[0]:] = data[:]
            
        except KeyError as e:
            # dataset does not yet exist -- we're creating it.
            logging.debug("Creating dataset '%s' in '%s'" % (path, h5like.name))

            # If the user didn't specify anything else, we make the dataset
            # infinitely extensible in the 1st dimension.
            max_shape = tuple([None] + [i for i in data.shape[1:]])
            create_args = dset_args.copy()
            create_args.setdefault('maxshape', max_shape)
            h5like.create_dataset(path, data=data, **create_args)

    else:
        try:
            group = h5like[path]
        except KeyError:
            # need to create group first
            split = path.rsplit('/')
            h5base = h5like if len(split) == 1 else h5like['/'.join(split[:-2])]

            logging.debug("Creating group '%s' in '%s'" % \
                          (split[-1], '/'.join(split[:-2])))
            
            group = h5base.create_group(split[-1])
        
        for k, v in data.items():
            concat_h5(group, v, path=k, dset_args=dset_args)
