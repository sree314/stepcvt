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


def getJSON(args):
    # return a json file if one was specified, otherwise open/make
    #    a standard json named stepcvt.json
    if args.jsonfile:
        return open(args.j, "x")
    else:
        return open("stepcvt.json", "x")


def make(args):
    jf = getJSON(args)
    # add handling of empty json to make new project
    p = Project.from_dict(jf)
    if args.name is None:
        p.name = "stepcvt"
    else:
        p.name = args.name
    jf.close()


def display(args):
    jf = getJSON(args)
    print(jf)
    jf.close()


def newName(args):
    jf = getJSON(args)
    p = Project.from_dict(jf)
    p.name = args.name
    jf.close()
