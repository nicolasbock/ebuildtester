import unittest
from ebuildtester.atom import Atom, AtomException


class TestAtom(unittest.TestCase):

    def test_equals(self):
        atom = Atom("=CATEGORY/PACKAGE-1.0.0")
        self.assertEqual(atom.__str__()[0], "=")
        self.assertEqual(atom.__str__(), "=CATEGORY/PACKAGE-1.0.0")

    def test_slash_1(self):
        with self.assertRaises(AtomException) as e:
            Atom("ATOM")

    def test_slash_2(self):
        atom = Atom("CATEGORY/PACKAGE")
        self.assertEqual(atom.category, "CATEGORY")
        self.assertEqual(atom.package, "PACKAGE")

    def test_version(self):
        self.assertEqual(Atom("CATEGORY/PACKAGE-1").version, "1")
        self.assertEqual(Atom("CATEGORY/PACKAGE-1.0").version, "1.0")
        self.assertEqual(
            Atom("CATEGORY/PACKAGE-1.0-r1").version, "1.0-r1")

    def test_str(self):
        atom_1 = Atom("=CATEGORY/PACKAGE-1.0.0-r1")
        atom_2 = Atom(str(atom_1))
        self.assertEqual(atom_1, atom_2)
