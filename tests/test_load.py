import pytest

from stepcvt.project import Project, CADSource, PartInfo, TextInfo
import models
import sys


def test_load(tmp_path):
    model_file = tmp_path / "book.step"
    book = models.book_model()
    book.save(str(model_file))

    p = Project(name="Book")

    # the add source method adds a step file as a CADSource
    # the file is added to the sources list after loading it from the stepfile.
    # this is done by calling the CADSource.load_step_file() function
    # the function does not return anything
    p.add_source(name="book", path=model_file)
    source = p.sources[-1]

    for partid, obj in source.parts():
        source.add_partinfo(partid, obj)

    x = p.to_dict(root=model_file.parent)

    p2 = Project.from_dict(x, tmp_path)

    # this passes the path which is where the JSON file lives, since
    # usually that is where all the paths inside the file are relative to.
    #
    # pretend the JSON file lives in tmp_path

    # the load function calls load on all the components of a project,
    # passing them the path

    p2.load(tmp_path)

    # This uses internal attributes, but since this test is closely
    # coupled to implementation, this is okay
    for s in p2.sources:
        assert s._CADSource__step is not None
        for part in s.partinfo:
            assert part._cad is not None
