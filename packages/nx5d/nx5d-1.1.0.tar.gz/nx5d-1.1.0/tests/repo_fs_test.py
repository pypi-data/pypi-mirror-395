from nx5d.repo.filesystem import FilesystemWalker, DataRepository
from os import path

def test_walker():
    w = FilesystemWalker('./tests/test_data/udkm/{key}', glob='20??/20??????')
    assert len(w.keys()) > 0

    w = FilesystemWalker('./tests/test_data/spice/{key}')
    print(w.keys())

    
def test_repo1():
    r = DataRepository(url=path.abspath('./tests/test_data/udkm/{proposal}/{scan}'),
                       glob='20??/20??????',
                       proposal_k2h=lambda x: f'p{x[7:]}')
    print('proposals in repo:', r.all())
    assert len(r.all()) > 1
    assert '2025/20250408' in r.all()

    
def test_scan1():
    pass
