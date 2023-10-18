# Contains classes for Project information
#
# The top-level object is a Project, which can contain multiple Source
# files, with each Source file containing information on individal
# part. Each PartInfo contains a set of information, each for a
# specific task. Right now, only the STLConversionTask is specified.


class Project:
    pass

class Source:
    pass

class PartInfo:
    pass

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
    
