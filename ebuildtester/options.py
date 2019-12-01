from ebuildtester.atom import Atom
import logging


def init():
    global base_packages
    global exec_env
    global sh_env
    global log
    global log_ch
    global options

    base_packages = list(map(Atom, ["app-portage/gentoolkit",
                                    "app-portage/flaggie",
                                    "dev-util/strace"]))

    sh_env = []

    # man make.conf
    exec_env = ["ACCEPT_KEYWORDS", "ACCEPT_LICENSE", "PORTDIR", "CCACHE_DIR", "PORTAGE_BINHOST"]
    exec_env += ["USE", "MAKEOPTS", "FEATURES", "PKGDIR", "DISTDIR", "EMERGE_DEFAULT_OPTS"]
    exec_env += ["CFLAGS", "CXXFLAGS", "LDFLAGS", "CPU_FLAGS_X86"]

    options = None
    log = logging.getLogger("test-package")
    log_ch = logging.StreamHandler()
    log_ch.setLevel(logging.INFO)
    log_ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    log.addHandler(log_ch)

    fh = logging.FileHandler("/tmp/ebuildtester.log", "w")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    log.addHandler(fh)
