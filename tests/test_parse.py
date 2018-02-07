import unittest
import ebuildtester.parse


class TestParse(unittest.TestCase):

    def setUp(self):
        self.args = ["--portage-dir", "."]

    def test_atom(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--atom", "dev-util/ebuildtester"])
        self.assertTrue("dev-util/ebuildtester" in options.atom)
