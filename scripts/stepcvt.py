import sys
sys.path.append("../")
from stepcvt.cli import *
import argparse

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="")
    p.add_argument("-j", dest="jsonfile", type=str, help="Provide the jsonfile")

    sp = p.add_subparsers(dest='command')

    app = sp.add_parser("addpart", help="Add a part")
    # can be no id specified if --all is used
    app.add_argument("id", nargs="*", help="Specify partid for parts to be added")
    app.add_argument("--all",
                     action="store_true",
                     help="Include this if you want to add all of the parts")
    app.set_defaults(func=part.add_part)

    rpp = sp.add_parser("rmpart", help="Remove a part")
    rpp.add_argument("id", nargs="+", help="Specify partid for parts to be removed")
    rpp.set_defaults(func=part.remove_part)

    epp = sp.add_parser("editpart", help="Change part properties")
    # can only change one part at a time
    epp.add_argument("id", help="Specify partid for the part to be edited")
    epp.add_argument("-c", "--count", type=int, help="Change the count of the part")
    epp.set_defaults(func=part.edit_part)


    # --- Choices ---
    p_choices = sp.add_parser("choices")
    # nested subparser possible?
    # stepcvt choices add-chooser [--choices-type TYPE] TEXT VARNAME (TEXT:VARNAME[:COND])+
    # example:
    # stepcvt choices add-chooser --choice-type single "Printer Options" "options"
    #   --values "HEPA filter":"Filter" "Build area lights":"Lights":"version=='V6'"
    subp_choices = p_choices.add_subparsers(help="actions on choices")
    subp_choices_add = subp_choices.add_parser("add-chooser", help="create a choice")
    subp_choices_add.set_defaults(func=choices.choices_add)
    subp_choices_add.add_argument(
        "--choice-type",
        choices=["single", "multi", "boolean"],
        default="single",
        help="chooser type",
    )
    subp_choices_add.add_argument("text")
    subp_choices_add.add_argument("varname")
    subp_choices_add.add_argument(
        "values",
        default=set(),
        nargs="*",
        help="list of potential value and their optional condition, 'text':'value'[:'cond'], "
             "use [sel_value, unsel_value] for boolean chooser",
    )

    # stepcvt choices edit VARNAME [--choice-value TEXT] (TEXT:VARNAME[:COND])+
    # example:
    # stepcvt choices edit "options" --choice-value "Lights" "Build area lights":"Lights":"version=='V4'"
    subp_choices_edit = subp_choices.add_parser("edit", help="replace ChoiceValue(s) of a Chooser")
    subp_choices_edit.set_defaults(func=choices.choices_edit)
    subp_choices_edit.add_argument(
        "varname", help="select specific varname of the Chooser to modify"
    )
    subp_choices_edit.add_argument(
        "--choice-value",
        help="if this is specified, select specific ChoiceValue, otherwise select all ChoiceValue's."
             "For boolean chooser, this value is limited to {select, unselect}.",
    )
    subp_choices_edit.add_argument(
        "new_values", nargs="*",
        help="new value(s) to replace the selected ChoiceValue or ChoiceValue list. "
             "Format follows 'text':'value'[:'cond']",
    )

    # stepcvt choices remove VARNAME [--choice-value TEXT] [--cond]
    # example:
    # stepcvt choices remove "options" --choice-value "Lights" --cond
    subp_choices_remove = subp_choices.add_parser("remove", help="remove a chooser or any component in a chooser")
    subp_choices_remove.set_defaults(func=choices.choices_remove)
    subp_choices_remove.add_argument("varname", help="specify which chooser")
    subp_choices_remove.add_argument("--choice-value", help="specify a choice value to in the chooser to be removed")
    subp_choices_remove.add_argument("--cond", help="remove the condition part of a choice value")

    # stepcvt choices apply (VARNAME=VALUE(,EXTRA_VALUES)*)+
    # example:
    # stepcvt choices apply Version=v6 Options=Lights,Filter
    subp_choices_apply = subp_choices.add_parser("apply", help="apply user choice to ")
    subp_choices_apply.add_argument("choices_input", nargs="*",
                                    help="List of users choices in the format: varname=value[,extra_values]")

    args = p.parse_args()
    sys.exit(args.func(args))
