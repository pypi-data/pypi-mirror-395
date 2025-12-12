#!/usr/bin/python

import numpy as np

'''
Valid for the P08 Kohzu goniometer, e.g. proposal 20221024 (Taseer/Mai 2023)
'''
P08KohzuExperiment = {
    "goniometerAxes": ('x+', 'y+', 'z-'),
    
    "detectorTARAxes": ('z+', 'x+', None),
    
    "imageAxes": ('z-', 'x+'),
    "imageSize": (516, 1554),
    "imageCenter": (200, 800),

    "imageDistance": 995,
    "imageChannelSize": (0.055, 0.055), # same unit as imageDistance (mm)
    
    "sampleFaceUp": 'z+',
    "beamDirection": (0, 1, 0),
    
    "sampleNormal": (0, 0, 1),
    
    "beamEnergy": 8994,

    "goniometerAngles": {
        'theta': '@fio/data/om',
        'chi':   0,
        'phi':   0
    },

    "detectorTARAngles": {
        'inclination': 0,
        'azimuth':     '@fio/data/tt_position',
    }
}
