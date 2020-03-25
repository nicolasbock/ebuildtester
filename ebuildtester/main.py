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
