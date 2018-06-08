from ebuildtester.atom import Atom
from pkg_resources import get_distribution
import argparse
import multiprocessing


def parse_commandline(args):
    """Parse the command line."""

    parser = argparse.ArgumentParser(
        description="A dockerized approach to test a Gentoo "
        "package within a clean stage3.")
    parser.add_argument(
        "--version",
        action="version",
        version="v" + get_distribution("ebuildtester").version)
    parser.add_argument(
        "--atom",
        help="The package atom(s) to install",
        nargs="+",
        action="append")
    parser.add_argument(
        "--live-ebuild",
        help="Unmask the live ebuild of the atom",
        action="store_true")
    parser.add_argument(
        "--manual",
        help="Install package manually",
        default=False,
        action="store_true")
    parser.add_argument(
        "--portage-dir",
        help="The local portage directory",
        required=True)
    parser.add_argument(
        "--overlay-dir",
        help="Add overlay dir (can be used multiple times)",
        action="append",
        default=[])
    parser.add_argument(
        "--update",
        help="Update container before installing atom",
        choices=["yes", "true", "no", "false"],
        default="false")
    parser.add_argument(
        "--threads",
        metavar="N",
        help="Use N (default %(default)s) threads to build packages",
        default=multiprocessing.cpu_count(),
        type=int)
    parser.add_argument(
        "--use",
        help="The use flags for the atom",
        default=[],
        nargs="+")
    parser.add_argument(
        "--global-use",
        help="Set global USE flag",
        default=[],
        nargs="+")
    parser.add_argument(
        "--unmask",
        metavar="ATOM",
        help="Unmask atom (can be used multiple times)",
        default=[],
        action="append")
    parser.add_argument(
        "--unstable",
        help="Globally 'unstable' system, i.e. ~amd64",
        action="store_true")
    parser.add_argument(
        "--gcc-version",
        metavar="VER",
        help="Use gcc version VER")
    parser.add_argument(
        "--rm",
        help="Remove container after session is done",
        action="store_true")
    parser.add_argument(
        "--with-X",
        help="Globally enable the X USE flag",
        action="store_true")
    parser.add_argument(
        "--with-vnc",
        help="Install VNC server to test graphical applications",
        action="store_true")
    parser.add_argument(
        "--profile",
        help="The profile to use",
        choices=["default/linux/amd64/17.0",
                 "default/linux/amd64/17.0/systemd"],
        default="default/linux/amd64/17.0")

    options = parser.parse_args(args)

    if not options.manual and options.atom is None:
        raise Exception("either specify an atom or use --manual")

    if options.atom:
        temp = []
        for a in options.atom:
            temp += a
        options.atom = temp
    else:
        options.atom = []

    if options.with_vnc:
        options.atom += ["net-misc/tigervnc", "x11-wm/icewm"]

    options.atom = list(map(Atom, options.atom))

    if options.update in ["yes", "true"]:
        options.update = True
    else:
        options.update = False

    return options
