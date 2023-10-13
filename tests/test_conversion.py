from stepcvt.project import *

def test_STLConversionInfo_to_dict():
    x = STLConversionInfo()
    d = x.to_dict()
    assert isinstance(d, dict)
