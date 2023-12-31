from stepcvt.choices import *
from stepcvt.project import PartInfo, Project, CADSource
import math
import pytest

choices_dict = [
    {
        "type": "SingleChooser",
        "text": "Nevermore Model Version Number",
        "varname": "NevermoreModel",
        "values": [{"text": "V4", "value": "V4"}, {"text": "V6", "value": "V6"}],
    },
    {
        "type": "MultiChooser",
        "text": "Optional Printer Features",
        "varname": "PrinterOptions",
        "values": [
            {"text": "HEPA Filter", "value": "Filter"},
            {"text": "Lights", "value": "Lights"},
            {
                "text": "Lights controller",
                "value": "LightsCtrl",
                "cond": "'Lights' in PrinterOptions",
            },
        ],
    },
]

user_choices = UserChoices.from_dict(
    {"NevermoreModel": "V4", "PrinterOptions": {"Filter", "Lights"}}
)

project = Project("Nevermore", available_choices=Choices.from_dict(choices_dict))

partinfo = PartInfo("LightsMount", default_selected=False, count=0)
project.sources.append(CADSource("Lights Mount", None, [partinfo]))
project.accept_user_choices(user_choices)


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
    partinfo.choice_effects.append(
        SelectionEffect.from_dict(
            {"type": "SelectionEffect", "cond": "'Lights' in PrinterOptions"}
        )
    )
    partinfo.update_from_choices(project.user_choices)
    assert partinfo.selected


def test_relative_count_effect():
    partinfo.choice_effects.append(
        RelativeCountEffect.from_dict(
            {
                "type": "RelativeCountEffect",
                "cond": "'Lights' in PrinterOptions",
                "count_delta": 2,
            }
        )
    )
    partinfo.choice_effects.append(
        RelativeCountEffect.from_dict(
            {
                "type": "RelativeCountEffect",
                "cond": "'Filter' in PrinterOptions",
                "count_delta": 1,
            }
        )
    )
    partinfo.update_from_choices(project.user_choices)
    assert partinfo.count == 3

    partinfo.choice_effects.append(
        AbsoluteCountEffect.from_dict(
            {
                "type": "AbsoluteCountEffect",
                "cond": "NevermoreModel == 'V4'",
                "count": 2,
            }
        )
    )
    partinfo.update_from_choices(project.user_choices)
    assert partinfo.count == 2


def test_scale_effect():
    assert math.isclose(partinfo.scale, 1.0)
    partinfo.choice_effects.append(
        ScaleEffect.from_dict(
            {"type": "ScaleEffect", "cond": "NevermoreModel == 'V4'", "scale": 1.2}
        )
    )
    partinfo.update_from_choices(project.user_choices)
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


def test_choice_expr_to_dict():
    assert project.available_choices.to_dict() == choices_dict
