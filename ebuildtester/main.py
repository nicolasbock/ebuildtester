"""The main function."""

import os.path
import sys

from ebuildtester.atom import Atom
from ebuildtester.config import ConfigFile
from ebuildtester.docker import Docker, ExecuteFailure
from ebuildtester.parse import parse_commandline
import ebuildtester.options as options


def main():
    """The main function."""

    cfg = ConfigFile()
    options.OPTIONS = parse_commandline(sys.argv[1:], cfg.get_cfg())
    if len(options.OPTIONS.atom) > 0:
        options.set_logfile('ebuildtester-'
                            + ':'.join([f'{atom.category}-{atom.package}'
                                        for atom in options.OPTIONS.atom])
                            + '.log')
    else:
        options.set_logfile('ebuildtester-manual.log')

    if options.OPTIONS.debug:
        options.set_debugLoglevel()

    options.log.info(
        "*** please note that all necessary licenses will be accepted ***")
    options.log.info("creating container")
    container = Docker(
        os.path.abspath(os.path.expanduser(options.OPTIONS.portage_dir)),
        [os.path.abspath(p) for p in options.OPTIONS.overlay_dir])

    options.log.info("created container %s", container.cid)
    if options.OPTIONS.manual:
        container.shell()
    else:
        emerge_command = [
            "emerge",
            "--verbose ",
            "--autounmask-write=y ",
            "--autounmask-license=y ",
            "--autounmask-continue=y "]

        atoms = [Atom(str(a)) for a in options.OPTIONS.atom]

        if options.OPTIONS.binhost:
            for a in atoms:
                p = "{}/{}".format(a.category, a.package)
                emerge_command.append("--usepkg-exclude={}".format(p))

        for a in atoms:
            emerge_command.append(str(a))
        container.execute(" ".join(["echo"] + emerge_command + ["--ask"]) +
                          " >> ~/.bash_history")

        for i in range(5):
            options.log.info("emerge attempt %d (of %d)", i + 1, 5)
            try:
                container.execute(emerge_command)
            except ExecuteFailure:
                options.log.warning(
                    "command failed, updating configuration files")
                container.execute("etc-update --verbose --automode -5")
            else:
                break
        if not options.OPTIONS.batch:
            options.log.info("opening interactive shell")
            container.shell()

    container.cleanup()
