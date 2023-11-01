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

# Example: stepcvt_export_all.py file.step out_dir --partid part1 --rot 0,45,0 --partid part2 --rot 90,0,0
# Example: stepcvt_export_all.py file.step out_dir --exclude part1 part2
# --partid needs to be followed by --rot
# --rot 0,0,0 corresponds to no rotation
# --rot aruguments only support positive degrees

import argparse
from pathlib import Path
from stepcvt.project import Project
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
        action="append",
        help="Specify part to be exported"
    )
    p.add_argument(
        "--rot", 
        action="append",
        help="Apply custom rotation to the specified part ('x,y,z' in degrees,"
            " only support integers)"
    )
    p.add_argument(
        "--exclude",
        nargs="+",
        help="Export all objects except those specified here with partid"
    )

    args = p.parse_args()

    stepfile = Path(args.stepfile)
    odir = Path(args.output_directory)
    specified_ids = args.partid
    specified_rot = args.rot
    exclude_ids = args.exclude
    
    # create a project and load the step file
    p = Project(name=stepfile.name)
    p.add_source(name=stepfile.name, path=stepfile)

    # go through all parts in the step file and create partinfo for
    # them
    source = p.sources[0]
        
    if exclude_ids != None:
        exclude_ids = set(exclude_ids)
        for partid, obj in source.parts():
            if partid not in exclude_ids:
                source.add_partinfo(partid, obj)
    # export all parts, i.e. no partid and exclude specified
    elif specified_ids is None: 
        for partid, obj in source.parts():
            source.add_partinfo(partid, obj)
    else:
        dict_id_rot = {}
        for id, rot in zip(specified_ids, specified_rot):
            pattern = r"(?P<x>\d+),(?P<y>\d+),(?P<z>\d+)"
            m = re.match(pattern, rot)
            dict_id_rot.__setitem__(id, [int(m.group('x')),
                                        int(m.group('y')),
                                        int(m.group('z'))])
        
        specified_ids = set(specified_ids)
        for partid, obj in source.parts():
            if partid in specified_ids:
                source.add_partinfo(partid, obj)

    # add custom/random STLConversionInfo to parts
    if specified_ids is not None:
        for pi in source.partinfo:
            pi.add_info(
                stepcvt.project.STLConversionInfo(
                    rotation=dict_id_rot[pi.part_id],
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
