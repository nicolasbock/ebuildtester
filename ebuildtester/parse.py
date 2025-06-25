"""Parse command line options."""

import os
import argparse
import multiprocessing
from importlib.metadata import version

from ebuildtester.atom import Atom


def parse_commandline(args, d):
    """Parse the command line."""

    parser = argparse.ArgumentParser(
        description="A dockerized approach to test a Gentoo "
        "package within a clean stage3.")
    parser.add_argument(
        "--version",
        action="version",
        version="v" + version("ebuildtester"))
    parser.add_argument(
        "--atom",
        help="The package atom(s) to install",
        nargs="+",
        action="append")
    parser.add_argument(
        "--binhost",
        help="Binhost URI")
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
        required="portage_dir" not in d)
    parser.add_argument(
        "--overlay-dir",
        help="Add overlay dir (can be used multiple times)",
        action="append",
        default=[])
    parser.add_argument(
        "--update",
        help="Update container before installing atom",
        action="store_true")
    parser.add_argument(
        "--install-basic-packages",
        help="Install basic packages after container starts",
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
        "--python-single-target",
        metavar="PYTHON_SINGLE_TARGET",
        help="Specify a PYTHON_SINGLE_TARGET")
    parser.add_argument(
        "--python-targets",
        metavar="PYTHON_TARGETS",
        help="Specify a PYTHON_TARGETS")
    parser.add_argument(
        "--rm",
        help="Remove container after session is done",
        action="store_true")
    parser.add_argument(
        "--storage-opt",
        help="Storage driver options for all volumes (same as Docker param)",
        nargs="+",
        action="append")
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
        help="The profile to use (default = %(default)s)",
        default="default/linux/amd64/23.0")
    parser.add_argument(
        '--features',
        help="Set FEATURES, see https://wiki.gentoo.org/wiki/FEATURES "
             "(default = %(default)s)",
        default=["-sandbox", "-usersandbox", "userfetch"],
        nargs="+",
        action="append")
    parser.add_argument(
        "--docker-image",
        help="Specify the docker image to use (default = %(default)s)",
        default="gentoo/stage3")
    parser.add_argument(
        "--docker-command",
        help="Specify the docker command")
    parser.add_argument(
        "--pull",
        help="Download latest docker image",
        action="store_true")
    parser.add_argument(
        "--show-options",
        help="Show currently selected options and defaults",
        action="store_true")
    parser.add_argument(
        "--ccache",
        metavar="CCACHE_DIR",
        help="Path to mount that contains ccache cache")
    parser.add_argument(
        '--batch',
        help='Do not drop into interactive shell',
        action='store_true')
    parser.add_argument(
        '--debug',
        help='Add some debugging output',
        action='store_true')
    parser.set_defaults(**d)

    if '--complete' in args:
        print('Suggesting')
        args.pop(args.index('--complete'))
        print(f'args = {",".join(args)}')

    options = parser.parse_args(args)

    if not options.manual and options.atom is None:
        raise Exception("either specify an atom or use --manual")

    if options.atom:
        temp = []
        for atom in options.atom:
            temp += atom
        options.atom = temp
    else:
        options.atom = []

    temp = []
    for feature in options.features:
        if type(feature) is list:
            temp += feature
        else:
            temp.append(feature)
    options.features = temp

    if options.binhost:
        options.features.append("getbinpkg")

    if options.ccache:
        options.features.append("ccache")

    options.atom = list(map(Atom, options.atom))

    if options.update in ["yes", "true"]:
        options.update = True
    else:
        options.update = False

    if not options.docker_command:
        options.docker_command = os.getenv('DOCKER_COMMAND', default='docker')

    # Convert docker command into list so that `subprocess` can run the command
    # and add command line options if they are present.
    options.docker_command = options.docker_command.split()

    if options.show_options:
        print(options)

    return options
