import unittest
from ebuildtester.atom import Atom, AtomException


class TestAtom(unittest.TestCase):

    def test_equals(self):
        with self.assertRaises(AtomException) as e:
            Atom("ATOM")
