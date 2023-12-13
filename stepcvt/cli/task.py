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

    for partinfo in source.partinfo:
        if partinfo.part_id == args.partID:
            if len(partinfo.info) > 0:
                for el in partinfo.info:
                    if isinstance(el, STLConversionInfo):
                        # edit existing TaskInfo case
                        el = STLConversionInfo(
                            rotation=rotation,
                            linearTolerance=linearTol,
                            angularTolerance=angularTol,
                        )
            else:
                # create new taskInfo object
                partinfo.add_info(
                    STLConversionInfo(
                        rotation=rotation,
                        linearTolerance=linearTol,
                        angularTolerance=angularTol,
                    )
                )
    return 1
