#!/usr/bin/python3

'''
Geometry and data set definitions for the ESRF ID09 XRD beamline.
Need these for the `nx5d.xrd.data.ScanReader` object.
'''

'''
See `nx5d.xrd.data.ScanReader.__init_experiment()` for a more detailed
documentation of the device setup data.
'''

ExperimentTemplate = {
    "goniometerAxes": ('y+',),
    "detectorTARAxes": (None, None, None),
    "imageAxes": ("z-", "y-"),
    "imageSize": (4096, 4096),
    "imageCenter": (0.5, 0.5),

    # pixel size is typically present in the HDF5 data file, distance is 0.2 m.
    "imageChannelSize": None,

    "sampleFaceUp": 'z+',
    "sampleNormal": (0, 0, 1),
    "beamDirection": (-1, 0, 0),

    "goniometerAngles": [ "hphi" ],
    "detectorTARAngles": []
}

#DataLabels = {
        #"img":  lambda src: "measurement/rayonix",
        #"hphi": lambda src: "instrument/positioners/hphi",
        #"lxt":  lambda src: "instrument/positioners/lxt_ps",
        #"norm": lambda src: "measurement/sbcurr"
#}
