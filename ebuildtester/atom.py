"""An Atom."""

import re


class AtomException(Exception):
    """An exception in this class."""
    pass


# from lib/portage/version.py
# PMS 3.1.3: A slot name may contain any of the characters [A-Za-z0-9+_.-].
# It must not begin with a hyphen or a dot.
_slot = r"([\w+][\w+.-]*)"

# 2.1.1 A category name may contain any of the characters [A-Za-z0-9+_.-].
# It must not begin with a hyphen or a dot.
_cat = r"[\w+][\w+.-]*"

# 2.1.2 A package name may contain any of the characters [A-Za-z0-9+_-].
# It must not begin with a hyphen,
# and must not end in a hyphen followed by one or more digits.
_pkg = r"[\w+][\w+-]*?"

_v = r"(\d+)((\.\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\d*)*)"
_rev = r"\d+"
_vr = _v + "(-r(" + _rev + "))?"

_cp = "(" + _cat + "/" + _pkg + "(-" + _vr + ")?)"
_cpv = "(" + _cp + "-" + _vr + ")"
_pv = (
    "(?P<pn>"
    + _pkg
    + "(?P<pn_inval>-"
    + _vr
    + ")?)"
    + "-(?P<ver>"
    + _v
    + ")(-r(?P<rev>"
    + _rev
    + "))?"
)

_pv_re = None


def _get_pv_re():
    global _pv_re
    if _pv_re is not None:
        return _pv_re

    _pv_re = re.compile(r"^" + _pv + r"$", re.VERBOSE | re.UNICODE)

    return _pv_re


def _pkgsplit(mypkg: str):
    """
    @param mypkg: pv
    @return:
    1. None if input is invalid.
    2. (pn, ver, rev) if input is pv
    """
    m = _get_pv_re().match(mypkg)
    if m is None:
        return None

    if m.group("pn_inval") is not None:
        # package name appears to have a version-like suffix
        return None

    rev = m.group("rev")
    if rev is None:
        rev = "0"
    rev = "r" + rev

    return (m.group("pn"), m.group("ver"), rev)


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
            # If atom don't start with "=" we assume there is no version
            if '=' in atom:
                self.package, self.version, rev = _pkgsplit(self.package)
                self.version = f"{self.version}-{rev}"
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
