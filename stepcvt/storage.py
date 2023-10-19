# Classes to assist in loading and saving project information to files


class ReaderWriter:
    def read(self, filename):
        """Read a file and generate a project"""

        raise NotImplementedError

    def write(self, project, filename):
        """Write out file for a project"""

        raise NotImplementedError


class JSONReaderWriter(ReaderWriter):
    pass


class YAMLReaderWriter(ReaderWriter):
    pass
