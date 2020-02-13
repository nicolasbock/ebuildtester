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
        "--ccache-dir",
        help="Add ccache dir",
        action="append",
        default=[])
    parser.add_argument(
        "--update",
        help="Update container before installing atom",
        action="store_true")
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
        "--mask",
        metavar="ATOM",
        help="Mask atom (can be used multiple times)",
        default=[],
        action="append")
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
        "--pull",
        help="Download latest 'gentoo/stage3-amd64' docker image",
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
        choices=["default/linux/amd64/17.1",
                 "default/linux/amd64/17.1/systemd"],
        default="default/linux/amd64/17.1")
    parser.add_argument(
        "--shell-env",
        help="Set user shell env (Example: --shell-env \"EDITOR=/usr/bin/vi\")",
        default=[],
        nargs="+",
        action="append")

    options = parser.parse_args(args)

    return options
