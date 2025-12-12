from nx5d.repo.base import DataScanBase
import urllib
from nx5d.recipe import *
from nx5d.recipe import my_callable

def test_file_loader():
    c = load_recipe(f'file://{__file__}#my_callable')
    assert c(None, None) == my_callable(None, None)


def test_pymod_loader():
    c = load_recipe(f'pymod:///nx5d.recipe#my_callable')
    assert c(None, None) == my_callable(None, None)
