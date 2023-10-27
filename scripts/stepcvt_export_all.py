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


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Export all components of a STEP file as STL files"
    )
    p.add_argument("stepfile", help="STEP file")
    p.add_argument(
        "output_directory",
        help="Output directory where step files will be placed (e.g. /tmp)",
    )

    args = p.parse_args()

    stepfile = Path(args.stepfile)
    odir = Path(args.output_directory)

    # create a project and load the step file
    p = Project(name=stepfile.name)
    p.add_source(name=stepfile.name, path=stepfile)

    # go through all parts in the step file and create partinfo for
    # them
    source = p.sources[0]
    for partid, obj in source.parts():
        source.add_partinfo(partid, obj)

    # go through each added partinfo and add some STLConversionInfo
    # with some arbitrary rotation for now
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
