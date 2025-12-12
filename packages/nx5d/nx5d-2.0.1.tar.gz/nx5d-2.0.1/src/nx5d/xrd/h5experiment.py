#!/usr/bin/python3

## Module to load / save experiment definitions from/to HDF5 Nexus files.

import yaml

def exp_from_yaml(fname):
    '''
    Returns an experiment definition dictionary (as required by QMapper)
    from a YAML file.
    '''

    with open(fname, 'r') as stream:
        try:
            return yaml.safe_load(stream)['experimentSetup']
        except yaml.YAMLError as e:
            logging.error(e)
            raise

def exp2xeuler(exp):
    '''
    "Translates" an experiment setup (or template) into the coordinate
    system naming of the NXeuler Nexus application type. This essentially
    means replacing coordinate letters (x, y, z) with different type
    of coordinate letters.

    The NXxeuler experiment essentially has the following lab system
    definition (see also: https://manual.nexusformat.org/classes/applications/NXxeuler.html#nxxeuler):

     - the Holy Direction of the X-ray Beam is... z. Not x.
    
     - x and y are directions of the detector area / 2D chip.

     - all angles grow counter-clockwise with respect to their
       axis (i.e. they are all "+" direction in xrayutilities lingo).

     - there's no way to specify a direction of the detector pixels,
       i.e. the detector axes are "x" and "y", but pixel 0 apparently
       belongs to the lower value, and pixel N to the higher value
       in that specific direction / on that specific axis.

    Returns an xeuler-compatible experiment template dictionary,
    and a tuple of signs for each of the angles.
    '''
    pass
    # Intermediate name for the axes:
    #  - K: 1st image direction (dimension)
    #  - L: 2nd image direction
    #  - M: X-ray beam direction
