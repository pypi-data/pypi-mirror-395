#!/usr/bin/python3

import pytest
import nx5d.h5like.fio as p3

@pytest.fixture
def fio_file():
    return 'tests/test_data/fioh5/m3_2507_00744.fio'


@pytest.fixture
def fio_tiff():
    return 'tests/test_data/fiotiff/s1_1161_00484.fio'

def test_fio_parser(fio_file):
    ''' Reading/parsing a FIO file '''
    
    pars, data = p3.read_fio(fio_file)

    assert data['om'].shape[0] == 61
    assert type(pars['om']) == float
    
    #print("Got FIO:", data)

    
def test_fio_loadh5(fio_file):

    fh = p3.FioH5(fio_file)

    assert "fio" in fh.keys()
    
    assert len(fh['fio'].keys()) == 2
    assert len(fh['fio/parameters']) > 10
    assert "om" in fh['fio/parameters'].keys()
    assert "om" in fh['fio/data'].keys()

    assert "lambda_00000" in fh.keys()
    
    a = fh['lambda_00000']['entry']
    b = fh['lambda_00000/entry']

    assert a.keys() == b.keys()

    data = fh['lambda_00000/entry/instrument/detector/mock_data'][()]

    # Very simple test of retrieving the data -- we know this to be the shape
    # of 'mock_data' of the test dataset. Real datasets have a different field
    # ("data") with different shapes, of course.
    assert data.shape == (61, 100, 100)

    assert data.shape[0] == fh['fio/data/om'].shape[0]


def test_fio_loadtiff(fio_tiff):
    
    f5 = p3.FioTiff(fio_tiff, 'fio')

    # This is where we store the TIFF dataset
    assert "fio" in f5
    assert "p100k" in f5['fio']
    assert len(f5["fio/p100k/data"].shape) == 3

    # This is real data, sum is somewhere around 25k or so.
    assert f5["fio/p100k/data"][0:2,...].sum() > 0
