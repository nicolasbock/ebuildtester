import argparse


def parse_commandline(args):
    """Parse the command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--atom",
        help="The package atom(s) to install",
        nargs="+",
        action="append")
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
        default=False,
        action="store_true")
    parser.add_argument(
        "--threads",
        metavar="N",
        help="Use N threads to build packages",
        default=1,
        type=int)
    parser.add_argument(
        "--use",
        help="The use flags for the atom",
        default=[],
        nargs="+")
    parser.add_argument(
        "--unmask",
        metavar="ATOM",
        help="Unmask atom (can be used multiple times)",
        default=[],
        action="append")
    parser.add_argument(
        "--gcc-version",
        metavar="VER",
        help="Use gcc version VER")
    parser.add_argument(
        "--with-X",
        help="Install VNC server to test graphical applications",
        default=False,
        action="store_true")
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

    if options.with_X:
        options.atom += ["net-misc/tigervnc", "x11-wm/icewm"]

    return options
