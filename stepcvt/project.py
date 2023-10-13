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
    roll = 0
    pitch = 0
    yaw = 0
    rotation = [roll, pitch, yaw]
    linTol = 0.1
    angTol = 0.1
    
    def to_dict(self):
        return {'type':'STLConversionInfo', 'rotation':self.rotation, 'linearTolerance':self.linTol, 'angularTolerance':self.angTol}