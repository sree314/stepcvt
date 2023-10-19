import pytest

from stepcvt.project import Project, CADSource, PartInfo, TextInfo


def test_Project_to_dict():
    p = Project(name="Name")

    d = p.to_dict()

    assert d["type"] == "Project"
    assert d["name"] == "Name"


def test_Project_from_dict():
    d = {"type": "Project", "name": "Name"}

    p = Project.from_dict(d)

    assert isinstance(p, Project)
    assert p.name == d["name"]
    assert len(p.sources) == 0


def test_Project_from_dict_source():
    d = {
        "type": "Project",
        "name": "Name",
        "sources": [
            {
                "type": "CADSource",
                "name": "upper",
                "path": "upper.step",
                "partinfo": [],
            },
            {
                "type": "CADSource",
                "name": "lower",
                "path": "lower.step",
                "partinfo": [],
            },
        ],
    }

    p = Project.from_dict(d)

    assert isinstance(p, Project)
    assert p.name == d["name"]
    assert len(p.sources) == 2
    assert all([isinstance(x, CADSource) for x in p.sources])

    assert p.sources[0].name == "upper"
    assert p.sources[1].name == "lower"
