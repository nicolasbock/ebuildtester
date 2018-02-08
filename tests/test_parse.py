import unittest
import ebuildtester.parse


class TestParse(unittest.TestCase):

    def setUp(self):
        self.args = ["--portage-dir", ".", "--manual"]

    def test_portage_dir(self):
        import sys
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            self.assertRaises(Exception, ebuildtester.parse.parse_commandline(
                ["--portage-dir", "."]))
        else:
            with self.assertRaises(Exception):
                options = ebuildtester.parse.parse_commandline(
                    ["--portage-dir", "."])
        options = ebuildtester.parse.parse_commandline(self.args)
        self.assertEqual(".", options.portage_dir)

    def test_atom(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--atom", "ATOM"])
        self.assertTrue("ATOM" in options.atom)

    def test_manual(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual"])
        self.assertTrue(options.manual)

    def test_overlay_dir(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--overlay-dir", "."])
        self.assertTrue("." in options.overlay_dir)

    def test_update(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--update"])
        self.assertTrue(options.update)

    def test_threads(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--threads", "4"])
        self.assertEqual(options.threads, 4)

    def test_use(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--use", "a", "b", "c"])
        self.assertTrue("a" in options.use)
        self.assertTrue("b" in options.use)
        self.assertTrue("c" in options.use)

    def test_unmask(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--unmask", "ATOM"])
        self.assertTrue("ATOM" in options.unmask)

    def test_gcc_version(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--gcc-version", "VER"])
        self.assertEqual("VER", options.gcc_version)

    def test_with_X(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--with-X"])
        self.assertTrue(options.with_X)
        self.assertTrue("net-misc/tigervnc" in options.atom)
        self.assertTrue("x11-wm/icewm" in options.atom)
