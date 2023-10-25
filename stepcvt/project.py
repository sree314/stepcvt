# Contains classes for Project information
#
# The top-level object is a Project, which can contain multiple Source
# files, with each Source file containing information on individal
# part. Each PartInfo contains a set of information, each for a
# specific task. Right now, only the STLConversionTask is specified.

from pathlib import Path


class Project:
    def __init__(self, name: str = "", sources: list = None):
        self.name = name
        self.sources = [] if sources is not None else sources

    def to_dict(self, root=None):
        pass

    @classmethod
    def from_dict(cls, self):
        pass


class CADSource:
    def __init__(self, name: str = "", path: Path = None, partinfo: list = None):
        # human-readable name, for use in the UI for this source file
        # e.g. Rapido Hotend

        self.name = name
        self.path = path
        self.partinfo = [] if partinfo is None else partinfo

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

    def __init__(self, part_id: str = "", info: list = None):
        self.part_id = part_id
        self.info = [] if info is None else info

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
