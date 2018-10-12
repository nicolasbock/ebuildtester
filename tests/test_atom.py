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

    def test_atomName(self):
        self.assertEqual(Atom("CATEGORY/PACKAGE").atomName(), "PACKAGE")
        self.assertEqual(Atom("=CATEGORY/PACKAGE-1.0.0").atomName(), "PACKAGE")
        self.assertEqual(Atom("CATEGORY/PACKAGE-1.0.0").atomName(), "PACKAGE")
        self.assertEqual(Atom("=CATEGORY/PACKAGE-DEP-1.0b-r1").atomName(),
                         "PACKAGE-DEP")

    def test_atomCategory(self):
        self.assertEqual(Atom("CATEGORY/PACKAGE").atomCategory(), "CATEGORY")
        self.assertEqual(Atom("=CATEGORY/PACKAGE-1.0.0").atomCategory(),
                         "CATEGORY")

    def test_atomVersion(self):
        self.assertEqual(Atom("=CATEGORY/PACKAGE-1").atomVersion(), "1")
        self.assertEqual(Atom("=CATEGORY/PACKAGE-1.0").atomVersion(), "1.0")
        self.assertEqual(Atom("=CATEGORY/PACKAGE-1.0-r1").atomVersion(),
                         "1.0-r1")
        self.assertEqual(Atom("=CATEGORY/PACKAGE-DEP-1.0b-r1").atomVersion(),
                         "1.0b-r1")

    def test_atomRepo(self):
        self.assertEqual(Atom(
            "=CATEGORY/PACKAGE-1::REP-0").atomRepo(), "REP-0")
        self.assertEqual(Atom(
            "<=CATEGORY/PACKAGE-1.0.0::REPO-NAME").atomRepo(), "REPO-NAME")
        self.assertEqual(Atom(
            "CATEGORY/PACKAGE::REPO_NAME").atomRepo(), "REPO_NAME")

    def test_atomCatName(self):
        self.assertEqual(Atom("CATEGORY/PACKAGE").atomCatName(),
                         "CATEGORY/PACKAGE")
        self.assertEqual(Atom("=CATEGORY/PACKAGE-1.0").atomCatName(),
                         "CATEGORY/PACKAGE")

    def test_atomComplete(self):
        atom1 = Atom("=CATEGORY/PACKAGE-1.0.0::REPO")
        atom2 = Atom(atom1.atomComplete())
        self.assertEqual(atom1, atom2)

    def test_atom(self):
        atom1 = Atom("=CATEGORY/PACKAGE-DEP-1.0b-r1")
        self.assertEqual(atom1.atomCategory(), "CATEGORY")
        self.assertEqual(atom1.atomName(), "PACKAGE-DEP")
        self.assertEqual(atom1.atomCatName(), "CATEGORY/PACKAGE-DEP")
        self.assertEqual(atom1.atomVersion(), "1.0b-r1")
        self.assertEqual(atom1.atomComplete(), "=CATEGORY/PACKAGE-DEP-1.0b-r1")
