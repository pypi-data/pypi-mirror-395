import logging, importlib, urllib

logger = logging.getLogger(__name__)

all = [
    "load_recipe",
    "pymod_recipe_loader",
    "file_recipe_loader"
]

def load_recipe(url):
    '''
    Loads a recipe from a URL-style location.

    The URL-like string supports the following schemes:
        - `pymod`: URL like "pymod://<netloc>/<module>#<callable>",
          where <netloc> is currently ignored, <module> needs to be
          a locally installed Python module in its dot-notation,
          and <callable> a callable inside that module.
        - `file`: URL like "file:///<path-to-file.py>#<callable>",
          loading <callable> from the local file <path-to-file.py>    
    '''
    
    purl = urllib.parse.urlparse(url)
        
    rloader = {
        'pymod': pymod_recipe_loader,
        'file': file_recipe_loader,
    }[purl.scheme]

    return rloader(purl)


def my_callable(stype, idata, **spice):
    # Just a test callable -- for unit testing, and for documentation
    return 'Jinkies!'

def pymod_recipe_loader(url):
    '''
    Loads a callable from a local python module.

    Expects the module name in the `.path` part of the (parsed) URL,
    and the callable inside the module. The initial "/" in the
    module path will be ignored. This is because of how URL definition
    (and parsing) works. Sub-modules can be separated either Python-style
    by ".", or URL-style by "/" (e.g. "module.submodule", "/module.submodule",
    "/module/submodule" will all point to the same module).
    The `.fragment` part (i.e. the part that follows after `#` in a URL) is
    the callable. Currently no other parameters are supported.

    This function doesn't check that the callable has a particular
    signature, but Nx5d's `DataScanBase` expects it to be of
    the form `proc(type, input, **spice)`.

    Returns a referene to the recipe callable.
    '''
    # Don't know how to handle net locations
    if url.netloc not in ('', None):
        raise RuntimeError(f'netloc must be empty (found: {url.netloc})')

    if url.path[0] == '/':
        modname = url.path[1:].replace('/', '.')
    else:
        modname = url.path.replace('/', '.')

    procparts = url.fragment.split('?')
    procname = procparts[0]
    if len(procparts) > 1:
        logger.warning('msg="URL parameters are ignored"')

    mobj = importlib.import_module(modname)
    return getattr(mobj, procname)
    

def file_recipe_loader(url):
    '''
    Loads a recipe from a file on the local filesystem.

    This works pretty much as expected: `.path` needs to point to the
    (absolute or relative) Python file name, and `.fragment` needs to
    be the callable inside the module

    Returns the recipe callable.
    '''
    
    import importlib.util
    import sys
    tmp = '_'.join(url.path.replace('.', '_').split('/'))
    modname = f'{__name__}.{tmp}'

    spec = importlib.util.spec_from_file_location(modname, url.path)
    mobj = importlib.util.module_from_spec(spec)

    procparts = url.fragment.split('?')
    procname = procparts[0]
    if len(procparts) > 1:
        logger.warning('msg="URL parameters are ignored"')

    sys.modules[modname] = mobj
    spec.loader.exec_module(mobj)

    return getattr(mobj, procname)
