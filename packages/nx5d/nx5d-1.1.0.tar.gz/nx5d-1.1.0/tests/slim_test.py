import pytest, json, glob, os, pprint, uuid
from nx5d.slim import Application
from nx5d.slim import _json_from_args

def test_jargs():
    
    j = _json_from_args('foo=42',
                      'bar="bar"',
                      'obj={"key": "value", "array": [1, 2, 3]}')
    assert j['foo'] == 42
    assert j['bar'] == "bar"
    assert j['obj']['key'] == "value"
    assert j['obj']['array'] == [1, 2, 3]

    j = _json_from_args('./tests/test_data/json/offsets.json')
    for i in ('chi', 'phi', 'theta', 'tth'):
        assert i in j
    assert j['chi'] == 0

    j = _json_from_args('./tests/test_data/json/offsets.json', 'chi=1.0')
    for i in ('chi', 'phi', 'theta', 'tth'):
        assert i in j
    assert j['chi'] == 1.0

    j = _json_from_args('chi=2.0', './tests/test_data/json/offsets.json')
    for i in ('chi', 'phi', 'theta', 'tth'):
        assert i in j
    assert j['chi'] == 2.0

    j = _json_from_args('chi=2.0',
                        './tests/test_data/json/offsets.json',
                        './tests/test_data/json/energy.json')
    for i in ('chi', 'phi', 'theta', 'tth', 'energy'):
        assert i in j
    assert j['chi'] == 2.0

    with pytest.raises(RuntimeError):
        j = _json_from_args('nonexistent')

    pprint.pprint(j)


@pytest.fixture
def env():
    import os
    return {
        "NX5D_SPICE_REPO": os.path.abspath("./tests/test_data/spice/{proposal}")
    }

def test_proposals(env):
    # Lists proposals, no output    
    o = Application(args=["slim", "proposals?"], env=env)._run()
    print('result:', o)
    assert o == None


def test_list(env):
    o = Application(env=env, args=[
        "slim", "pack1", "list"
    ])._run()
    print('result:', o)
    assert len(o) == 2 # 2 anchor points for 'pack1'


def test_view(env):
    o = Application(env=env, args=[
        "slim", "pack1", "view", "r01"
    ])._run()
    print('result:', o)
    assert len(o) == 3 # 3 spice types for 'pack1'


def test_update(env):
    o = Application(env=env, args=[
        "slim", "pack1", "update", "straight@r01", "--dry"
    ])._run()
    print('result:', o)
    u = uuid.UUID(o)
    

def test_seed(env):

    # Should succeed
    o = Application(env=env, args=[
            "slim", "pack1", "seed", "straight2", "data=3.14", "--dry"
        ])._run()
    print('result:', o)
    u = uuid.UUID(o)

    # Should fail ('straight' already exists)
    o = Application(env=env,
        args=[
            "slim", "pack1", "seed", "straight", "data=3.14", "--dry",
        ])._run()
    print('result:', o)
    with pytest.raises((ValueError, AttributeError)):
        uuid.UUID(o)
    

def test_anchor(env):
    o = Application(env=env,
        args=[
            "slim", "pack1", "anchor", "r02", "straight", "--dry"
        ])._run()
    print('result:', o)
    u = uuid.UUID(o)
    
