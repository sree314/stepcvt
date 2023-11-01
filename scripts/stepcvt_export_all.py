#!/usr/bin/env python3
#
# stepcvt_export_all.py
#
# Convenience script for exporting all parts of a model as individual STL files.
#
# In its current version, this serves as an integration test for the
# classes in the stepcvt.package as well as a demonstration of how the
# library should be used.
#
# I'm using this STEP file as an example, since it contains only 3D
# printed parts and not any off-the-shelf component
#  https://github.com/VoronDesign/Voron-Stealthburner/blob/main/CAD/Printheads/Stealthburner_Printhead_V6.stp
#
# Download it someplace and pass it as an argument to this script

import argparse
from pathlib import Path
from stepcvt.project import Project
import sys
import re


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Export all components of a STEP file as STL files"
    )
    p.add_argument("stepfile", help="STEP file")
    p.add_argument(
        "output_directory",
        help="Output directory where step files will be placed (e.g. /tmp)",
    )
    p.add_argument(
        "--partid", 
        help="Specify part to be exported"
    )
    p.add_argument(
        "--rot", 
        help="Apply custom rotation to the specified part ('x,y,z' in degrees,"
            " only support integers)"
    )
    p.add_argument(
        "--exclude",
        nargs="*",
        help="Export all objects except those specified here with partid"
    )

    args = p.parse_args()

    stepfile = Path(args.stepfile)
    odir = Path(args.output_directory)
    exclude_ids = args.exclude  # None if not specified

    # create a project and load the step file
    p = Project(name=stepfile.name)
    p.add_source(name=stepfile.name, path=stepfile)

    # go through all parts in the step file and create partinfo for
    # them
    source = p.sources[0]
        
    if exclude_ids != None:
        for partid, obj in source.parts():
            if partid not in exclude_ids:
                source.add_partinfo(partid, obj)
    else:
        specified_ids = []
        specified_rot = []
        # get arguments for (partid + rot)'s and parse them out
        argstr = ' '.join(sys.argv[3:])
        pattern = r'--partid\s(?P<id>\S*)(\s)?(--rot\s(?P<x>[-+]?\d+),(?P<y>[-+]?\d+),(?P<z>[-+]?\d+)(\s)?)?'
        matches = re.finditer(pattern, argstr)
        for match in matches:
            partid = match.group("id")
            rot = (match.group("x"), match.group("y"), match.group("z"))
            specified_ids.append(partid)
            specified_rot.append(rot)
            
        # print(specified_ids)
        # print(specified_rot)

        # export all parts, i.e. no partid and exclude specified
        if not specified_ids: 
            for partid, obj in source.parts():
                source.add_partinfo(partid, obj)
        else:
            for sid in specified_ids:  # keep the same order with specified_rot
                for partid, obj in source.parts():
                    if sid == partid:
                        source.add_partinfo(partid, obj)
    

    # user has specified some rotations for specific parts
    # there might be the case that specified_ids is not empty and specified_rot is empty
    if specified_rot:
        for pi, rot in zip(source.partinfo, specified_rot):
            pi.add_info(
                stepcvt.project.STLConversionInfo(
                    rotation=[int(rot[0]) if rot[0] is not None else 90, 
                              int(rot[1]) if rot[1] is not None else 0,  
                              int(rot[2]) if rot[2] is not None else 0], 
                    linearTolerance=0.1, 
                    angularTolerance=0.2
                )
            )
    
    # go through each added partinfo and add some STLConversionInfo
    # with some arbitrary rotation for now
    else:
        for pi in source.partinfo:
            pi.add_info(
                stepcvt.project.STLConversionInfo(
                    rotation=[90, 0, 0], linearTolerance=0.1, angularTolerance=0.2
                )
            )

    # finally, export each object to a step file. For now, assume the
    # object's partid is a valid filename too.
    for pi in source.partinfo:
        ofile = odir / f"{pi.part_id}.step"
        print(f"Exporting to {ofile}")
        pi.export_to_stl(odir / f"{pi.part_id}.step")
