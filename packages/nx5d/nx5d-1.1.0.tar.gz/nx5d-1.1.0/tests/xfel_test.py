#!/usr/bin/python3

import extra_data as ex
import nx5d.h5like.xfel as xfel

import pytest

# Unit test for the XFEL data module (mostly nx5d.h5like.xfel).
# Needs XFEL data and API, predominantly extra_data.
# Tests therefore only work within the XFEL environment.
#
# Call with 'pytest -m xfel'

@pytest.fixture(scope="class")
def xfel_test_run():
    '''Which dataset to use for unit testing'''
    
    return { 'proposal': 3491,
             'run': 149,
             'data': 'all' } # proposal, run


@pytest.fixture(scope="class")
def xfel_test_data(xfel_test_run):
    '''Selection to use for unit testing (from dataset above)'''
    
    run = ex.open_run(**xfel_test_run)
    return run.select([
        ('MID_DET_AGIPD1M-1/DET/*CH0:xtdf', '*'),
        ('SA2_XTD1_XGM/XGM/DOOCS:output', '*'),
        ('MID_EXP_EPIX-1/DET/RECEIVER:daqOutput','*'),
        ('MID_EXP_SAM/MDL/DOWNSAMPLER', '*')
    ])


@pytest.mark.xfel
class TestExdatH5:
    @pytest.fixture(scope="class", autouse=True)
    def exdat_h5(self, xfel_test_data):
        '''Returns an ExdatH5 instance for testing'''
        return xfel.ExdatH5(xfel_test_data)

    @pytest.fixture(scope="class")
    def simple_dataset(self, exdat_h5):
        ''' Returns a 'simple' data set'''
        return exdat_h5["/instrument/selection/SA2_XTD1_XGM/XGM/DOOCS:output/data.xTD"]

        
    def test_xgm_available(self, exdat_h5):
        assert "instrument" in exdat_h5
        node = exdat_h5["/instrument/selection/SA2_XTD1_XGM/XGM/DOOCS:output"]
        #print (node.keys())
        
        assert "data.xTD" in node
        data = node['data.xTD']
        #print(data.shape)

        
    def test_slicing(self, simple_dataset):
        '''Tests simple slicing and arithmetics on a dataset'''
        
        subdata = simple_dataset[13:15]
        #print(subdata.shape)
        assert len(simple_dataset.shape) == 2
        assert len(subdata.shape) == 2

        nr = subdata.sum()
        nr2 = (subdata*2).sum()
        assert (nr*1.9 < nr2) and (nr*2.1 > nr2)


    def test_multimod_detect(self, exdat_h5):
        '''Discovery of multimodal detectors.
        '''

        # Step 1: Multimodal data should *not* be available at "measurement/$PATH/" anymore
        with pytest.raises(KeyError):
            regular = exdat_h5["/instrument/MID_DET_AGIPD1M-1/DET/"]

        with pytest.raises(KeyError):
            regular = exdat_h5["/instrument/selection/MID_DET_AGIPD1M-1/DET/"]

            
        # Step 2: Dedicated detector entries should be at "instrument/$DETECTOR/...",
        # and detector images linked to "measurement/$DETECTOR"
        det = exdat_h5["/instrument/multimod/MID_DET_AGIPD1M-1"]
        img1 = det['image.data']
        assert len(img1.shape) == 4 # train_pulse, module, w, h

        
    def test_multimod_slice(self, exdat_h5):
        '''Slicint on multi-module data (necessary because this
        is a different Dataset codebase). This will take a loooong time.
        '''
        img = exdat_h5["/instrument/multimod/MID_DET_AGIPD1M-1/image.data"]

        subdata = img[13:29]
        #print(subdata.shape)
        assert len(subdata.shape) == len(img.shape)
        assert subdata.shape[1:] == img.shape[1:]

        nr  =  subdata.sum()
        nr2 = (subdata*2).sum()
        assert (nr*1.9 < nr2) and (nr*2.1 > nr2)
