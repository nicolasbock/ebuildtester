"""Options and some initializations."""

import logging
import os

from ebuildtester.atom import Atom

base_packages = list(map(Atom, ["app-portage/gentoolkit",
                                "app-portage/flaggie"]))
OPTIONS = None
log = logging.getLogger("test-package")
_log_default_formatter = \
    logging.Formatter("%(asctime)s - %(message)s")
_log_debug_formatter = \
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
_log_ch = logging.StreamHandler()
_log_ch.setLevel(logging.INFO)
_log_ch.setFormatter(_log_default_formatter)
_log_fh = None
log.addHandler(_log_ch)
log.setLevel(logging.DEBUG)

_logdir = os.getenv('XDG_STATE_HOME', '/tmp')
_logfile = None
_log_filehandle = None


def set_logfile(logfile):
    """Add a logfile to logging."""

    global _log_fh

    _logfile = os.path.join(_logdir, logfile)
    _log_fh = logging.FileHandler(_logfile, "a")
    _log_fh.setLevel(logging.INFO)
    _log_fh.setFormatter(_log_default_formatter)
    log.addHandler(_log_fh)
    log.info("logging at %s", _logfile)


def set_debugLoglevel():
    """Set logging level."""
    _log_ch.setLevel(logging.DEBUG)
    _log_ch.setFormatter(_log_debug_formatter)
    _log_fh.setLevel(logging.DEBUG)
    _log_fh.setFormatter(_log_debug_formatter)
