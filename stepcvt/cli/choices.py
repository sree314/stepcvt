import json

from stepcvt import *


def choices_add(args):
    # parse json input
    with open(args.jsonfile, "r") as file:
        project = Project.from_dict(json.load(file))
    if not project:
        raise SyntaxError("Error loading project config from json")

    # parse new choice
    # split values
    values = set()
    try:
        for kv in args.values:
            l = kv.split(":", maxsplit=3)
            values.add(ChoiceValue(l[0], l[1], l[2:3] or None))
    except IndexError:
        raise SyntaxError("Missing required attribute in text:value[:cond] pair")

    # add new chooser to project
    project.available_choices.choices.append(values)


def choices_edit(args):
    pass


def choices_remove(args):
    pass


def choices_apply(args):
    pass
