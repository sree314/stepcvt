from ..project import *

"""
Project CLI Overview:
	1. Create project and make a new json file to be filled in
	   - If no .json file specified, use default file "stepcvt.json"
	   - If no name specified, use default name "proj"

		<stepcvt> [-j] [json file path/name.json] <make> [-n] [specific project "name"]
		<stepcvt> [-j] [json file path/name.json] <make>
		<stepcvt> <make> [-n] [specific project "name"]
		<stepcvt> <make>

	2. Display existing project from an existing json file
	   - If no .json file specified,
	      - If the current directory has only one .json file,
		 - Then use the only exisitng .json file.
	      - If there is more than one possible json file,
		 - Try to use default file "stepcvt.json" if it exists.
		 - If that fails, throw an error

		<stepcvt> [-j] [json file path/name.json] <display>
		<stepcvt> <display>

	3. Edit name, etc. in a given json file (or default json file)
	   - If no .json file specified,
	      - If the current directory has only one .json file,
		 - Then use the only exisitng .json file.
	      - If there is more than one possible json file,
		 - Try to use default file "stepcvt.json" if it exists.
		 - If that fails, throw an error
	   - If no "name" given, throw an error

		<stepcvt> [-j] [json file path/name.json] <newName> [new "name"]
		<stepcvt> <newName> [new "name"]
"""

import json
from ..project import *


def getJSON(args, req):  # Adapted from part.py CLI code
    if args.jsonfile is None:
        if req:
            print("ERROR: Need to provide a jsonfile")
            return None, None
        else:
            jfName = "stepcvt.json"
    else:
        jfName = args.jsonfile

    try:
        with open(jfName, "x") as jf:
            d = json.load(jf)
    except FileNotFoundError as fe:
        print(f"ERROR: {args.jsonfile} doesn't exist")
        return None, None
    except json.JSONDecodeError:
        print("ERROR: Invalid json syntax")
        return None, None
    return d, jf


def make(args):
    data, jf = getJSON(args, False)

    # add handling of empty json to make new project

    p = Project.from_dict(data)
    if args.name is None:
        p.name = "stepcvt"
    else:
        p.name = args.name
    jf.close()


def display(args):
    data, jf = getJSON(args, False)
    print(data)
    jf.close()


def newName(args):
    data, jf = getJSON(args, False)
    p = Project.from_dict(data)
    p.name = args.name
    jf.close()
