import pytest
from stepcvt.project import SlicerSettingsInfo, TextInfo


def test_SlicerSettingsInfo_to_dict():
    x = SlicerSettingsInfo(slicer="Cura", supports=True, adhesion="brim")

    d = x.to_dict()
    assert isinstance(d, dict)
    assert d["type"] == "SlicerSettingsInfo"
    assert d["slicer"] == "Cura"
    assert d["settings"]["supports"] == True
    assert d["settings"]["adhesion"] == "brim"


def test_SlicerSettingsInfo_from_dict():
    ssi_info = {
        "type": "SlicerSettingsInfo",
        "slicer": "PrusaSlicer",
        "settings": {"supports": True, "speed": 50},
    }

    si = SlicerSettingsInfo.from_dict(ssi_info)
    assert isinstance(si, SlicerSettingsInfo)
    assert si.slicer == ssi_info["slicer"]
    assert si.settings["supports"] == ssi_info["settings"]["supports"]
    assert si.settings["speed"] == ssi_info["settings"]["speed"]


def test_SlicerSettings_from_dict_notype():
    ssi_info = {"slicer": "PrusaSlicer", "settings": {"supports": True, "speed": 50}}

    with pytest.raises(ValueError) as exc:
        si = SlicerSettingsInfo.from_dict(ssi_info)


def test_SlicerSettings_from_dict_incorrecttype():
    ssi_info = {"type": "TextInfo", "text": "Hello, World!"}

    with pytest.raises(ValueError) as exc:
        si = SlicerSettingsInfo.from_dict(ssi_info)


def test_TextInfo_from_dict():
    text_info = {"type": "TextInfo", "text": "Hello, World!"}

    ti = TextInfo.from_dict(text_info)
    assert isinstance(ti, TextInfo)
    assert ti.text == text_info["text"]


def test_TextInfo_to_dict():
    ti = TextInfo(text="Goodbye, World!")
    tid = ti.to_dict()
    assert tid["type"] == "TextInfo"
    assert tid["text"] == "Goodbye, World!"


def test_TextInfo_from_dict_notype():
    ti_info = {
        "text": "Hello, World!",
    }

    with pytest.raises(ValueError) as exc:
        si = TextInfo.from_dict(ti_info)


def test_TextInfo_from_dict_incorrecttype():
    ssi_info = {"type": "SlicerSettings", "slicer": "Slic3r", "settings": {}}

    with pytest.raises(ValueError) as exc:
        si = TextInfo.from_dict(ssi_info)
