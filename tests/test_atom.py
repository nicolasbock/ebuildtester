import unittest
from ebuildtester.atom import Atom


class TestAtom(unittest.TestCase):

    def test_equals(self):
        atom = Atom("ATOM")
