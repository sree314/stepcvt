from stepcvt.project import CADSource


def test_CADSource_to_dict():
    x = CADSource()
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d["type"] == "CADSource"
