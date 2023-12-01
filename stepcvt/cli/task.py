import json
from stepcvt import project
from ..project import *


def stlconvert(p, args):
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
    return 1
