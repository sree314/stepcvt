from stepcvt.project import *

def test_STLConversionInfo_to_dict():
    x = STLConversionInfo()
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d['type'] == 'STLConversionInfo'

def test_STLConversionInfo_from_dict():
    si_info = {
        'rotation': [0,0,0],
        'linearTolerance': 0.1,
        'angularTolerance': 0.1,
        }

    si = STLConversionInfo.from_dict(si_info)
    assert isinstance(si, STLConversionInfo)
    assert si.rotation == [0,0,0]
    assert si.linearTolerance == 0.1
    assert si.angularTolerance == 0.1

def test_PartInfo_to_dict():
    x = PartInfo()
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d['type'] == 'PartInfo'

def test_PartInfo_from_dict():
    pinfo = {
        'part_id': 'some.step.file.identifier.or.name',
        'info': [
            {'type': 'STLConversionInfo',
             'rotation': [0,30,0],
             'linearTolerance': 0.1,
             'angularTolerance': 0.2,
             }
        ]
    }

    pi = PartInfo.from_dict(pinfo)
    assert isinstance(pi, PartInfo)
    assert pi.part_id == 'some.step.file.identifier.or.name'
    assert isinstance(pi.info, list)
    assert len(pi.info) == 1
    assert isinstance(pi.info[0], STLConversionInfo)

    si = pi.info[0]
    assert si.rotation == [0, 30, 0]
    assert si.linearTolerance == 0.1
    assert si.angularTolerance == 0.2

def test_CADSource_to_dict():
    x = Source()
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d['type'] == 'CADSource'
