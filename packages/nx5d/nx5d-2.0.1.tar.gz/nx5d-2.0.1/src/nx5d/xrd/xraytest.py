#!/usr/bin/python3

import fabio
import xrayutilities as xray
import numpy as np
import argparse
import experiment


def makeXray(experiment):
    '''
    Creates / returns an xrayutilities.Experiment() class according to
    dictionary experiment specification.
    '''
    # The experiment["detector"] object always has a tupe of 3 axes
    # to specify; this is because some xrayutilities modules, e.g.
    # the HXRD object, use specific definitions.
    # Those that are not defined in a particular setup are set
    # as 'None' at the axis level.
    # We need to filter those out before passing them on to QConversion.
    
    #detector_geometry = {
    #    "axes": [],
    #    "angles": []
    #}
    #
    #for ax,rot in ):
    #    if ax is not None:
    #        detector_geometry["axes"].append(ax)
    #        detector_geometry["angles"].append(rot)

    detector = [ x for x in filter(lambda x: x[0] is not None,
                                                zip(experiment["detector"]["axes"],
                                                    experiment["detector"]["angles"])) ]
    det_axes, det_angles = zip(*detector)
    
    print ("Detector axes:", det_axes)
    print ("Detector angles:", det_angles)

    qconv = xray.QConversion(sampleAxis=experiment["sample"]["axes"],
                             detectorAxis=det_axes,
                             r_i=experiment["sample"]["inplane-direction"],
                             en=experiment["xray-energy"])
    
    e = xray.io.EDFFile(filename)
    run15x = e.ReadData()

    exp = xray.HXRD(idir=experiment["sample"]["inplane-direction"],
                    ndir=experiment["sample"]["normal-direction"],
                    sampleor=experiment["sample"]["orientation"],
                    qconv=qconv)

    exp.Ang2Q.init_area(detectorDir1=experiment["detector"]["sensor"]["directions"][0],
                        detectorDir2=experiment["detector"]["sensor"]["directions"][1],
                        cch1=experiment["detector"]["sensor"]["center"][0],
                        cch2=experiment["detector"]["sensor"]["center"][1],
                        Nch1=experiment["detector"]["sensor"]["size"][0],
                        Nch2=experiment["detector"]["sensor"]["size"][1],
                        # either distance/chwidth...
                        distance=experiment["detector"]["sensor"]["distance"],
                        pwidth1 =experiment["detector"]["sensor"]["channel-size"][0],
                        pwidth2 =experiment["detector"]["sensor"]["channel-size"][1],
                        # or channels-per-degree
                        # ...,
                        detrot     =experiment["detector"]["angles"][2],
                        tiltazimuth=experiment["detector"]["angles"][1],
                        tilt       =experiment["detector"]["angles"][0]
                        )

    return exp
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="Process a single image file")
    parser.add_argument("-x", "--experiment", help="Use experiment definiton from YAML file")
    #parser.add_argument("nexus", help="Opens / processes data from a HDF5/Nexus file")
    args = parser.parse_args()    

    if args.image:
        print ("Loading data:", args.image)
        f = fabio.open(args.image)
        run15f = f.data        
    else:
        print("No data specified.")

    xray = None
    if args.experiment:
        print ("Loading experiment setup:", args.experiment)
        exp = makeXray(fromYaml(args.experiment))
        xray = makeXray(exp)
    else:
        print("No experiment file, using default KMC3 builtin")
        xray = makeXray(experiment.KMC3)

    
    qset = exp.Ang2Q.area(*(experiment["sample"]["angles"]),
                         *(detector_geometry["angles"]))
   
    print ("Q:", qset)

    for qi in qset:
        print ("Shape:", qi.shape)
