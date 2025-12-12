import time
import numpy as np
import xarray as xr

import itertools

class DatasetFactory:
    '''
    Helper class to ingest data into an `xarray.Dataset`
    '''
    
    def __init__(self, **instr):
        '''
        Args:
            **instr: tag -> dict(path=..., chunk=..., dims=...)
              Where the keys of the instrument setup are as documented
              in `.add_instrument()`.
        '''
        self._instr = instr


    def add_instrument(self, tag, pathfmt, chunk=None, dims=None):
        '''
        Args:
            tag: the name of the data array in the resulting `Dataset`
            path: the location of the data array inside the container
              we're reading from. THIS IS A FORMAT, i.e. you can use
              format keys here that will be substituted by the keyword-args
              data supplied to `.__call__()`.
            chunk: either `None`, `"auto"`, `"scan"` or an integer,
              representing the Dask chunking in the 1st (indexing!) dimension.
              Chunking in the other dimension(s) will always be chosed to fit
              the actual data size.
              The chunking value has the following meaning:
              - 0: no chunking, load all the data at once
              - N: where N is an integer. loads N datapoints per chunk
              - `None` or `"auto"`: perform auto-chunking, i.e. load
                as many data points as we can while still staying below
                a certain threshold (typically in the order of 1M datapoints)
              - `"scan"`: select chunk size based on the size of the first
                scan in the series (see `.__call__()`). If the loading operation
                is performed on a single scan, this is the same as `0`. Otherwise
                this will put each scan into its own chunk, assuming that all
                scans are of the same length of points.
            dims: Name of the dimensions that are NOT the index (i.e. first)
              dimension.
        '''
        self._instr[tag] = {
            'path': pathfmt,
            'chunk': chunk,
            'dims': dims
        }


    def __call__(self, h5like, mode: str = None, **fmtkeys):

        if mode in ('series',):
            return self._build_series(h5like, **fmtkeys)

        elif mode in ('single',):
            return self._build_single(h5like, **fmtkeys)

        elif mode in ('auto', None): # auto-detecting?
        
            for k,v in fmtkeys.items():
                if isinstance(v, list) or isinstance(v, tuple):
                    return self._build_series(h5like, **fmtkeys)
            return self._build_single(h5like, **fmtkeys)


    def _build_series(self, h5like, **fmtkeys):
        
        ## Need to make sure all fmtkeys.values() are lists

        collection = lambda x: x if isinstance(x, list) or isinstance(x, tuple) \
            else tuple([x])
        
        series = {
            k:collection(v) for k,v in fmtkeys.items()
        }
        
        combinations = [
            dict([
                j for j in zip(series.keys(), single)
            ]) \
            for single in itertools.product(*series.values())
        ]

        dset = None
        for single in combinations:
            dnew = self._build_single(h5like, **single)
            #print('dset', dset)
            #print('dnew', dnew)
            if dset is None:
                dset = dnew
            else:
                dset = xr.concat((dset, dnew), dim='index', join='override')

        return dset



    def _build_single(self, h5like, **fmtkeys):

        index_size = None

        ds = xr.Dataset()

        for tag, dset_spec in self._instr.items():
            if isinstance(dset_spec, dict):
                dset = dset_spec['path'].format(**fmtkeys)
                chunks = dset_spec.get('chunk', None)
                dims = dset_spec.get('dims', None)
            else:
                dset = dset_spec.format(**fmtkeys)
                chunks = None
                dims = None

            try:
                dnode = h5like[f'{dset}']
                
                if dims is None and len(dnode.shape)>0:
                    dims = ['index'] + [f'{tag}_{i}' for i in range(1, len(dnode.shape)) ]

                data_size = np.prod(dnode.shape)
                #print(f'Loading: {tag} <- {dset}, shape {dnode.shape}, {data_size}')
            except KeyError as e:
                #print(f'Skipping: {tag} ({dset} not found): {e}')
                continue


            # We expect every value to have an `index_size` sized 1st dimension.
            # As a courtesy, we _also_ accept scalars (shape==() or shape==(1,)),
            # but (maybe?) scale scalars up to (index_size,) arrays of the same value.
            if (len(dnode.shape) == 0) or \
               (len(dnode.shape) == 1 and dnode.shape[0] == 1):
                #if index_size is None:
                #    raise RuntimeError(f'msg="Cannot determine realistic resize target '
                #                       f'of scalar-like value" shape={dnode.shape} '
                #                       f'tag={tag}')

                data = dnode[()]

            # If nodes get too large, or if chunking is explicitly enabled,
            # we store the data as dask arrays
            else:

                # For later use.
                if index_size is None:
                    index_size = dnode.shape[0]

                if (data_size > 1e5 and chunks != 0):
                    if chunks in (None, 'auto'):
                        chunk = int(1e7 / np.prod(dnode.shape[1:]))
                        chunks = (chunk, *(dnode.shape[1:]))
                        #print(f'Auto-chunking: {tag} -> {chunks}')
                    elif chunks in ('scan',):
                        chunk = dnode.shape[0]
                        chunks = (chunk, *(dnode.shape[1:]))
                        #print(f'Auto-chunking: {tag} -> {chunks}')
                    from dask.array import from_array as da_from_array                        
                    data = da_from_array(dnode, chunks=chunks)

                # Regular, unchunked, ndarray data
                else:
                    data = dnode[()]


            if dims is None:
                ds[tag] = data
            else:
                ds[tag] = (dims, data)

        return ds
