from ebuildtester.atom import Atom
import ebuildtester.parse
import unittest


class TestParse(unittest.TestCase):

    def setUp(self):
        self.args = ["--portage-dir", "~/gentoo"]

    def test_atom(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--atom", "=SECTION/ATOM-1.0.0"], {})
        self.assertTrue(Atom("=SECTION/ATOM-1.0.0") in options.atom)

    def test_binhost(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--binhost", "http://localhost:8080"], {})
        self.assertIn("http://localhost:8080", options.binhost)

    def test_live_ebuild(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--live-ebuild"], {})
        self.assertTrue(options.live_ebuild)

    def test_manual(self):
        options = ebuildtester.parse.parse_commandline(self.args + ["--manual"], {})
        self.assertTrue(options.manual)

    def test_portage_dir(self):
        import sys
        if sys.version_info[0] == 2 and sys.version_info[1] == 6:
            self.assertRaises(Exception, ebuildtester.parse.parse_commandline({}))
        else:
            with self.assertRaises(Exception):
                options = ebuildtester.parse.parse_commandline({})
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual"], {})
        self.assertEqual("~/gentoo", options.portage_dir)

    def test_overlay_dir(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--overlay-dir", "."], {})
        self.assertTrue("." in options.overlay_dir)
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--overlay-dir", "."], {"overlay_dir": ["/overlay/path"]})
        self.assertTrue("/overlay/path" in options.overlay_dir)

    def test_update(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--update"], {})
        self.assertFalse(options.update)

    def test_threads(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--threads", "4"], {})
        self.assertEqual(options.threads, 4)

    def test_use(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--use", "a", "b", "c"], {})
        self.assertTrue("a" in options.use)
        self.assertTrue("b" in options.use)
        self.assertTrue("c" in options.use)

    def test_unmask(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--unmask", "ATOM"], {})
        self.assertTrue("ATOM" in options.unmask)

    def test_gcc_version(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--gcc-version", "VER"], {})
        self.assertEqual("VER", options.gcc_version)

    def test_python_single_target(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--python-single-target", "-* python3_8"], {})
        self.assertEqual("-* python3_8", options.python_single_target)

    def test_python_targets(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual", "--python-targets", "python3_8"], {})
        self.assertEqual("python3_8", options.python_targets)

    def test_docker_image(self):
        options = ebuildtester.parse.parse_commandline(
            self.args + ["--manual"], {})
        self.assertEqual(options.docker_image, "gentoo/stage3")
