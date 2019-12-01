from ebuildtester.atom import Atom
from ebuildtester.docker import Docker, ExecuteFailure
from ebuildtester.parse import parse_commandline
import ebuildtester.options as options
import logging
import os.path
import sys


def main():
    """The main function."""

    options.init()
    options.log.setLevel(logging.DEBUG)
    options.options = parse_commandline(sys.argv[1:])

    if not options.options.manual and options.options.atom is None:
        raise Exception("either specify an atom or use --manual")

    if options.options.shell_env is not None:
        for e in options.options.shell_env:
            options.sh_env.extend(list(set(e)))

    if options.options.atom:
        temp = []
        for a in options.options.atom:
            temp += a
        options.options.atom = temp
    else:
        options.options.atom = []

    if options.options.with_vnc:
        options.options.atom += ["net-misc/tigervnc", "x11-wm/icewm"]

    options.options.atom = list(map(Atom, options.options.atom))

    if options.options.ccache_dir is not None:
        options.base_packages.extend(list(map(Atom, ["dev-util/ccache"])))

    options.log.info("creating container")
    container = Docker(
        os.path.abspath(os.path.expanduser(options.options.portage_dir)),
        [os.path.abspath(p) for p in options.options.overlay_dir])

    options.log.info("created container " + container.cid)
    if options.options.manual:
        container.shell()
    else:
        container.execute("echo emerge --ask --autounmask-write=y --verbose " +
                          " ".join(map(str, options.options.atom)) +
                          " >> ~/.bash_history")

        for i in range(5):
            options.log.info("emerge attempt %d (of %d)" % (i + 1, 5))
            try:
                container.execute("emerge --autounmask-write=y --verbose " +
                                  " ".join(map(str, options.options.atom)))
            except ExecuteFailure:
                options.log.warn(
                    "command failed, updating configuration files")
                container.execute("etc-update --verbose --automode -5")
            else:
                break
        options.log.info("opening interactive shell")
        container.shell()

    container.cleanup()
