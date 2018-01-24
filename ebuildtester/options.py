import logging


def init():
    global basic_packages
    global log
    global log_ch
    global options

    basic_packages = ["app-portage/gentoolkit"]
    options = None
    log = logging.getLogger("test-package")
    log_ch = logging.StreamHandler()
    log_ch.setLevel(logging.INFO)
    log_ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    log.addHandler(log_ch)

    fh = logging.FileHandler("tester.log", "a")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    log.addHandler(fh)
