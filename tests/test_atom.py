import unittest
from ebuildtester.atom import Atom, AtomException


class TestAtom(unittest.TestCase):

    def test_equals(self):
        atom = Atom("=SECTION/PACKAGE-1.0.0")
        self.assertEqual(atom.__str__()[0], "=")
        self.assertEqual(atom.__str__(), "=SECTION/PACKAGE-1.0.0")

    def test_slash_1(self):
        with self.assertRaises(AtomException) as e:
            Atom("ATOM")

    def test_slash_2(self):
        atom = Atom("SECTION/PACKAGE")
        self.assertEqual(atom.section, "SECTION")
        self.assertEqual(atom.package, "PACKAGE")

    def test_version(self):
        self.assertEqual(Atom("SECTION/PACKAGE-1").package_version, "1")
        self.assertEqual(Atom("SECTION/PACKAGE-1.0").package_version, "1.0")
