# Contains classes for Project information
#
# The top-level object is a Project, which can contain multiple Source
# files, with each Source file containing information on individal
# part. Each PartInfo contains a set of information, each for a
# specific task. Right now, only the STLConversionTask is specified.

from pathlib import Path, PurePath, PurePosixPath


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

    def to_dict(self, root=None):     
        path = PurePath(self.path)
        drive = path.drive

        if path.is_absolute():
            if not root:
                raise AssertionError("Root must be provided for absolute paths!")
            if drive:
                path = path.relative_to(drive / root)
            else:
                path = path.relative_to(root)

        return {"type": "CADSource",
                "name": self.name,
                "path": str(path.as_posix()),
                "partinfo": self.partinfo
                }
    
    def from_dict(self, root=None):       
        if root:
            path = PurePath(root / self["path"])
        else:
            path = PurePath(self["path"])

        cs = CADSource(name=self["name"], path=path, partinfo=self["partinfo"])
        return cs

class TaskInfo:
    """Base class for all part-specific task information"""


class STLConversionInfo(TaskInfo):
    rotation: None
    linearTolerance: float
    angularTolerance: float

    @classmethod
    def from_dict(cls, si_info):
        x = STLConversionInfo()
        x.rotation = si_info.get("rotation")
        x.linearTolerance = si_info.get("linearTolerance")
        x.angularTolerance = si_info.get("angularTolerance")
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
        self.part_id = ""
        self.info = [] if info is None else info

    @classmethod
    def from_dict(cls, dict):
        """
        Creates a PartInfo object from dictionary containning necessary information
        """
        part_id = dict["part_id"]
        info: [STLConversionInfo] = []

        info_dict_list = dict["info"]
        for info_dict in info_dict_list:
            info.append(STLConversionInfo.from_dict(info_dict))

        x = cls()
        x.part_id = part_id
        x.info = info

        return x

    def to_dict(self):
        return {"part_id": self.part_id, "info": [obj.to_dict() for obj in self.info]}
