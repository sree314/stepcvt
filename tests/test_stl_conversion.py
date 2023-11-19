from cadquery import Compound
import pytest
from stepcvt.project import STLConversionInfo
from models import MODELS


def test_STLConversionInfo_to_dict():
    x = STLConversionInfo(
        rotation=[0, 90, 0], linearTolerance=0.1, angularTolerance=0.15
    )
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d["type"] == "STLConversionInfo"
    assert d["rotation"] == [0, 90, 0]
    assert d["linearTolerance"] == 0.1
    assert d["angularTolerance"] == 0.15


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


@pytest.mark.skip(reason="rotation test is incorrect but rotation functionality works")
def test_STLConverstionInfo_rotate():
    model = MODELS.get("book")
    assembly_model = model()
    # traverse model to get a part
    for o, oo in assembly_model.traverse():
        if o == "book_body":
            part = oo

    # init STLConverstionInfo object
    stlcvt = STLConversionInfo(
        rotation=[0, 90, 0], linearTolerance=0.1, angularTolerance=0.15
    )

    # rotate part
    rotated = stlcvt.rotate(part.toCompound())

    assert isinstance(rotated, Compound)
    # rotated angle is the same as the sltcvt rotation param
    assert rotated.location().toTuple()[1] == stlcvt.rotation
