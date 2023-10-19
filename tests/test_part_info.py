from stepcvt.project import PartInfo, STLConversionInfo, TextInfo


def test_PartInfo_to_dict():
    x = PartInfo(part_id="some.part.id")
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d["type"] == "PartInfo"
    assert d["part_id"] == "some.part.id"


def test_PartInfo_from_dict():
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
        ],
    }

    pi = PartInfo.from_dict(pinfo)
    assert isinstance(pi, PartInfo)

    assert pi.part_id == "some.step.file.identifier.or.name"

    assert isinstance(pi.info, list)
    assert len(pi.info) == 2

    # check that each dictionary is resolved to its correct type.
    # this should be done in from_dict by using the 'type' in each dictionary.
    assert isinstance(pi.info[0], STLConversionInfo)
    assert isinstance(pi.info[1], TextInfo)

    si = pi.info[0]
    assert si.rotation == [0, 30, 0]
    assert si.linearTolerance == 0.1
    assert si.angularTolerance == 0.2

    ti = pi.info[1]
    assert pi.text == pinfo["info"][1]["text"]
