import json
from pathlib import Path
from ..project import *


def add_step(p, args):
    if args.jsonfile is None:
        print("ERROR: Need to provide a jsonfile")
        return 1

    if args.step_path is None:
        print("Missing path to step file")
    else:
        print(f"Adding step file: {args.step_path} to {args.jsonfile}.")
        stepfile = Path(args.step_path)
        cs = CADSource(name="test", path=stepfile)
        p.add_source(cs, args.step_name, args.step_path)
        cs.load_step_file()
        try:
            with open(args.jsonfile, "w") as j:
                info = cs.to_dict()
                json.dump(info, j)
        except FileNotFoundError as fe:
            print(f"ERROR: {args.jsonfile} doesn't exist")
            return 1
        except json.JSONDecodeError:
            print("ERROR: Invalid json syntax")
            return 1


def remove_step(p, args):
    # TODO Needs to be implemented
    print(f"Removing step file: {args.step_path} from {args.project}")


def list_parts(p, args):
    if args.step_path is None:
        print("Missing path to step file")
    else:
        print(f"Listing parts of step file: {args.step_name}")
        stepfile = Path(args.step_path)
        cs = CADSource(name="temp", path=stepfile)
        for partid, _ in cs.parts():
            print(partid)
