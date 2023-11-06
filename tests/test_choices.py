from stepcvt.choices import *
from stepcvt.project import PartInfo, Project
import math
import pytest


project_available_choices = Choices(
    [
        SingleChooser(
            "Nevermore Model Version Number",
            "NevermoreModel",
            [ChoiceValue("V4", "V4"), ChoiceValue("V6", "V6")],
        ),
        MultiChooser(
            "Optional Printer Features",
            "PrinterOptions",
            [
                ChoiceValue("HEPA Filter", "Filter"),
                ChoiceValue("Lights", "Lights"),
                ChoiceValue(
                    "Lights controller",
                    "LightsCtrl",
                    ChoiceExpr("'Lights' in PrinterOptions"),
                ),
            ],
        ),
    ]
)

user_choices = UserChoices(
    {"NevermoreModel": "V4", "PrinterOptions": {"Filter", "Lights"}}
)

project = Project("Nevermore", available_choices=project_available_choices)
project.accept_user_choices(user_choices)

partinfo = PartInfo("LightsMount", default_selected=False, count=0)
partinfo.root_project = project  # This would be set in a more systematic way


def test_choice_expr():
    choice_expr_v6 = ChoiceExpr("NevermoreModel == 'V6' and 'Filter' in PrinterOptions")
    choice_expr_v4 = ChoiceExpr("NevermoreModel == 'V4'")
    assert set(choice_expr_v6.vars()) == {"NevermoreModel", "PrinterOptions"}
    assert choice_expr_v4.vars() == ["NevermoreModel"]
    assert not choice_expr_v6.eval(user_choices)
    assert choice_expr_v4.eval(user_choices)


def test_selection_effect():
    partinfo.choice_effects.append(
        SelectionEffect(ChoiceExpr("'Lights' in PrinterOptions"))
    )
    assert partinfo.selected


def test_relative_count_effect():
    partinfo.choice_effects.append(
        RelativeCountEffect(ChoiceExpr("'Lights' in PrinterOptions"), 2)
    )
    partinfo.choice_effects.append(
        RelativeCountEffect(ChoiceExpr("'Filter' in PrinterOptions"), 1)
    )
    assert partinfo.count == 3

    partinfo.choice_effects.append(
        AbsoluteCountEffect(ChoiceExpr("NevermoreModel == 'V4'"), 2)
    )
    assert partinfo.count == 2


def test_scale_effect():
    assert math.isclose(partinfo.scale, 1.0)
    partinfo.choice_effects.append(
        ScaleEffect(ChoiceExpr("NevermoreModel == 'V4'"), 1.2)
    )
    assert math.isclose(partinfo.scale, 1.2)


def test_invalid_user_choice():
    # potentially better error messages?
    with pytest.raises(
        AttributeError, match="Unidentified options '.*' in 'PrinterOptions'"
    ):
        invalid_choices = UserChoices(
            {"PrinterOptions": {"HEPA Filter", "Infrared Lights"}}
        )
        project.accept_user_choices(invalid_choices)
    with pytest.raises(
        AttributeError, match="Precondition for 'LightsCtrl' not satisfied"
    ):
        invalid_pre_cond = UserChoices({"PrinterOptions": {"LightsCtrl"}})
        project.accept_user_choices(invalid_pre_cond)
