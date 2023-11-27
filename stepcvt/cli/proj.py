# Samantha Kriegsman
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
    # req = True means the file oppened must be a valid json
    # req = False means the file can be init if empty
    if args.jsonfile is None:
        jfName = "stepcvt.json"
    else:
        jfName = args.jsonfile

    try:
        jf = open(jfName, "r+")
        rd = jf.read()
        pd = json.loads(rd)
        return pd, jf
    except FileNotFoundError as fe:
        print(f"ERROR: {args.jsonfile} doesn't exist")
        return None, None
    except json.JSONDecodeError:
        if req:
            print("ERROR: Invalid json syntax")
            return None, None
        else:
            p = Project()
            json.dump(p.to_dict(), jf)
            return p.to_dict(), jf


def make(args):
    data, jf = getJSON(args, False)
    p = Project.from_dict(data)
    if args.name:
        p.name = args.name
    jf.close()


def display(args):
    data, jf = getJSON(args, True)
    if data is None:
        return False
    print(data)
    jf.close()


def newName(args):
    data, jf = getJSON(args, True)
    if data is None:
        return False
    p = Project.from_dict(data)
    p.name = args.name
    jf.close()
