import logging
from ebuildtester.docker import Docker
from ebuildtester.parse import parse_commandline
import ebuildtester.options as options
import os.path
import sys


def main():
    """The main function."""

    options.init()

    options.log.setLevel(logging.DEBUG)

    options.options = parse_commandline(sys.argv[1:])

    options.log.info("creating container")
    container = Docker(
        os.path.abspath(os.path.expanduser(options.options.portage_dir)),
        [os.path.abspath(p) for p in options.options.overlay_dir])

    options.log.info("created container " + container.cid)
    if options.options.manual:
        container.shell()
    else:
        container.execute("echo emerge --ask --autounmask-write=n --verbose " +
                          " ".join(options.options.atom) +
                          " >> ~/.bash_history")
        try:
            container.execute("emerge --autounmask-write=n --verbose " +
                              " ".join(options.options.atom))
        except Exception:
            options.log.warn("ignoring failure of command")
        container.execute("etc-update --automode -5")
        try:
            container.execute("emerge --verbose " +
                              " ".join(options.options.atom))
        except Exception:
            options.log.warn("ignoring failure of command")
        container.shell()
