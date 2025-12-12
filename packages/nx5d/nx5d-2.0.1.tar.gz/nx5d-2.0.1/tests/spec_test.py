#!/usr/bin/python3

import pytest
from nx5d.h5like.spec import SpecTiffH5

from numpy import isnan

@pytest.fixture
def testfile():

    # Note that, for data storage reasons within the git project,
    # our testfile contains only TIFF data for scan "2.1" and "44.1"
    return "./tests/test_data/spech5/231-cw7-12083-roessle/231-cw7-12083-roessle.spec"


@pytest.fixture
def badfile1():
    # Some TIFFs are missing for scan 44.1 (including the first one).
    return "./tests/test_data/spech5/231-cw7-12083-roessle-missing/231-cw7-12083-roessle-missing.spec"


@pytest.fixture
def badfile2():
    # All TIFFs are missing, and the SPEC data is also missing for scan 3
    return "./tests/test_data/spech5/empty-spec/empty-spec.spec"


def test_spectiff(testfile):

    h5like = SpecTiffH5(testfile)

    assert "2.1" in h5like
    assert "44.1" in h5like

    scan = h5like["44.1"]

    for i in [ "measurement", "instrument" ]:
        assert i in scan

    assert "pilatus" in scan["measurement"]
    assert "data" in scan["instrument/pilatus"]

    d1 = scan['measurement/pilatus']
    d2 = scan['instrument/pilatus/data']

    for i,j in zip(d1.shape, d2.shape):
        assert i == j
        assert j != 0

    assert len(d1) == 41
    assert (d1 == d2).all()


def test_missingtiff(badfile1):

    h5like = SpecTiffH5(badfile1)

    assert "44.1" in h5like

    # There is no data for 2.1. This should result in a NaN scalar.
    tmp = h5like["2.1/measurement/pilatus"]
    assert len(tmp.shape) == 0
    assert isnan(tmp[()])

    # There should be data in 44.1, but some items are missing and
    # should've been replaced by an all-NaN-image. This is true in
    # particular for the first image.
    
    scan = h5like["44.1"]

    d1 = scan['measurement/pilatus']
    d2 = scan['instrument/pilatus/data']

    for i,j in zip(d1.shape, d2.shape):
        assert i == j
        assert j != 0

    # There's only one image in scan "2.1"
    assert len(d1) == 41

    # The first frame was missing, the 2nd was present.
    assert isnan(d1[0]).all()
    assert not isnan(d1[1]).all()


def test_missingcolumns(badfile2):
    h5like = SpecTiffH5(badfile2)

    tmp = h5like["2.1/measurement/pilatus"]


def test_nocache(testfile):

    h5like = SpecTiffH5(testfile, cache=False)
    node = h5like["44.1/instrument/pilatus/data"]

    d1 = node[0:3,0:10,20:30]    
    assert node._is_initialized == False

    data = node[()]    

    d2 = node[0:3,0:10,20:30]

    assert (d1 == d2).all()
    assert node._is_initialized == False    
    
    
