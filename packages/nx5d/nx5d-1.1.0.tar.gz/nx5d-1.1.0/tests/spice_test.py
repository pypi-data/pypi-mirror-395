import pytest, json, glob, os, pprint
from nx5d.spice import  spice_schema, FsSpiceRepository, SpiceCollection, \
    SpiceView, SpiceRevisionConflict, BranchView, MemorySpiceRepository, \
    SpiceProposal

def test_load():
    base = os.path.abspath('./tests/test_data/spice/pack1')

    col = SpiceCollection()
    
    for p in glob.glob(f'{base}/*'):
        with open(p, 'r') as f:
            data = json.load(f)
            col.add(data)

    vs = col.view("r01", 'straight')
    assert hasattr(vs, "straight")
    assert hasattr(vs.straight, "param")
    assert vs.straight.param == 3.14

    with pytest.raises(SpiceRevisionConflict):
        vc = col.view("r01", 'conflicted')

    v = col.view("r01", ignore_conflict=True)
    assert hasattr(v, 'straight')
    assert hasattr(v, 'conflicted')

    assert isinstance(v.straight, BranchView)
    assert isinstance(v.conflicted, tuple)
    assert len(v.conflicted) > 1

    assert isinstance(v.conflicted[0], BranchView)

    print (v.straight.meta())
            
    v2 = col.view("r05", 'straight')
    v3 = col.view("r10", 'straight')

    assert v2.straight.param == vs.straight.param
    assert v3.straight.param != vs.straight.param

    print(v2.straight)
    print(v3.straight)
    
    # Test retrieving the seed
    s1 = col.view(None, 'straight')
    print('anchor:', s1)

    
def test_fs_spice():
    sr = FsSpiceRepository(os.path.abspath('./tests/test_data/spice/{proposal}'))
    scan1 = sr.pack1.collection.view("r01", ignore_conflict=True)

    assert "straight" in sr.pack1.collection.handles()
    assert hasattr(scan1, "straight")


def test_find():
    sr = FsSpiceRepository(os.path.abspath('./tests/test_data/spice/{proposal}'))
    
    f = sr.pack1.collection.find(startswith=True, uuid='f965')
    assert len(f) == 1

    f2 = sr.pack1.collection.handles('straight')
    pprint.pprint(f2)


def test_memrepo_empty():
    repo = MemorySpiceRepository()
    assert len(repo.all()) == 0

    repo.new('myprop')
    assert 'myprop' in repo.all()
    
    p = repo.myprop    
    assert isinstance(repo.myprop, SpiceProposal)


@pytest.fixture
def memrepo():
    t = FsSpiceRepository(os.path.abspath('./tests/test_data/spice/{proposal}'))
    return MemorySpiceRepository(t)
    
def test_memrepo_template(memrepo):
    assert "pack1" in memrepo.all()
    assert "pack2" in memrepo.all()


def test_seed(memrepo):
    
    # Should succeed (new type)
    memrepo.pack1.seed('straight2', data=3.14, idem=False)
    v = memrepo.pack1.collection.view('r01', 'straight2')
    assert hasattr(v, 'straight2')
    assert 'data' in v.straight2.data()

    # Should fail ('straight' already exists as a spice type)
    with pytest.raises(ValueError):
        memrepo.pack1.seed('straight', data=3.14, idem=False)

    # Should work (idem parameter)
    exists = memrepo.pack1.seed('straight', data=3.14, idem=True)
    assert exists['uuid'] == memrepo.pack1.collection.view(None, 'straight').straight.meta('uuid')
    assert exists['uuid'] == memrepo.pack1.collection.view('r01', 'straight').straight.meta('uuid')


def test_anchor(memrepo):
    v1 = memrepo.pack1.collection.view(None, 'straight').straight.obj()
    v2 = memrepo.pack1.anchor('r02', 'straight')
    
    print('v1', v1)
    print('v2', v2)
    assert v1['data'] == v2['data']

    v3 = memrepo.pack1.anchor('r02', 'straight')
    assert v2['data'] == v2['data']
    assert v2['uuid'] == v2['uuid']


def test_update(memrepo):
    v1 = memrepo.pack1.update('r02', 'straight', param=1)
    
    print('update:', v1)
    assert v1['data']['param'] == 1
    
    v2 = memrepo.pack1.update('r02', 'straight', param=1)
    print('idem update:', v2)
    assert v2['uuid'] == v1['uuid']

    v3 = memrepo.pack1.update('r02', 'straight', param=2)
    print('overwrite:', v3)
    assert v2['uuid'] != v3['uuid']
    assert v3['data']['param'] == 2
    assert v2['data']['param'] != v3['data']['param']

    v4 = memrepo.pack1.update(v3['uuid'], param=3)
    print('update by uuid:', v4)
    assert v4['uuid'] != v3['uuid']
    assert v4['data']['param'] != v3['data']['param']
    assert v4['data']['param'] == 3
