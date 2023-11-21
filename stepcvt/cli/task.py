import json
from stepcvt import project
from ..project import *


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

    if args.rotation:
        rotation = args.rotation
    else:
        rotation = [0, 0, 0]

    if args.linearTolerance:
        linearTol = args.linearTolerance
    else:
        linearTol = 0.1

    if args.angularTolerance:
        angularTol = args.angularTolerance
    else:
        angularTol = 0.1

    for partid, obj in source.parts():
        if partid == args.partID:
            if len(obj.info) > 0:
                for el in obj.info:
                    if el.gettype() == STLConversionInfo:
                        # edit existing TaskInfo case
                        el = STLConversionInfo(
                            rotation=rotation,
                            linearTolerance=linearTol,
                            angularTolerance=angularTol,
                        )
            else:
                # create new taskInfo object
                obj.info.append(
                    STLConversionInfo(
                        rotation=rotation,
                        linearTolerance=linearTol,
                        angularTolerance=angularTol,
                    )
                )

    with open(args.jsonfile, "w") as jf:
        json.dump(project.to_dict(), jf)
    return 0


stlconvert()
