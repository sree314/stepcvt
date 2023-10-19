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


class PartInfo:
    def __init__(self, id: str, info: [STLConversionInfo]):
        self.part_id = id
        self.info = info

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

        return cls(part_id, info)

    def to_dict(self):
        return {"part_id": self.part_id, "info": [obj.to_dict() for obj in self.info]}


class STLConversionInfo:
    rotation: []
    linearTolerance: float
    angularTolerance: float
    @classmethod 
    def from_dict(cls, si_info):
        x = STLConversionInfo() 
        x.rotation = si_info.get('rotation')
        x.linearTolerance = si_info.get('linearTolerance')
        x.angularTolerance = si_info.get('angularTolerance')
        return x
    
