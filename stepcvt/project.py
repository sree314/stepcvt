# Contains classes for Project information
#
# The top-level object is a Project, which can contain multiple Source
# files, with each Source file containing information on individal
# part. Each PartInfo contains a set of information, each for a
# specific task. Right now, only the STLConversionTask is specified.


class Project:
    pass

class CADSource:
    pass

class PartInfo:
    pass

class STLConversionInfo:
    xRotation = 0
    yRotation = 0
    zRotation = 0
    rotation = None
    linearTolerance = 0.1
    angularTolerance = 0.1
    
    def __init__(self):
        self.rotation = [xRotation, yRotation, zRotation]

    def to_dict(self):
        return {'type':'STLConversionInfo', 'rotation':self.rotation, 'linearTolerance':self.linearTolerance, 'angularTolerance':self.angularTolerance}