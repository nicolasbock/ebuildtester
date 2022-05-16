"""Options and some initializations."""

from ebuildtester.atom import Atom
import logging
import os

base_packages = list(map(Atom, ["app-portage/gentoolkit",
                                "app-portage/flaggie"]))
options = None
log = logging.getLogger("test-package")
log_ch = logging.StreamHandler()
log_ch.setLevel(logging.INFO)
log_ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
log.addHandler(log_ch)
log.setLevel(logging.DEBUG)

logdir = os.getenv('XDG_STATE_HOME', '/tmp')
_logfile = None
_log_filehandle = None


def set_logfile(logfile):
    """Add a logfile to logging."""

    _logfile = os.path.join(logdir, logfile)
    _log_filehandle = logging.FileHandler(_logfile, "a")
    _log_filehandle.setLevel(logging.INFO)
    _log_filehandle.setFormatter(
        logging.Formatter("%(asctime)s - %(message)s"))
    log.addHandler(_log_filehandle)
    log.info("logging at %s", _logfile)
