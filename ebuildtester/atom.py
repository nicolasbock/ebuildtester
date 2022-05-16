"""An Atom."""


class AtomException(Exception):
    """An exception in this class."""
    pass


class Atom(object):

    def __init__(self, atom):
        # We expect an atom of the form [=]CATEGORY/PACKAGE[-VERSION].
        self.category = None
        self.package = None
        self.version = None

        # We don't store the optional '='.
        temp = atom.split("=")
        self.atom = temp[-1]

        try:
            self.category, self.package = self.atom.split("/")
        except ValueError:
            raise AtomException(
                "ATOM has to be of the form [=]SECTION/PACKAGE[-VERSION]")

        # Split off version.
        try:
            temp = self.package.index("-")
            if temp > -1:
                self.version = self.package[temp + 1:]
                self.package = self.package[:temp]
        except ValueError:
            pass

    def __str__(self):
        if self.version is not None:
            prefix = "="
            suffix = "-" + self.version
        else:
            prefix = ""
            suffix = ""
        return prefix + self.category + "/" + self.package + suffix

    def __eq__(self, other):
        result = (self.atom == other.atom)
        return result

    def __repr__(self):
        return "Atom(\"%s\")" % self.__str__()
