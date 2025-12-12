#!/usr/bin/python3

import yaml

# Device / experiment geometry.
# The idea is to have this as a standard data format for any input
# data to the transformation algorithm.
#
# Ideally we'd separate this into strictly geometric data (i.e.
# "how the detector is built") and measurement data ("where are
# my angles at this particular moment"), but these data seem
# to be pretty mixed up in xrayutilities.
#
# As a consequence, we keep them together here, too.
# Perhaps a (future) system where several of these dictionaries
# can be cascaded can be put in place?
KMC3 = {

    # Energy of the X-ray beam in eV
    # XPP: ?
    # ESRF: ?
    "xray-energy": 9400.0,    

    
    "sample": {

        # Sample surface orientation in the same coordinate system as
        # the goniometer rotations are given (?)
        #  - det:
        #  - sam: ...
        #  - xyz+-...
        "orientation": 'x+', #"sam",

        # X-ray direction at zero angles (as seen from the sample coordinate system)
        "inplane-direction": (0, 1, 0),
        
        # Sample surface normal (_always_ perpendicular to inplane-dir -- why necessary?)
        # XPP: n/a
        "normal-direction": (0, 0, 1),

        # Definition of rotation angles (and direction) of
        # the sample with resepct to the lab coordinate system,
        # from outer to inner most circles.
        # XPP: n/a, 
        "axes": ('y+', 'z+', 'x+'),

        # Angles of sample positioning
        # XPP: (Sxx/positioners/Theta, Sxx/positioners/Chi, Sxx/positioners/Phi)
        # ESRF: (instrument/positioners/gonx|y|z?
        "angles": (0, 0, 0),
    },

    "detector" : {

        "sensor": {

            # Directions of the detector along width/height of the pixel plate
            # XPP: n/a
            "directions": ('x+', 'z+'),
        
            # Center channels (pixels) of the detector, i.e.
            # the point through which the X-ray goes at zero
            # angles, should probably be the same as the axis
            # of rotation (?). If there is no rotation axis,
            # then this is just the point on which the incoming
            # X-ray beam hits (right?)
            # XPP: n/a
            "center": (283, 178),

            # Number of channels (pixels) in each dimenion
            # XPP: n/a
            # ESRF: ?
            "size": (195, 487),

            # The pixel geometry is either specified as distance/pixel-size,
            # or as pixel-per-degree
        
            # Size of a detector channel (pixel) in the same
            # units as the distance (see below), and
            # distance of detector center from the sample in the
            # same units as the pixel size (see above)
            # XPP: n/a
            # ESRF: ?
            "channel-size": (1.5e-4, 1.5e-4),
            "distance": 1.0,

            # Numer of pixels (channels) per degree, in either direction
            # XPP: n/a
            # ESRF: n/a
            "chperdeg": None, # (43, 57)
        },

        # Definition of rotation angles (and direction)
        # of the detector, relative to the lab system, in
        # the order (Tilt, Azimuth, Rotation), where:
        #  - Tilt: The in-sample-plane rotation of the detector;
        #    None of the axis is an experimental constant/never
        #    used, and to be set to 0.
        #  - Azimuth: Rotation in the detector plane (2-Theta?)
        #  - Rotation of the sensor itself around its own normal
        #    axis (around the incident beam axis at zero angle).
        #    None if never used, set to 0.
        # XPP: n/a
        # ESRF: ?
        "axes": (None, 'z+', None),

        # Detector angles, tuple as specified by "rotations" above.
        # XPP: (None, 'Sxx/positioners/TwoTheta', None)
        # ESRF: (instrument/positioners/detx|y|z?
        "angles": (0, 0, 0),
    },

    "data": {

        # Which value to normalize data by
        # XPP: ?
        # ESRF: instrument/machine/current
        "normalization": 1.0,
    }
}

def fromYaml(path):
    '''
    Reads an experiment specification file (YAML) and returns
    an experiment dictionary, with values as above.
    '''

    x = yaml.load(path)
