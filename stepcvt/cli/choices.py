import sys

from stepcvt.choices import *
from stepcvt.project import *


def _parse_values(value_strs: [str]) -> [ChoiceValue]:
    """Split each value string in the list into a ChoiceValue,
    value string has format of: text:value[:cond]"""
    values = []
    try:
        for kv in value_strs:
            l = kv.split(":", maxsplit=3)
            values.append(ChoiceValue(l[0], l[1], (l[2:3] or [None])[0]))
    except IndexError:
        raise SyntaxError("Missing required attribute in text:value[:cond] pair")
    return values


def choices_add(project: Project, args):
    # parse new choice
    # split values
    values = _parse_values(args.values)

    # add new chooser to project
    if args.type == "single":
        project.available_choices.choices.append(
            SingleChooser(args.text, args.varname, values)
        )
    elif args.type == "multi":
        project.available_choices.choices.append(
            MultiChooser(args.text, args.varname, values)
        )
    elif args.type == "boolean":
        project.available_choices.choices.append(
            BooleanChooser(args.text, args.varname, values[0], values[1])
        )
        if len(values) > 2:
            print(
                "Extra ChoiceValue provided other than [select_value, unselect_value] is discarded for boolean chooser",
                file=sys.stderr,
            )
    # theoretically no other values should appear

    return 1


def choices_effect(project: Project, args):
    # find specified partid
    part = None
    for source in project.sources:
        for p in source.partinfo:
            if p.part_id == args.partid:
                part = p
                break
    if not part:
        raise AttributeError(
            f"Cannot find partid {args.partid} in provided project config"
        )

    # create choice effect
    if args.type == "select":
        effect = SelectionEffect(args.cond)
    elif args.type == "relative-count":
        effect = RelativeCountEffect(args.cond, int(args.value))
    elif args.type == "absolute-count":
        effect = AbsoluteCountEffect(args.cond, int(args.value))
    else:
        raise AttributeError(f"Unknown choice effect type {args.type}")

    part.choice_effects.append(effect)
    return 1


def choices_edit(project: Project, args):
    # find chooser to edit
    chooser = next(
        filter(lambda c: c.varname == args.varname, project.available_choices.choices),
        None,
    )
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
                raise SyntaxError(
                    f"'choice_value' needs to match either 'select' or 'unselect' in boolean chooser"
                )
        else:
            cv = next(
                filter(lambda v: v.value == args.choice_value, chooser.values), None
            )
        # replace specific ChoiceValue
        if len(values) > 1:
            print(
                "Extra new_values provided is discarded, only accepts one when a choice_value is specified",
                file=sys.stderr,
            )
        value = values[0]
        if cv is None:
            if isinstance(chooser, BooleanChooser) and args.choice_value == "unselect":
                # boolean chooser with no unsel_value set
                # add an unsel_value
                chooser.unsel_value = value
                return
            else:
                raise SyntaxError(
                    f"Choice value {args.choice_value} not found in chooser {args.varname}"
                )
        cv.text = value.text
        cv.value = value.value
        cv.cond = value.cond
    else:
        # replace entire ChoiceValue list
        chooser.values = _parse_values(values)

    return 1


def choices_remove(project: Project, args):
    # select chooser
    chooser = next(
        filter(lambda c: c.varname == args.varname, project.available_choices.choices),
        None,
    )
    if chooser is None:
        raise SyntaxError(f"Chooser {args.varname} not found in provided project file")
    if not args.choice_value:
        project.available_choices.choices.remove(chooser)
        return

    # select choice value
    cv = next(filter(lambda v: v.value == args.choice_value, chooser.values), None)
    if cv is None:
        raise SyntaxError(
            f"Choice value {args.choice_value} not found in chooser {args.varname}"
        )
    if not args.cond:
        chooser.values.remove(cv)
        return

    # select cond
    cv.cond = None

    return 1


def choices_apply(project: Project, args):
    user_choices = {}

    for kv in args.choices_input:
        k, v = kv.split("=", maxsplit=2)
        user_choices[k] = v.split(",")
        if len(user_choices[k]) == 1:
            user_choices[k] = user_choices[k][0]
        # unwrap if already surrounded by quotes
        if user_choices[k][0] in {'"', "'"} and user_choices[k][-1] in {'"', "'"}:
            user_choices[k] = user_choices[k][1:-1]

    project.accept_user_choices(UserChoices(user_choices))

    return 1
