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
        p.add_source(args.step_name, stepfile)
        try:
            with open(args.jsonfile, "w") as j:
                info = p.to_dict()
                json.dump(info, j, indent=4)
        except FileNotFoundError as fe:
            print(f"ERROR: {args.jsonfile} doesn't exist")
            return 1
        except json.JSONDecodeError:
            print("ERROR: Invalid json syntax")
            return 1


def remove_step(p, args):
    # TODO Needs to be implemented
    if args.jsonfile is None:
        print("ERROR: Need to provide a jsonfile")
        return 1

    if args.step_name is None:
        print("Missing step file name")
    else:
        print(f"Removing step file: {args.step_name} from {args.jsonfile}")
        for source in p.sources:
            if source.name == args.step_name:
                p.sources.remove(source)
                print(
                    f"Removed step file: {args.step_name} from {args.jsonfile} successfully!"
                )

        try:
            with open(args.jsonfile, "w") as j:
                info = p.to_dict()
                json.dump(info, j, indent=4)
        except FileNotFoundError as fe:
            print(f"ERROR: {args.jsonfile} doesn't exist")
            return 1
        except json.JSONDecodeError:
            print("ERROR: Invalid json syntax")
            return 1


def list_parts(p, args):
    if args.step_name is None:
        print("Missing name of the step file")
    else:
        print(f"Listing parts of step file: {args.step_name}")
        for source in p.sources:
            if source.name == args.step_name:
                for partid, _ in source.parts():
                    print(partid)
