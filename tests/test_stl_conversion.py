from stepcvt.project import STLConversionInfo


def test_STLConversionInfo_to_dict():
    x = STLConversionInfo()
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d["type"] == "STLConversionInfo"


def test_STLConversionInfo_from_dict():
    si_info = {
        "rotation": [0, 0, 0],
        "linearTolerance": 0.1,
        "angularTolerance": 0.1,
    }

    si = STLConversionInfo.from_dict(si_info)
    assert isinstance(si, STLConversionInfo)
    assert si.rotation == [0, 0, 0]
    assert si.linearTolerance == 0.1
    assert si.angularTolerance == 0.1
