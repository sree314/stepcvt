from stepcvt.project import PartInfo, STLConversionInfo, TextInfo, SlicerSettingsInfo
import models

pinfo = {
    "type": "PartInfo",
    "part_id": "some.step.file.identifier.or.name",
    "info": [
        {
            "type": "STLConversionInfo",
            "rotation": [0, 30, 0],
            "linearTolerance": 0.1,
            "angularTolerance": 0.2,
        },
        {"type": "TextInfo", "text": "Part must be printed using clear filament."},
        {
            "type": "SlicerSettingsInfo",
            "slicer": "Cura",
            "settings": {"layerHeight": "0.2mm", "infillDensity": 0.4},
        },
    ],
}


def test_PartInfo_to_dict():
    x = PartInfo(part_id="some.part.id")
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d["type"] == "PartInfo"
    assert d["part_id"] == "some.part.id"


def test_PartInfo_from_dict():
    pi = PartInfo.from_dict(pinfo)
    assert isinstance(pi, PartInfo)

    assert pi.part_id == "some.step.file.identifier.or.name"

    assert isinstance(pi.info, list)
    assert len(pi.info) == 3

    # check that each dictionary is resolved to its correct type.
    # this should be done in from_dict by using the 'type' in each dictionary.
    assert isinstance(pi.info[0], STLConversionInfo)
    assert isinstance(pi.info[1], TextInfo)
    assert isinstance(pi.info[2], SlicerSettingsInfo)

    si = pi.info[0]
    assert si.rotation == [0, 30, 0]
    assert si.linearTolerance == 0.1
    assert si.angularTolerance == 0.2

    ti = pi.info[1]
    assert ti.text == pinfo["info"][1]["text"]

    sli = pi.info[2]
    assert sli.slicer == pinfo["info"][2]["slicer"]
    assert sli.settings == pinfo["info"][2]["settings"]


def test_PartInfo_from_part():
    book = models.book_model()

    for o, oo in book.traverse():
        pi = PartInfo.from_part(o, oo)
        assert isinstance(pi, PartInfo)
        assert pi.part_id == o
        assert pi._cad is oo  # use _cad as the hidden attribute
        break  # do this only for the first object
