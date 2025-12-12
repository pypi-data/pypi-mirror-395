#!/usr/bin/python3

import numpy as np

class RunlogFile():
    '''
    This is meant for "what is what" logfile which accompanies EDF data,
    apparently written at some ESRF facilities.

    The logfile format is essentially a TSV (tab separated values) file
    with a header line for field naming. What we're doing is exposing this
    as a "flat" HDF5-like object where each column of the logfile corresponds
    to a data container.
    '''

    def _consume_header(self, fobj):
        '''
        Returns the header `(attribues, column)` from the top of the
        file object `fobj`
        The "attributes" are `key: value` pairs at the beginning, and the
        "column" tags are the last line before the data section.
        The corresponding lines are consumed from `fobj`.
        '''

        attrs = {}
        header_candidate = None
        
        # First read the header
        while True:

            _line = fobj.readline()
            if not _line:
                raise RuntimeError("Premature end of file")
            
            line = _line.strip()
            
            if line[0] == '#':
                if len(line) == 1:
                    # skipping lines with a single '#'
                    continue
                header_candidate = line
                
            tmp = line[1:].split(':')

            if len(tmp) == 0:
                continue
            
            elif len(tmp) == 2:
                # Trying to parse tmp[1] as a number would be cool, but the
                # data crammed in there -- even when numerical -- is a mess
                # of units, information etc. Not really meant to be parsed.
                attrs[tmp[0].strip()] = tmp[1].strip()
                
            elif len(tmp) == 1:
                header = []
                for h in header_candidate[1:].split(' '):
                    if len(h) > 0:
                        header.append(h)
                return attrs, header
            
            else:
                raise RuntimeError("Confused by header line: '%s'" % line)


    def _consume_data(self, fobj, columns, dtype_map='auto'):
        '''
        Parses data, line by line, and stores it into a dictionary where
        the keys are strings from `columns`, values are 1D `numpy.ndarray`,
        objects and the entries in the ndarray are the numbers coresponding
        to each data file line.

        Parameters:
          - `fobj`: is a file object created by `open()` (NOT a file path)
          - `columns`: This is a list of string, containing the name of the data
            columns. It must be as long as there are items in each line.
          - `dtype_maps`: This is an optional column name -> numpy-dtype map for
            the data. If specified, it will be used to transform the data from
            string to whatever this map specifies. If set to None, no transformation
            will take place. In the default value of `'auto'`, this function tries
            to autodetect integer and floating point data, leaving everything
            else as strings.
        '''

        data = {}
        for c in columns:
            data[c] = [] 

        line_no = 0
        while True:
            _line = fobj.readline()
            if not _line:
                break

            line_no += 1

            line = _line.strip()

            index = 0
            for val in line.split(' '):
                if len(val):
                    try:
                        data[columns[index]].append(val)
                        index += 1
                    except IndexError as e:
                        raise RuntimeError("%s: have %d columns, but %d data fields" %
                                           (str(e), len(columns), index))
            
            if index != len(columns):
                raise RuntimeError("Too few items in line HEAD+%d(found %d, expecting %d):"
                                   " \"%s\"" % (line_no, index, len(columns), line))

        # At this point we have a dictionary of data lists full with strings.
        # We'd rather have "proper" data, i.e. floats, dates, timestamps etc.
        for col in columns:
            l = data[col]
            a = np.array(l, dtype=str)
            final_a = None

            if isinstance(dtype_map, map):
                try:
                    final_a = np.array(a, dtype=dtype_map[col])
                except:
                    pass
            elif dtype_map == 'auto':
                try:
                    final_a = np.array(a, dtype=int)
                except:
                    try:
                        final_a = np.array(a, dtype=float)
                    except:
                        final_a = a
            
            data[col] = final_a if final_a is not None else a

        return data
        

    def __init__(self, f, mode='r', dtype_map='auto'):
        '''
        Opens the Logfile specified by `f` with specified `mode`
        (currently only opening for reading, `mode='r'`, is accepted).
        The optional parameter `dtype_map` specifies how to interpret
        data columns in a column name -> numpy dtype map. If set to
        `None`, data is left as string. If left on its default value
        (`auto`), interpretation as integer is first attempted, followed
        by floating point arrays. Fallback is string.
        '''

        # This constructs a mostly empty / dysfunctionsl object.
        # Used for unit testing.
        if not f:
            return
        
        if mode != 'r':
            raise RuntimeError("EdfLogFile: only reading supported (requested: %s)" % mode)

        if not hasattr(f, "readline"):
            f = open(f)

        self.__attrs, self.__columns = self._consume_header(f)
        self.__data                  = self._consume_data(f, self.__columns)


    def __getitem__(self, column):
        '''
        Returns the data array of the specified column. The column may be
        specified as "name" or "/name", to mimic HDF5 path specifications.
        '''
        if column[0] == '/':
            col = column[1:]
        else:
            col = column

        return self.__data[col]


    def __setitem__(self, column, data):
        '''
        Sets the column data at once. No checks for data type or length are performed.
        '''
        if column[0] == '/':
            col = column[1:]
        else:
            col = column
            
        self.__data[col] = data


    def keys(self):
        '''
        Returns a list with all column names.
        '''
        return self.__columns

    
    def values(self):
        '''
        Returns a list with all the data vectors.
        '''
        return self.__data.values()


    def items(self):
        '''
        Simialr to dict().items()
        '''
        return self.__data.items()
    

    @property
    def attrs(self):
        '''
        Returns the list of key: value pairs at the top of the index file (as a map)
        '''
        return self.__attrs

    @attrs.setter
    def attrs(self, a):
        self.__attrs = a
            
#
# This is for more convenience during development. This may or
# may not fit anyone besides the main developer ¯\_(ツ)_/¯
#
from sys import argv, exit

if __name__ == "__main__":
    
    if len(argv) < 2:
        print("Test usage: %s file.log" % argv[0])
        exit(-1)

    print ("From logfile: %s" % argv[1])
    l = RunlogFile(argv[1])

    for k in l.keys():
        print ("Column: %s, %d items, %r" % (k, len(l[k]), l[k].dtype))
