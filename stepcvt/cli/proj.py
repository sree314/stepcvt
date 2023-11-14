from ..project import *

"""
Project CLI Overview:
	1. Create project and make a new json file to be filled in
	   - If no .json file specified, use default file "stepcvt.json"
	   - If no name specified, use default name "proj"

		<stepcvt> [-j] [json file path/name.json] <make> [specific project "name"]
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

		<stepcvt> [-j] [json file path/name.json] <name> [-n] [new "name"]
		<stepcvt> <name> [-n] [new "name"]
"""

import argparse
import json
from stepcvt.project import Project

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create and manage Project Objects")
    parser.add_argument(
        "-j", "--json", help="Path to an empty .json file or one with a saved project"
    )
    parser.add_argument("command", help="Subcommand to run (make, display, name)")
    parser.add_argument("-n", "--newName", help="Optional subcommand input")
    args = parser.parse_args()

    if args.json:
        jsonFile = open(args.j, "x")
    else:
        jsonFile = open("stepcvt.json", "x")

    if args.newName:
        n = args.newName
    else:
        n = "stepcvt"

    if args.command == "make":
        jsonData = json.load(jsonFile)
        Project.from_dict(n, jsonData)

    elif args.command == "display":
        print(json.load(jsonFile))

    elif args.command == "name":
        Project.name = n

    else:
        print("ERROR")

    jsonFile.close()
