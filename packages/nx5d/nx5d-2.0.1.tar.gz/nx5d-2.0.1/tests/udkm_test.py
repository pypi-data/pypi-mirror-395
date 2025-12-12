# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 13:38:50 2025

@author: aleks
"""
import nx5d.xrd.udkm as nxu
import pytest, os


@pytest.fixture
def data_base():
    return os.path.abspath(
        os.path.join(".", "tests", "test_data", "udkm",
                     "{proposal}", "{scan}")
    )


def test_load(data_base):
    fac = nxu.DatasetFactory()

    ds = fac(
            data_base.format(
                proposal=os.path.join("2025", "20250408"),
                scan="162828"
            )
    )
    assert 'images' in ds.data_vars
    for k in ds.data_vars:
        assert (ds[k].shape[0] == ds['images'].shape[0])


    ds = fac(
            data_base.format(
                proposal=os.path.join("2025", "20250424"),
                scan="150008"
            )
    )
    assert 'images' in ds.data_vars
    for k in ds.data_vars:
        assert (ds[k].shape[0] == ds['images'].shape[0])
        

def test_repo(data_base):
    print('Test repo:', data_base)
    repo = nxu.LegacyRepository(data_base)

    for pack in ('p20250424', 'p20250408'):
        assert pack in repo.__dir__()
        pobj = getattr(repo, pack)
        assert isinstance(pobj, nxu.DataPack)


def test_scan(data_base):
    print('Test repo:', data_base)
    repo = nxu.LegacyRepository(data_base)
    print('UDKM test repo:', repo.all())

    prop = repo.p20250424
    print('UDKM test proposal:', prop.all())

    html = prop._repr_html_()
    text = prop.__repr__()
    spice = prop.spice
    print('spice:', spice)

    scan = prop.r150008
    r = scan.raw
    assert "images" in r
    print(r)

    # 'prop' is now an in-memory proposal.
    #
    # It may or may not come with a recipe for the current scan type.
    # If it doesn't have, we seed one; if it does have recipes, we
    # make sure that at least the default fallback is something
    # we can use.
    if hasattr(scan.spice, "recipes"):
        prop.spice.update(None, 'recipes', __default__='pymod:///nx5d.recipe#my_callable')
    else:
        prop.spice.seed('recipes', **{ scan.type: 'pymod:///nx5d.recipe#my_callable'})
    
    c = scan.cooked
    print(c)
