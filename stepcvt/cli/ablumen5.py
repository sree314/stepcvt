# Task: STL conversion info - rotation, linear tolerance, angular tolerance - attach to part
import argparse
from stepcvt import project


def definePart():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--rotation", type=int, nargs=3, help="3 integers for x, y, z rotation"
    )
    parser.add_argument(
        "--linearTolerance", type=float, nargs=1, help="float for linear tolerance"
    )
    parser.add_argument(
        "--angularTolerance", type=float, nargs=1, help="float for angular tolerance"
    )
    args = parser.parse_args()
    # print(args.rotation)
    # print(args.linearTolerance)
    # print(args.angularTolerance)
    rot = args.rotation
    linarTol = args.linearTolerance
    angularTol = args.angularTolerance
    part = project.STLConversionInfo(
        rotation=rot, linearTolerance=linarTol, angularTolerance=angularTol
    )
    return part


definePart()
