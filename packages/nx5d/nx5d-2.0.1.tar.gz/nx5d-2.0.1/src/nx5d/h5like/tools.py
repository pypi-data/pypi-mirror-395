#!/usr/bin/python3

from numpy import array as np_array
import logging

'''
Contains useful tools for working HDF5-like data files (...as opposed to
the rest of the nx5d.h5like submodules, which mostly contain API elements
to *generate* HDF5-like data access.
'''

__all__ = [ "HdfCarver", "DatasetEmpty" ]

class DatasetEmpty(Exception):
    ''' Raised by HdfCarver.__call__() when a specific dataset turns out empty.

    This feature is actually dedicated to `nx5d.scan.ScanReader`, which in turn
    uses slicer generators which are sometimes open-ended (i.e. don't necessarily
    have a *known* maximum number of items to return). Since most indexable
    elements in Python (lists, numpy arrays, HDF5 datasets...) will happily 
    continue returning empty sets when sliced beyond their boundaries, the only
    way of knowing when to stop slicing (e.g. by `.streaks()` of `ScanReader`)
    is for `HdfCarver` to actually signalize the end of data.

    This is done by raising `DatasetEmpty`.
    '''
    pass


class HdfCarver:
    '''A fancy way of reading structured data from HDF5-like objects.
    
    Takes a dictionary which may contain HDF5 paths in the values
    and "restricts" the template by replacing the templated values
    by the data at the corresponding HDF5 path.

    Works recursively on the data, i.e. if the dicitonary contains
    sub-structured data, the structure is retained. All values that
    don't contain HDF5 references are returned verbatim.

    For instance, using this template:
    ```
    {
       "h5data": "@/path/to/dataset",
       "static": 3.14,
       "nested": {
          "static": [3, 4, 5],
          "h5data": "@/path/to/another/dataset",
       }
    }
    ```

    Would return something like this (assuming that "/path/to/dataset"
    and "/path/to/another/dataset" are arrays containing `[1, 2]` and `[3, 4]`,
    respectively):
    ```
    {
       "h5data": [1, 2],
       "static": 3.14,
       "nested": {
          "static": [3, 4, 5],
          "h5data": [3, 4],
       }
    }
    ```
    
    '''
    
    def __init__(self, template, accept=None, paths=None, passthrough=False):
        '''Initialises the carver.

        Args:
        
            template: the configuration template dictionaray

            accept: Places a whitelist restriction on the template
              keys to process and return. This is useful e.g. when
              template dictionaries are to be processed
              only partially. Note that unprocessed keys are _not_
              returned. Default is `None`, which disables the whitelist
              restriction.

            paths: If specified, it's expected to contain a
              for path format substitutes, i.e. this enables the template
              to contain references liek "@{key}", where `{key}` will
              be replaced with whatever is in `paths` at the corresponding
              dictionary slot.

            passthrough: If set to `True`, instead of returning the
              the actual data for HDF5 references, the HDF5-like Python
              container will be returned (e.g. the dataset HDF5 node object).
              This is useful for accessing metadata provided by HDF5 (e.g.
              dataset sizes and shapes) without actually reading out
              possibly large amounts of data. Default is `False`.
        '''
        
        self._tmpl = { k:v for k,v in template.items() }
        self._paths = {k:v for k,v in (paths or {}).items() }
        self._accepted = accept or [k for k in template.keys()]
        self._pass = passthrough


    def __value(self, h5like, value, fmtKeys, slicer=slice(None), **opts):
        '''
        This is the heart of the HDF5 address data lookup system: it checks
        the contents of `value` and returns the corresponding data as expected.
        The trick is in correctly determining the meaning of `value` here.

        The simples assumption here is that `value` is, indeed, a real piece
        of data (i.e. a number or an array with numbers), in which case it
        should be returned verbatim.

        But mostly this isn't the case. `value` might typically differ from
        a pure value in two ways (or any combination thereof):

          1. `value` is a string reference to a path within a HDF5-like
             object (file or node) -- here referenced by `h5like`.

          2. `value` is a container (tuple or dict) that we need to recursively
             descend into and look at each item individually.

        
        For the case of (1), the distinction is the following:
        
          - If `value` is a string that begins with `@`, then it is taken
            as a HDF5 address relative to `h5like`. The string is assumed
            to be a format (e.g. "contain {key}") where the keys to be
            substituted are taken from `fmtKeys`.

          - If `value` is a tuple which's first item is a string that begins
            with "@", and *all* other items are `slice()` objects, then
            the first item of the tuple is assumed to be the HDF5 path
            (as above), but instead of returning the value as-is, it is
            sliced using the provided slicer.

          - Everything else is returned as-is.


        We enter the case of (2) if neither of the above is the case, i.e.
        if `value` is either a dict, or another type of container (tuple
        with different items than (string, slice, ...),

          - If `value` is a tuple that doesn't fit the ("addr", slice()...)
            form, or is a dictionary, we need to recursively call
            `__valyue()` for each of the items.

        
        The function finally returns something that has the same
        structure as `value`, but eventual HDF5 paths are replaced by
        actual data as requested.

        Options:

          nodeOnly: do not return the actual data, just a reference to the
            HDF5 node(s)

          allowEmpty: allow the result of read operations to be an empty
            set (i.e. array of length 0). Otherwise a `DatasetEmpty`
            error is raised when there is no data.
        '''

        my_slicer = slicer

        # Check if value is a fancy ("addr", slice(), ...) tuple.
        # If it is, rewrite `value` to actually contain only the address,
        # and append the slicing part `value` to the slicer argument.
        if isinstance(value, tuple) and \
           len(value)>=2 and \
           (isinstance(value[0], str) and value[0][0] == '@') and \
           np_array([isinstance(v, slice) for v in value[1:]]).all():
            if isinstance(slicer, tuple):
                my_slicer = (*slicer, *value[1:])
            else:
                my_slicer = (slicer, *value[1:])
            value = value[0]


        if isinstance(value, str):
            # The main feature: loading data from HDF5 if we encounter an "@..." string.
            if (len(value) == 0) or (value[0] not in  ['@', '$']):
                return value

            # Only HDF5 addresses prefixed with '@' will be subject to slicing.
            # Prefix '$' will take the data verbatim, no slicing.
            doSlicing = (value[0] == '@')
            
            nodeAddrFmt = value[1:]
            
            try:
                nodeAddr = nodeAddrFmt.format(**fmtKeys)

                node = h5like[nodeAddr]

                logging.debug("Loading data from %s (only node: %r)" % \
                              (nodeAddr, opts.get('nodeOnly', False)))
                
                if opts.get('nodeOnly', False):
                    return node
                else:
                    try:
                        if doSlicing:
                            s = tuple(my_slicer[:len(node.shape)]) \
                                if isinstance(my_slicer, tuple) else my_slicer
                            data = node[s]
                            #print("Slicing %s: %r" % (value, data))
                        else:
                            data = node[()]
                            #print("Not slicing %s: %r" % (value, data))

                        if data.shape[0] == 0 and not opts.get('allowEmpty', False):
                            raise DatasetEmpty
                        
                        return data
                    
                    #except TypeError:  # ...not sure when this happens (?)
                    #    return node
                    except ValueError: # This happens when value is a scalar \
                           # and needs to be sliced by ()
                        return node[()]
                        

            except KeyError as e:
                logging.error("Path substitition error in '%s' for '%s': %s" \
                              % (nodeAddrFmt, value, str(e)))
                raise

            except DatasetEmpty:
                raise
                    
            except Exception as e:
                logging.error("%s: error reading node (%r)" % (nodeAddr, str(e)))
                raise


        # Descending into each of the elements if we encounter python basic
        # data types dict, list, tuple. For everything else, return verbatim.
            
        elif isinstance(value, dict):
            return dict({k:self.__value(h5like, v, fmtKeys, slicer, **opts) \
                         for k,v in value.items()})
        
        elif isinstance(value, tuple):
            return tuple([self.__value(h5like, v, fmtKeys, slicer, **opts) \
                          for v in value])

        elif isinstance(value, list):
            return [self.__value(h5like, v, fmtKeys, slicer, **opts) for v in value]
            
        else:
            return value

        
    def __call__(self, h5like=None, paths=None, slicer=slice(None), **opts):
        '''
        Uses the stored template to generate meaningful content based on the
        data from `h5like`. Typically, this involves going through all the
        templates' values and checking whether they consist of real data
        or H5 paths that need to be read. All paths are relative to `h5like`.

        If `nodeOnly` is set to `True`, the HDF5 nodes at the "nx5:" dataset
        paths is returned. Otherwise the `.value` property is read.

          - `slicer`: If specified, it is applied to any data that is to
            be retrieved from the HDF5-like node, insofar as the data shape
            matches the dimensionality of the slicer; if the slicer has
            too many components (e.g. a 3D-slicer on 1D data), the slicer
            is sliently truncated.        
        '''

        if h5like is None:
            return {k:v for k,v in self._tmpl.items()}

        combinedPaths = {k:v for k,v in self._paths.items()}
        combinedPaths.update((paths or {}))

        retr = {}
        for k,v in self._tmpl.items():
            if k in self._accepted:
                val = self.__value(h5like, v, fmtKeys=combinedPaths,
                                   slicer=slicer, **opts)
                retr[k] = val
                continue

            if self._pass:
                retr[k] = v

        return retr
