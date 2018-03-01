class AtomException(Exception):

    def __init__(self, msg):
        super(AtomException, self).__init__(msg)


class Atom(object):

    def __init__(self, atom):
        temp = atom.split("=")
        self.atom = temp[-1]
        try:
            self.section, self.package = self.atom.split("/")
        except ValueError:
            raise AtomException(
                "ATOM has to be of the form SECTION/PACKAGE[-VERSION]")
        temp = self.package.split("-")
        if len(temp) == 1:
            self.package_name = self.package
            self.package_version = None
        else:
            self.package_name, self.package_version = temp

    def __str__(self):
        if self.package_version is not None:
            prefix = "="
        else:
            prefix = ""
        return prefix + self.atom

    def __repr__(self):
        return self.atom
