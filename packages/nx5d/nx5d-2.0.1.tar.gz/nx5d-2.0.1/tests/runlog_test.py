
#
# Testing only below this point
#
import pytest
from io import StringIO

from nx5d.runlog import RunlogFile

def test_header_standard():
    '''
    Tests the "key: value" header setup. The "*_simple.log" files
    are straight-forward, no surprises; the regular files may contain
    empty lines and/or leading spaces and other non-breaking format
    "impurities". They all have to pass
    '''

    for fname in [
            './tests/test_data/runfile/run105_simple.log',
            './tests/test_data/runfile/run105.log' ]:
        r = RunlogFile(None)
        f = open(fname)
        result = r._consume_header(f)
        assert len(result[0]) == 17

        # These are just a few, feel free to extend:
        for i in [ "sample 4", "source", "sample slits" ]:
            assert (i in result[0].keys())

        assert int(result[0]["pulses per image"]) == 1000


def test_data_standard():
    '''
    Tests proper loading of data. We do this by initializing the
    object as-is, but we only care about integrity of the data
    part.
    '''
    for fname in [ ]:
        r = RunlogFile(fname)
        assert len(r.keys()) == 12


def test_header_broken():
    '''
    Loads test file(s) with broken headers / attrs and checks
    for proper error reporting.
    '''
    pass


def test_broken_data():
    '''
    '''
    pass
