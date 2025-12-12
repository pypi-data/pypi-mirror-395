#!/usr/bin/python3

import nx5d.ingest as ingest
import h5py, pytest, os, tempfile, numpy
from pathlib import Path

def test_h5path():

    assert ingest.H5DataSink('/path/to/h5').file_path == Path('/path/to/h5')
    
    assert ingest.H5DataSink('/path/to/h5#group').file_path == Path('/path/to/h5')
    assert ingest.H5DataSink('/path/to/h5#group').group_path == 'group'
    
    assert ingest.H5DataSink('/path/to/h5::group').file_path == Path('/path/to/h5')
    assert ingest.H5DataSink('/path/to/h5::group').group_path == 'group'

    # This is actually not ambiguous, by definition we let '#' have
    # precedence over '::'
    assert ingest.H5DataSink('ambi::guo#us').file_path == Path('ambi::guo')
    assert ingest.H5DataSink('ambi::guo#us').group_path == 'us'
    assert ingest.H5DataSink('ambi#guo::us').file_path == Path('ambi')
    assert ingest.H5DataSink('ambi#guo::us').group_path == 'guo::us'

    with pytest.raises(ingest.IngestUrlError):
        ingest.H5DataSink('fa##il')


def test_scan():

    with tempfile.TemporaryDirectory() as tmp:
        hfile = os.path.join(tmp, "scan.h5::node")
        sink = ingest.H5DataSink(hfile)
        scan = sink.open_scan(1)


def test_device():
    with tempfile.TemporaryDirectory() as tmp:
        hfile = os.path.join(tmp, "device.h5::node")
        sink = ingest.H5DataSink(hfile)
        scan = sink.open_scan(scan=1,
                              detector={'shape': (256, 512), 'dtype': 'f'},
                              angle={'shape': tuple(), 'dtype': 'f'})

        #print(f'Devices: {scan.devices}')

        with h5py.File(sink.file_path, 'r') as h5:
            for d in scan.devices:
                dset = h5[f"/node/1.1/measurement/{d}"]
                #print(f'{d} data: {dset.shape}')
                assert dset.shape[0] == 0
            assert len(h5[f"/node/1.1/measurement/angle"].shape) == 1
            assert len(h5[f"/node/1.1/measurement/detector"].shape) == 3
        
        scan.append({
            'detector': numpy.ndarray((256, 512)),
            'angle': numpy.array(3.14)
        })

        with h5py.File(sink.file_path, 'r') as h5:
            for d in scan.devices:
                dset = h5[f"/node/1.1/measurement/{d}"]
                #print(f'{d} data: {dset.shape}')
                assert dset.shape[0] == 1

        # We only accept a full set of data with every .append() call
        with pytest.raises(KeyError):
            scan.append({
                'angle': numpy.array(6.28)
            })
