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


def make(args):
    p = Project()
    print("New project created ...", end=" ")
    if args.name:
        p.name = args.name
        print("Project renamed to ", p.name, " ...", end=" ")
    print("done")
    return p


def display(p, args):
    # Add better formatting
    data = p.to_dict()
    print(json.dumps(data, indent=4))


def newName(p, args):
    print("Project being renamed to ", p.name, " ...", end=" ")
    p.name = args.name
    print("done")
    return 1
