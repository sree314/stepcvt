import pytest

from stepcvt.project import Project, CADSource, PartInfo, TextInfo
import models


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


def test_Project_from_dict_to_dict_roundtrip():
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
    d2 = p.to_dict()

    assert d2["type"] == d["type"]
    assert d2["name"] == d2["name"]
    assert len(d2["sources"]) == 2

    # assume cad_source.to_dict() works correctly
    # so do not check contents of the dictionary, other than the type
    for s in d2["sources"]:
        assert s["type"] == "CADSource"


def test_Project_from_file(tmp_path):
    model_file = tmp_path / "book.step"
    book = models.book_model()
    book.save(str(model_file))

    p = Project(name="Book")

    # the add source method adds a step file as a CADSource
    # the file is added to the sources list after loading it from the stepfile.
    # this is done by calling the CADSource.load_step_file() function
    # the function does not return anything
    p.add_source(name="book", path=model_file)

    assert len(p.sources) == 1
    assert isinstance(p.sources[0], CADSource)
    assert p.sources[0].name == "book"
    assert p.sources[0].path == model_file


def test_Project_from_file_dup(tmp_path):
    model_file = tmp_path / "book.step"
    book = models.book_model()
    book.save(str(model_file))

    p = Project(name="Book")

    # the add source method adds a step file as a CADSource

    # refuse to add sources with the same name twice
    p.add_source(name="book", path=model_file)

    with pytest.raises(KeyError):
        p.add_source(name="book", path=model_file)
