import json
import sys

from stepcvt import *


def _parse_values(value_strs: [str]) -> [ChoiceValue]:
    """Split each value string in the list into a ChoiceValue,
    value string has format of: text:value[:cond]"""
    values = []
    try:
        for kv in value_strs:
            l = kv.split(":", maxsplit=3)
            values.append(ChoiceValue(l[0], l[1], l[2:3] or None))
    except IndexError:
        raise SyntaxError("Missing required attribute in text:value[:cond] pair")


def choices_add(args):
    # parse json input
    # TODO: Project.from_dict should throw on any invalid json, this can simplify calling of from_dict function
    with open(args.jsonfile, "r") as file:
        project = Project.from_dict(json.load(file))
    if not project:
        raise SyntaxError("Error loading project config from json")

    # parse new choice
    # split values
    values = _parse_values(args.values)

    # add new chooser to project
    if args.choice_type == "single":
        project.available_choices.choices.append(SingleChooser(args.text, args.varname, values))
    elif args.choice_type == "multi":
        project.available_choices.choices.append(MultiChooser(args.text, args.varname, values))
    elif args.choice_type == "boolean":
        project.available_choices.choices.append(BooleanChooser(args.text, args.varname, values[0], values[1]))
        if len(values) > 2:
            print("Extra ChoiceValue provided other than [select_value, unselect_value] is discarded for boolean chooser",
                  file=sys.stderr)
    # theoretically no other values should appear

    # TODO: json dump modified project


def choices_edit(args):
    # parse json input
    with open(args.jsonfile, "r") as file:
        project = Project.from_dict(json.load(file))
    if not project:
        raise SyntaxError("Error loading project config from json")
    choices = project.available_choices

    # find chooser to edit
    chooser = next(filter(lambda c: c.varname == args.varname, choices), None)
    if chooser is None:
        raise SyntaxError(f"Chooser {args.varname} not found in provided project file")

    # edit
    values = _parse_values(args.new_values)
    if args.choice_value:
        # find ChoiceValue to edit
        if isinstance(chooser, BooleanChooser):
            if args.choice_value == "select":
                cv = chooser.sel_value
            elif args.choice_value == "unselect":
                cv = chooser.unsel_value
            else:
                raise SyntaxError(f"'choice_value' needs to match either 'select' or 'unselect' in boolean chooser")
        else:
            cv = next(filter(lambda v: v.text == args.choice_value, chooser.values), None)
        # replace specific ChoiceValue
        if len(values) > 1:
            print("Extra new_values provided is discarded, only accepts one when a choice_value is specified",
                  file=sys.stderr)
        value = values[0]
        if cv is None:
            if isinstance(chooser, BooleanChooser) and args.choice_value == "unselect":
                # boolean chooser with no unsel_value set
                # add an unsel_value
                chooser.unsel_value = value
                return
            else:
                raise SyntaxError(f"Choice value {args.choice_value} not found in chooser {args.varname}")
        cv.text = value.text
        cv.vlaue = value.value
        cv.cond = value.cond
    else:
        # replace entire ChoiceValue list
        chooser.values = _parse_values(values)


def choices_remove(args):
    with open(args.jsonfile, "r") as file:
        project = Project.from_dict(json.load(file))
    if not project:
        raise SyntaxError("Error loading project config from json")

    # select chooser
    chooser = next(filter(lambda c: c.varname == args.varname, project.available_choices.choices), None)
    if chooser is None:
        raise SyntaxError(f"Chooser {args.varname} not found in provided project file")
    if not args.choice_value:
        project.available_choices.choices.remove(chooser)
        return

    # select choice value
    cv = next(filter(lambda v: v.value == args.choice_value, chooser.values), None)
    if cv is None:
        raise SyntaxError(f"Choice value {args.choice_value} not found in chooser {args.varname}")
    if not args.cond:
        chooser.values.remove(cv)
        return

    # select cond
    cv.cond = None


def choices_apply(args):
    pass
