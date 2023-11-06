# Contains classes for Project information
#
# The top-level object is a Project, which can contain multiple Source
# files, with each Source file containing information on individal
# part. Each PartInfo contains a set of information, each for a
# specific task. Right now, only the STLConversionTask is specified.

from pathlib import Path
import cadquery as cq


class Project:
    def __init__(self, name: str = "", sources: list = None):
        self.name = name
        self.sources = [] if sources is None else sources

    def to_dict(self, root=None):
        return {"type": "Project", "name": self.name}

    def add_source(self, name: str, path: Path):
        for cs in self.sources:
            if cs.name == name or cs.path == path:
                raise KeyError("Cannot add source that already exists")
        self.sources.append(CADSource.load_step_file(name, path))

    @classmethod
    def from_dict(cls, d):
        Project(d["name"])
        cls.sources = [] if d["sources"] is None else d["sources"]


class CADSource:
    def __init__(self, name: str = "", path: Path = None, partinfo: list = None):
        # human-readable name, for use in the UI for this source file
        # e.g. Rapido Hotend

        self.name = name
        self.path = path
        self.partinfo = [] if partinfo is None else partinfo

    def add_partinfo(self, part_id, obj):
        # create a PartInfo object with the specified part_id, and
        # associate it with obj (which can be stored as a hidden
        # attribute). This is usually done by using the
        # PartInfo.from_part factory method.
        #
        # It is assumed that part_id and obj are obtained from
        # invoking parts()
        pass

    def parts(self):
        # returns a list of parts in the CAD model as list of (part_id, object)
        # where object corresponds to the shape in the OCCT library
        pass

    @classmethod
    def load_step_file(cls, name: str, path: Path):
        # should load the STEP file and return a CADSource object
        # the loaded file can be a hidden attribute on CADSource
        pass

    def to_dict(self):
        return {"type": "CADSource"}


class TaskInfo:
    """Base class for all part-specific task information"""

    @classmethod
    def gettype(cls, type_name):
        """Return one of the subtypes given by the name"""
        for t in cls.__subclasses__():
            if t.__name__ == type_name:
                return t
        raise TypeError(f"{type_name} is not a valid TaskInfo type")


class STLConversionInfo(TaskInfo):
    rotation: None
    linearTolerance: float
    angularTolerance: float

    def __init__(self, rotation: None, linearTolerance: float, angularTolerance: float):
        self.rotation = rotation
        self.linearTolerance = linearTolerance
        self.angularTolerance = angularTolerance

    def to_dict(self):
        return {
            "type": "STLConversionInfo",
            "rotation": self.rotation,
            "linearTolerance": self.linearTolerance,
            "angularTolerance": self.angularTolerance,
        }

    @classmethod
    def from_dict(cls, si_info):
        x = STLConversionInfo(
            rotation=si_info.get("rotation"),
            linearTolerance=si_info.get("linearTolerance"),
            angularTolerance=si_info.get("angularTolerance"),
        )
        return x

    def rotate(self, part: cq.Assembly) -> cq.Assembly:
        """returns a rotated Cadquery Assembly object"""
        # rotate takes two vector to form a rotational axis, then applies the rotation degree to that axis
        # so has to make own x, y, z axis
        for i in range(3):
            part = part.rotate(
                (0, 0, 0),
                # (1,0,0), (0,1,0), (0,0,1)
                tuple(1 if n == i else 0 for n in range(3)),
                self.rotation[i],
            )
        return part


class SlicerSettingsInfo(TaskInfo):
    """Class for containing slicer-specific settings for the part,
    organized as a key-value store. This implementation does not
    allow the setting to be repeated.
    """

    def __init__(self, slicer: str = "", **kwargs):
        self.slicer = slicer
        self.settings = {}

        for k, v in kwargs.items():
            self.settings[k] = v

    def to_dict(self):
        return {
            "type": "SlicerSettingsInfo",
            "slicer": self.slicer,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, d):
        if d.get("type", None) != "SlicerSettingsInfo":
            raise ValueError(f"Incorrect value for type, expected SlicerSettingsInfo")

        x = cls(slicer=d["slicer"], **d["settings"])
        return x


class TextInfo(TaskInfo):
    """Class for storing human-readable text for the part"""

    def __init__(self, text: str = ""):
        self.text = text

    def to_dict(self):
        return {"type": "TextInfo", "text": self.text}

    @classmethod
    def from_dict(cls, d):
        if d.get("type", None) != "TextInfo":
            raise ValueError(f"Incorrect value for type, expected TextInfo")

        return cls(text=d["text"])


class PartInfo:
    """Container for all part-specific task information"""

    def __init__(self, part_id: str = "", info: list = None, part: cq.Assembly = None):
        self.part_id = part_id
        self.info = [] if info is None else info
        self._cad: cq.Assembly = part

    def add_info(self, info: TaskInfo):
        """adds the provided info to the self.info list"""
        self.info.append(info)

    def export_to_stl(self, stl_output: Path):
        """
        search partinfo for STLConversionInfo, if found
        apply the STLConversionInfo transformations to the part
        if not found, simply export the part to the stl_output specified.
        """
        stlinfo = next(
            (info for info in self.info if isinstance(info, STLConversionInfo)), None
        )
        assem = self._cad.toCompound()
        if stlinfo is not None:
            assem = stlinfo.rotate(assem)
            cq.exporters.export(
                assem,
                stl_output,
                tolerance=stlinfo.linearTolerance,
                angularTolerance=stlinfo.angularTolerance,
            )
        cq.exporters.export(assem, stl_output)

    @classmethod
    def from_part(cls, part_id: str, part):
        """
        create and return a PartInfo object
        with the specified part_id and encapsulating the provided part object.
        """
        return cls(part_id, part=part)

    @classmethod
    def from_dict(cls, dict):
        """
        Creates a PartInfo object from dictionary containning necessary information
        """
        part_id = dict["part_id"]
        info: [STLConversionInfo] = []

        info_dict_list: [TaskInfo] = dict["info"]
        for info_dict in info_dict_list:
            info_type: type[TaskInfo] = TaskInfo.gettype(info_dict["type"])
            info.append(info_type.from_dict(info_dict))

        return cls(part_id, info)

    def to_dict(self):
        return {
            "type": "PartInfo",
            "part_id": self.part_id,
            "info": [obj.to_dict() for obj in self.info],
        }
