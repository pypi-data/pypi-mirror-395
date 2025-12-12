#!/usr/bin/python3

from nx5d.streaks import Pabst
from nx5d.h5like.pypod import concat_h5
import pytest
from numpy import array as np_array
from h5py import File

def make_h5ex():
    '''Returns a HDF5 object with virtual data.'''
    data = {
        "idx": np_array(range(100)),
        #"moo": np_array(range(300)).reshape(100,3)
    }

    h5 = File("/dev/null", "a", driver="core", backing_store=False)
    concat_h5(h5, data)

    return h5

@pytest.fixture
def h5ex():
    return make_h5ex()


#def test_data(h5ex):
#    assert "moo" in h5ex.keys()
#    assert "idx" in h5ex.keys()


def test_pabst(h5ex):

    #with h5ex as h5:
    #    print([k for k in h5.keys()])        
        #with h5 as h:
        #    print([k for k in h.keys()])
        #print([k for k in h5.keys()])

    #print(h5ex.keys())

    pbs = Pabst(moo="@/moo", idx="@/idx").moo(idx=3)
    #pbs = Pabst(idx="@/idx").moo(idx=3)

    #tmp = pbs(h5ex)
    #return tmp

    #print(tmp)
