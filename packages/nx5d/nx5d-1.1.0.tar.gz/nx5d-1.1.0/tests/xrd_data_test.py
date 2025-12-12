#!/usr/bin/python

#from nx5d.xrd import data as xd
#from nx5d.xrd import kmc3 as kmc3

import pytest, random

from pprint import pprint

@pytest.fixture
def testfile():

    # Note that, for data storage reasons within the git project,
    # our testfile contains only TIFF data for scan "2.1".
    return "./tests/test_data/spech5/231-cw7-12083-roessle.spec"


#def test_experimentsetup(testfile):
#
#    h5like = kmc3.SpecTiffH5(testfile)
#    
#    templ = kmc3.ExperimentTemplate
#    
#    setupGen = xd.SetupGenerator(templ)
#    setup = setupGen(h5like)
#
#    for i in templ:
#        assert i in setup
#
#    for i in setup:
#        assert i in templ

#    # Test setting of values fpr keys that already exist.
#    ev = random.random()*1000
#    assert xd.SetupGenerator(templ, beamEnergy=ev)(h5like)['beamEnergy'] == ev
#
#    # Test that keys not in template are rejected
#    with pytest.raises(KeyError):
#        xd.SetupGenerator(templ, jinkies=ev)
#    
#    #print("Experiment template:")
#    #pprint(templ)
#    #print("Experiment definition:")
#    #pprint(setup)
