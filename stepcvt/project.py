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
    def __init__(self, id=None, list_of_objects=None):
        self.part_id = id
        self.objects = list_of_objects
    
    def to_dict(self):
        return {'part_id': self.part_id, 
                'info': [obj.to_dict() for obj in self.objects]}       
        

class STLConversionInfo:
    pass
