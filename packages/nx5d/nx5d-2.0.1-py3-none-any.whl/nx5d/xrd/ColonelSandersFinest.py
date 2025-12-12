#!/usr/bin/python3

def stop_series(start=-200, shape=(8,10), step=2, pval=0):
    '''
    Creates a series of size NxM (for `shape=(N, M)`) values starting
    at `start` and with a step of `step`, but includes a "stop" value
    of `pval` every `period` entries.
    
    For example:
       stop_series(start=1, stop=9, period=3)
       
       -> `[1, 2, 3, 0,  4, 5, 6, 0,  7, 8, 9, 0 ]` 
       
    Returns: An array with lenth `(N+1) * M`, containing values with `step`
    increment starting from `start`, interseded with values of `pval`.
    '''
    ts  = start+np.array(range(0, (shape[1]*shape[0])))*step
    ts2 = ts.reshape(shape[::-1])
    cat =  np.concatenate((ts2, pval*np.ones([shape[1]])[:,None]), axis=1)
    
    return cat.flatten()