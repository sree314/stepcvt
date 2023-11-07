"""
Project CLI Overview:
	1. Create project and make a new json file to be filled in
	   - If no .json file specified, use default file "stepcvt.json"
	   - If no name specified, use default name "proj"

		<stepcvt> [-j] [json file path/name.json] <make> [specific project "name"]
		<stepcvt> [-j] [json file path/name.json] <make>
		<stepcvt> <make> [specific project "name"]
		<stepcvt> <make>

	2. Display existing project from an existing json file
	   - If no .json file specified,
	      - If the current directory has only one .json file,
		 - Then use the only exisitng .json file.
	      - If there is more than one possible json file,
		 - Try to use default file "stepcvt.json" if it exists.
		 - If that fails, throw an error

		<stepcvt> <display> [-j] [json file path/name.json]
		<stepcvt> <display>

	3. Edit name, etc. in a given json file (or default json file)
	   - If no .json file specified,
	      - If the current directory has only one .json file,
		 - Then use the only exisitng .json file.
	      - If there is more than one possible json file,
		 - Try to use default file "stepcvt.json" if it exists.
		 - If that fails, throw an error
	   - If no "name" given, throw an error

		<stepcvt> [-j] [json file path/name.json] <name> [new "name"]
		<stepcvt> <name> [new "name"]



File Tree for CLI:
	stepcvt/
		cli/
			project.py
			cadsource.py
			etc...
		scripts/
			stepcvt.bash
				from stepcvt.cli import *
"""

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "-j", help="Path to an empty .json file or one with a saved project"
)
parser.add_argument("make", help="Make a new project")
parser.add_argument("display", help="Display a project's data")
parser.add_argument("name", help="Change the name of a project")
args = parser.parse_args()

if args.j:
    json = args.j
if args.make:
    make = args.make
if args.display:
    disp = args.display
if args.name:
    name = args.name
