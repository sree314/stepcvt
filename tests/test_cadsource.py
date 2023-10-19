import pytest

from stepcvt.project import CADSource, PartInfo, TextInfo
from pathlib import Path


def test_CADSource_to_dict():
    x = CADSource(name="Rapido Hotend", path=Path("xyz.step"))
    d = x.to_dict()
    assert isinstance(d, dict)
    assert d["type"] == "CADSource"
    assert d["name"] == name
    assert d["path"] == "xyz.step"  # note: this is not a path, but a string

    # to_dict() should not return absolute paths
    # In this example, the path is not absolute, so this is fine.
    #
    # If the path was absolute, to_dict() must be given a root path,
    # which must be used to calculate the relative path to return

    p = Path(d["path"])
    assert not p.is_absolute()


def test_CADSource_to_dict_absolute():
    x = CADSource(name="Rapido Hotend", path=Path("/tmp/abc/xyz.step"))

    # note the provision of the optional root path so that to_dict()
    # can return the appropriate relative path
    d = x.to_dict(root=Path("/tmp"))
    assert isinstance(d, dict)
    assert d["type"] == "CADSource"
    assert d["name"] == name
    assert d["path"] == "abc/xyz.step"  # note: this is not a path, but a string

    p = Path(d["path"])
    assert not p.is_absolute()


def test_CADSource_to_dict_absolute_error():
    x = CADSource(name="Rapido Hotend", path=Path("/tmp/abc/xyz.step"))

    # should raise error when path is absolute, but to_dict is not
    # provided the optional root parameter

    with pytest.raises(AssertionError):
        d = x.to_dict()


def test_CADSource_from_dict():
    d = {"type": "CADSource", "name": "Rapido", "path": "abc/xyz.step"}

    # from_dict for cadsource should take a required root parameter in
    # addition to the dictionary
    cs = CADSource.from_dict(d, Path("/tmp"))
    assert isinstance(cs, CADSource)
    assert cs.name == d["name"]
    assert isinstance(cs.path, Path)

    # the root parameter should be combined with the path stored in
    # the dictionary and converted into an absolute path when processing
    assert cs.path.is_absolute()
    assert str(cs.path) == "/tmp/abc/xyz.step"


# from_dict with part information
def test_CADSource_to_dict_partinfo():
    pid1 = {
        "type": "PartInfo",
        "part_id": "first_part_id",
        "info": [{"type": "TextInfo", "text": "Hello World"}],
    }

    pid2 = {
        "type": "PartInfo",
        "part_id": "second_part_id",
        "info": [{"type": "TextInfo", "text": "Goodbye, World"}],
    }

    # this obviously relies on PartInfo.from_dict() being correct
    cs = CADSource(
        name="Rapido",
        path="xyz.step",
        partinfo=[PartInfo.from_dict(pid1), PartInfo.from_dict(pid2)],
    )

    d = cs.to_dict()

    assert isinstance(d, dict)
    assert d["type"] == "CADSource"
    assert d["name"] == cs.name
    assert d["path"] == str(cs.path)  # works here because path is relative
    assert "partinfo" in d
    assert isinstance(d["partinfo"], list)
    assert len(d["partinfo"]) == 2

    # also relies on PartInfo.to_dict() being correct
    assert all([x["type"] == "PartInfo" for x in d["partinfo"]])
