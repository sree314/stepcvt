import json
from ..project import *
from stepcvt import project


def stlconvert(args):
    # check for jsonfile
    if args.jsonfile is None:
        print("ERROR: Need to provide a jsonfile")
        return 1

    # try to get info from jsonfile
    try:
        with open(args.jsonfile, "r") as jf:
            d = json.load(jf)
            p = Project.from_dict(d)
    except FileNotFoundError as fe:
        print(f"ERROR: {args.jsonfile} doesn't exist")
        return 1
    except json.JSONDecodeError:
        print("ERROR: Invalid json syntax")
        return 1

    if not p.sources:
        print("ERROR: No existing source, add one first")
    else:
        source = p.sources[0]

    if args.partID:
        partID = args.partID
    else:
        print("ERROR: Need to specify at least one partid if --all is not included")
        return 1

    if args.rotation == True:
        rotation = args.rotation
    if args.linearTolerance == True:
        linearTol = args.linearTolerance
    else:
        linearTol = 0.1
    if args.angularTolerance == True:
        angularTol = args.angularTolerance
    else:
        angularTol = 0.1

    partID = project.STLConversionInfo(
        rotation=rotation, linearTolerance=linearTol, angularTolerance=angularTol
    )
    partID.rotate(source)

    with open(args.jsonfile, "w") as jf:
        json.dump(partID.to_dict(), jf)
    return 0


# issues:
# - there is no real way to connect a part to an STLConversionInfo object besides naming the object the partID
# - future work would be to have a --listConversionsApplied arg but since all our conversion info objects are seperate I'm not sure how to get all parts from all conversion info objects -- connects to issue 1
# Note: this uses strategies from part.py
