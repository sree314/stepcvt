# Contains classes for Project information
#
# The top-level object is a Project, which can contain multiple Source
# files, with each Source file containing information on individal
# part. Each PartInfo contains a set of information, each for a
# specific task. Right now, only the STLConversionTask is specified.


class Project:
    pass


class CADSource:
    def __init__(self):
        pass

    def to_dict(self):
        return {"type": "CADSource"}

    pass


class STLConversionInfo:
    pass


class PartInfo:
    def __init__(self):
        self.part_id = ""
        self.info = []

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
