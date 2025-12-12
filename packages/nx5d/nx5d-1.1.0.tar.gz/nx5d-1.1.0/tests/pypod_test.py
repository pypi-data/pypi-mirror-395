#!/usr/bin/python3

import pytest
import h5py
from numpy import array as np_array

from nx5d.h5like.pypod import concat_h5

def test_concat_h5_groups():
    # Tests the group creating / hierarchy
    
    h5 = h5py.File('/dev/null', 'w', driver='core', backing_store=False)

    # Test adding folders
    concat_h5(h5, { "jinkies": None })
    with pytest.raises(KeyError):
        # dataset "jinkies" is None, supposed to not exist
        assert h5['jinkies']

    # Test adding datasets
    concat_h5 (h5,
               { "jinkies": { "scooby": np_array(range(17)) } })

    assert h5['jinkies']
    assert h5['jinkies/scooby']

    s = h5['jinkies/scooby']
    assert len(s.shape) == 1
    assert s.shape[0] == 17

    # Test extending datasets
    concat_h5 (h5, { "jinkies": { "scooby": 17+np_array(range(23)) } })
    s = h5['jinkies/scooby']
    
    assert len(s.shape) == 1
    assert s.shape[0] == 17+23

    for i,j in zip(s,range(40)):
        assert i == j

    # Test adding and extending multidimensional datasets
    concat_h5(h5, {"boron": {"theMoron": np_array(range(20)).reshape(4,5)}})
    concat_h5(h5, {"boron": {"theMoron": np_array(range(30)).reshape(6,5)}})

    s = h5["boron/theMoron"]

    assert s.shape == (10, 5)
            

@pytest.fixture
def test_concat_hetero():
    '''Returns a HDF5 object with virtual data.'''

    data = {
        "idx": np_array(range(100)),
        "moo": np_array(range(300)).reshape(100,3)
    }

    h5 = h5py.File("/dev/null", "a", driver="core", backing_store=False)
    concat_h5(h5, data)

    return h5

