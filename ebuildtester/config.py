import tomli
from appdirs import user_config_dir


class ConfigFile:
    def __init__(self):
        appname = "ebuildtester"
        cfg_dir = user_config_dir(appname)
        cfg_file = "{}/config.toml".format(cfg_dir)

        self._d = {}
        self._cfg = None
        try:
            with open(cfg_file, mode="rb") as fp:
                self._cfg = tomli.load(fp)
        except FileNotFoundError:
            pass

    def _add(self, e, t=None):
        if e in self._cfg:
            if t and type(self._cfg[e]) is not t:
                raise Exception("{} is not of type {}".format(e, t))
            self._d[e] = self._cfg[e]

    def get_cfg(self):
        if self._cfg is None:
            return {}

        self._add("batch")
        self._add("docker_command")
        self._add("features", list)
        self._add("install_basic_packages")
        self._add("manual")
        self._add("overlay_dir", list)
        self._add("portage_dir")
        self._add("pull")
        self._add("rm")
        self._add("unstable")
        self._add("update")

        return self._d
