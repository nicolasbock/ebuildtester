
import re


class AtomException(Exception):
    pass


class Atom(object):
    """A Gentoo Atom consists of the:
    category
    package (name)
    version
    of a Gentoo package"""

    def __init__(self, atom):
        """We expect an atom of the form [=]CATEGORY/PACKAGE[-VERSION]."""
        self.category = ""
        self.package = ""
        self.version = ""

        # strip off an optional leading =
        atom = str(atom)
        if atom[0] == "=":
            atom = atom[1:]

        slashparts = atom.split("/")
        if len(slashparts) == 1:
            raise AtomException("Atoms must be of the form [=]CAT/PKG[-VER]!")
        else:
            self.category = slashparts[0]
            self._split_version(slashparts[1])

    def _split_version(self, pkg):
        """Splits the version from an atom with version"""
        minusparts = pkg.split("-")
        if len(minusparts) == 1:
            # no version given
            self.package = pkg
        else:
            # parse the name-version part
            while 1:
                try:
                    p = minusparts.pop(0)
                except IndexError:
                    break

                # try a number after a '-'
                if re.match('[0-9]+', p):
                    # version starts here
                    self.version = "-".join([p] + minusparts)
                    break
                else:
                    # append back to name
                    if self.package == "":
                        self.package = p
                    else:
                        self.package = "-".join([self.package, p])

    def atomName(self):
        """Returns the package name without category"""
        return self.package

    def atomCategory(self):
        """Returns the package category without name"""
        return self.category

    def atomVersion(self):
        """Returns the package version"""
        return self.version

    def atomCatName(self):
        """Returns the package category and name without version"""
        return "/".join([self.category, self.package])

    def atomString(self):
        """Returns a portage compatible string representation"""
        if self.version == "":
            return self.atomCatName()

        return ("=" + "/".join([self.category,
                                "-".join([self.package,
                                          self.version])]))

    def __str__(self):
        return self.atomString()

    def __eq__(self, other):
        result = (self.category == other.category
                  and self.package == other.package
                  and self.version == other.version)
        return result

    def __repr__(self):
        return "Atom(\"%s\")" % self.__str__()
