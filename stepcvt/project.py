# Contains classes for Project information
#
# The top-level object is a Project, which can contain multiple Source
# files, with each Source file containing information on individal
# part. Each PartInfo contains a set of information, each for a
# specific task. Right now, only the STLConversionTask is specified.

from pathlib import Path, PurePath
from typing import Type
from stepcvt import stepreader, choices
import cadquery as cq


class Project:
    def __init__(
        self,
        name: str = "",
        sources: list = None,
        available_choices: choices.Choices = None,
    ):
        self.name = name
        self.sources = [] if sources is None else sources
        self.available_choices = (
            available_choices if available_choices is not None else choices.Choices([])
        )
        self.user_choices = choices.UserChoices(dict())

    def to_dict(self, root=None):
        # Roundtrip test throws error in CADSource from_dict() method
        return {"type": "Project", "name": self.name, "sources": self.sources}

    def add_source(self, name: str, path: Path):
        # proj from file test says p.sources not type CADSource
        #  - Because CADSource to_dict() not returning proper type
        # proj from file Dup test says no keyerror raised for duplicate
        #  - Because add_source not working
        if not self.sources:
            for cs in self.sources:
                if cs.name == name or cs.path == path:
                    raise KeyError("Cannot add source that already exists")
        cs = CADSource.load_step_file(name, path)
        self.sources.append(cs.to_dict(root=path))

    @classmethod
    def from_dict(cls, d):
        # TestFromDict throws error in CADSource from_Dict() method
        if "sources" in d:
            return cls(d["name"], CADSource.from_dict(d["sources"]))
        else:
            return cls(d["name"])

    def accept_user_choices(self, user_choices: choices.UserChoices):
        # validate user choices
        self.available_choices.validate(user_choices)
        self.user_choices = user_choices

        # update dependent properties in partinfo
        for sc in self.sources:
            for info in sc.partinfo:
                info.update_from_choices(self.user_choices)


class CADSource:
    def __init__(self, name: str = "", path: Path = None, partinfo: list = None):
        # human-readable name, for use in the UI for this source file
        # e.g. Rapido Hotend
        self.name = name
        self.path = path
        self.partinfo = [] if partinfo is None else partinfo
        self.__step = None

    def add_partinfo(self, part_id, obj):
        # create a PartInfo object with the specified part_id, and
        # associate it with obj (which can be stored as a hidden
        # attribute). This is usually done by using the
        # PartInfo.from_part factory method.
        #
        # It is assumed that part_id and obj are obtained from
        # invoking parts()
        dict = dict.fromkeys(part_id, obj)
        partinfo = PartInfo.from_dict(dict)

        return partinfo

    # def parts(self, assemblies=None):  # we should pass in self._step.assemblies, which is a list object
    #     # returns a list of parts in the CAD model as list of (part_id, object)
    #     # where object corresponds to the shape in the OCCT library
    #     assemblies = self._CADSource__step.assemblies
    #     result = []
    #     for obj in assemblies:
    #         # If the current object has a shape, append it to the results
    #         if obj["shape"] is not None:
    #             result.append((obj["name"], obj["shape"]))
    #         # If the current object doesn't have a shape, recursively go into its 'shapes' list
    #         elif obj["shapes"] is not None:
    #             result.extend(CADSource.parts(obj["shapes"]))

    #     return result

    def parts(self, assemblies=None):
        if assemblies is None:
            assemblies = self._CADSource__step.assemblies
        return self._recursive_parts(assemblies)

    def _recursive_parts(self, assemblies):
        result = []
        for obj in assemblies:
            if obj["shape"] is not None:
                result.append((obj["name"], obj["shape"]))
            elif obj["shapes"] is not None:
                result.extend(self._recursive_parts(obj["shapes"]))
        return result

    @classmethod
    def load_step_file(cls, name: str, path: Path):
        # should load the STEP file and return a CADSource object
        # the loaded file can be a hidden attribute on CADSource
        cs = cls(name=name, path=path)
        sr = stepreader.StepReader()

        cs._CADSource__step = sr.load(str(path))

        return cs

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

        return {
            "type": "CADSource",
            "name": self.name,
            "path": str(path.as_posix()),
            "partinfo": self.partinfo,
        }

    def from_dict(self, root=None):
        if root:
            path = PurePath(root / self["path"])
        else:
            path = PurePath(self["path"])

        partinfo = self.get("partinfo", [])
        cs = CADSource(name=self["name"], path=path, partinfo=partinfo)
        return cs


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

    def rotate(self, part: cq.Shape) -> cq.Shape:
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


class CountInfo(TaskInfo):
    """Class for storing count for the part"""

    def __init__(self, count: int = 1):
        self.count = count

    def to_dict(self):
        return {"type": "CountInfo", "count": self.count}

    @classmethod
    def from_dict(cls, d):
        if d.get("type", None) != "CountInfo":
            raise ValueError(f"Incorrect value for type, expected CountInfo")

        return cls(count=d["count"])


class PartInfo:
    """Container for all part-specific task information"""

    def __init__(
        self,
        part_id: str = "",
        info: list = None,
        part: cq.Assembly = None,
        default_selected=False,
        count=1,
        scale=1.0,
    ):
        self.part_id = part_id
        self.info = [] if info is None else info
        self._cad: cq.Assembly = part
        self._default_selected = default_selected
        self._default_count = count
        self._default_scale = scale
        self.selected = self._default_selected
        self.count = self._default_count
        self.scale = self._default_scale
        self.choice_effects: [choices.ChoiceEffect] = []

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
            info_type: Type[TaskInfo] = TaskInfo.gettype(info_dict["type"])
            info.append(info_type.from_dict(info_dict))

        return cls(part_id, info)

    def to_dict(self):
        return {
            "type": "PartInfo",
            "part_id": self.part_id,
            "info": [obj.to_dict() for obj in self.info],
        }

    def update_from_choices(self, user_choices: choices.UserChoices):
        """Update dependent properties using provided UserChoices,
        if None, then reset those properties to their default value.
        Choices with conflicting value is undefined behaviour"""
        if user_choices is None:
            self.selected = self._default_selected
            self.count = self._default_count
            self.scale = self._default_scale
            return

        for effect in filter(lambda e: e.cond.eval(user_choices), self.choice_effects):
            if isinstance(effect, choices.RelativeCountEffect):
                self.count += effect.count_delta
            elif isinstance(effect, choices.AbsoluteCountEffect):
                self.count = effect.count
            elif isinstance(effect, choices.SelectionEffect):
                self.selected = True
            elif isinstance(effect, choices.ScaleEffect):
                self.scale = effect.scale
            else:
                raise SyntaxError(f"Unknown ChoiceEffect {effect}")
