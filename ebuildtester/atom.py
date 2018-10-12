import re

from portage.dbapi.dep_expand import dep_expand
from portage.versions import cpv_getversion
import portage.exception as pe


class AtomException(Exception):
    pass


class Atom(object):

    def __init__(self, atom):
        try:
            # We expect an atom of the form [=]CATEGORY/PACKAGE[-VERSION].
            self.atom = dep_expand(str(atom))
        except pe.InvalidAtom:
            raise AtomException(
                "ATOM has to be of the form [=]SECTION/PACKAGE[-VERSION]")

        self.category = self.atomCategory()
        self.package = self.atomName()
        self.version = self.atomVersion()
        self.repo = self.atomRepo()

    def _splitPackage(self):
        return self.atom.split("/", 1)

    def atomCategory(self):
        """Returns the package category without name"""
        category = re.sub('^.*(=|<|>|~)', '', self._splitPackage()[0])
        if category == 'null':
            raise AtomException(
                "ATOM has to be of the form [=]SECTION/PACKAGE[-VERSION]")

        return category

    def atomName(self):
        """Returns the package name without category"""
        pkg = self._splitPackage()[1]
        suffix = ['-' + str(self.atomVersion()),
                  '::' + str(self.atomRepo())]
        for s in suffix:
            pkg = pkg.replace(s, '')

        return pkg

    def atomVersion(self):
        """Returns the package version"""

        return cpv_getversion(self.atom)

    def atomRepo(self):
        """Returns the package repository"""
        pkg = self._splitPackage()[1].split("::", 1)
        if len(pkg) == 2:
            return pkg[1]

    def atomCatName(self):
        """Returns the package category and name without version"""
        return "/".join([self.category, self.package])

    def atomComplete(self):
        """Returns a portage compatible string representation"""
        suff = []
        pref = ''
        if self.version is not None:
            suff += ['-' + self.version]
            pref = '='

        if self.repo is not None:
            suff += ['::' + self.repo]

        return (pref + self.category + '/' + self.package +
                ''.join([str(s) for s in suff]))

    def __str__(self):
        return self.atomComplete()

    def __eq__(self, other):
        result = (self.category == other.category
                  and self.package == other.package
                  and self.version == other.version)

        return result

    def __repr__(self):
        return "Atom(\"%s\")" % self.__str__()
