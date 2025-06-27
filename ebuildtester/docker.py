"""The Docker backend."""

import os
import re
import sys
import subprocess

import ebuildtester.options as options
from ebuildtester.utils import massage_string


class ExecuteFailure(Exception):
    """Failure to execute command."""
    pass


class Docker:
    """The Docker class."""
    def __init__(self, local_portage, overlay_dirs):
        """Create a new container."""

        docker_image = options.OPTIONS.docker_image
        repo_names = self._get_repo_names(overlay_dirs)
        overlay_mountpoints = [os.path.join("/var/lib/overlays", r)
                               for r in repo_names]

        self._setup_container(docker_image)
        self._create_container(docker_image, local_portage,
                               zip(overlay_dirs, overlay_mountpoints))
        self._start_container()
        self._set_profile()
        self._enable_global_use()
        self._tweak_settings()
        self._enable_overlays(repo_names)
        self._enable_test()
        self._unmask_atom()
        self._unmask()
        self._update()
        self._install_basics()
        self._set_gcc()
        self._print_summary()

    def execute(self, cmd):
        """Execute command in container.

        cmd is a list of strings or a simple string with a command that is
        executed within a bash shell.
        """

        if isinstance(cmd, list):
            cmd_string = ' '.join(cmd)
        else:
            cmd_string = cmd
        options.log.info("%s %s", self.cid[:6], cmd)
        docker_cmd = options.OPTIONS.docker_command + ["exec", "--interactive"]
        docker_cmd += [self.cid, "/bin/bash"]
        docker = subprocess.Popen(docker_cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE,
                                  universal_newlines=True)
        docker.stdin.write(cmd_string + "\n")
        docker.stdin.close()

        stdout_reader = os.fork()
        if stdout_reader == 0:
            try:
                self._reader(docker, docker.stdout, "stdout")
            except KeyboardInterrupt:
                pass
            sys.exit(0)

        stderr_reader = os.fork()
        if stderr_reader == 0:
            try:
                self._reader(docker, docker.stderr, "stderr")
            except KeyboardInterrupt:
                pass
            sys.exit(0)

        try:
            os.waitid(os.P_PID, stdout_reader, os.WEXITED)
            os.waitid(os.P_PID, stderr_reader, os.WEXITED)
            docker.wait()
        except KeyboardInterrupt:
            try:
                options.log.info("received keyboard interrupt")
                docker.terminate()
                self.shell()
                options.log.info("return from shell, initiating shutdown")
                self.cleanup()
                sys.exit(0)
            except OSError:
                pass
            docker.wait()

        if docker.returncode != 0:
            options.log.error("running in container %s" % (str(self.cid)))
            options.log.error("failed command \"%s\"" % (cmd))

    def shell(self):
        """Run an interactive shell in container."""

        options.log.info("running interactive shell in container")
        docker = subprocess.Popen(options.OPTIONS.docker_command
                                  + ["exec", "--tty", "--interactive",
                                     self.cid, "/bin/bash"])
        try:
            docker.wait()
        except KeyboardInterrupt:
            options.log.info("ignoring keyboard interrupt")

    def cleanup(self):
        """Clean up."""

        if options.OPTIONS.rm:
            self.remove()

    def remove(self):
        """Remove the docker container."""

        options.log.info("stopping container")
        docker = subprocess.Popen(options.OPTIONS.docker_command
                                  + ["kill", self.cid])
        docker.wait()
        options.log.info("deleting container")
        docker = subprocess.Popen(options.OPTIONS.docker_command
                                  + ["rm", self.cid])
        docker.wait()

    def _reader(self, proc, stream, name):
        """Read from a subprocess stream."""

        while True:
            out = stream.readline()
            if out == "" and proc.poll() is not None:
                break
            options.log.info("%s (%s): %s" %
                             (self.cid[:6], name, out.rstrip()))
            options._log_ch.flush()

    def _setup_container(self, docker_image):
        """Setup the container."""

        if options.OPTIONS.pull:
            docker_args = options.OPTIONS.docker_command \
                + ["pull", docker_image]
            docker = subprocess.Popen(docker_args)
            docker.wait()

    def _create_container(self, docker_image, local_portage, overlays):
        """Create new container."""

        distdir = "{}/distfiles".format(local_portage)
        os.makedirs(distdir, exist_ok=True)

        pkgdir = "{}/packages".format(local_portage)
        os.makedirs(pkgdir, exist_ok=True)

        docker_args = options.OPTIONS.docker_command \
            + ["create",
               "--tty",
               "--cap-add", "CAP_SYS_ADMIN",
               "--cap-add", "CAP_MKNOD",
               "--cap-add", "CAP_NET_ADMIN",
               # https://github.com/moby/moby/issues/16429
               "--security-opt", "apparmor:unconfined",
               "--device", "/dev/fuse",
               "--workdir", "/root",
               "--volume", "%s:/var/db/repos/gentoo" % local_portage,
               "--volume", "%s:/var/cache/distfiles" % distdir,
               "--volume", "%s:/var/cache/binpkgs" % pkgdir]

        if options.OPTIONS.storage_opt:
            for s in options.OPTIONS.storage_opt:
                docker_args += ["--storage-opt", "%s" % s]

        ccache = options.OPTIONS.ccache
        if ccache:
            docker_args += ["--volume=%s:/var/tmp/ccache" % ccache]

        for o in overlays:
            docker_args += ["--volume=%s:%s" % o]

        docker_args += [docker_image]
        options.log.info("creating docker container with: %s" %
                         " ".join(docker_args))
        docker = subprocess.Popen(docker_args, stdout=subprocess.PIPE)
        docker.wait()

        if docker.returncode != 0:
            raise Exception("failure creating docker container")

        lines = docker.stdout.readlines()
        if len(lines) > 1:
            raise Exception("more output than expected")
        self.cid = massage_string(lines[0]).strip()
        options.log.info("container id %s" % (self.cid))

    def _start_container(self):
        """Start the container."""

        docker_args = options.OPTIONS.docker_command \
            + ["start", "%s" % self.cid]
        docker = subprocess.Popen(docker_args, stdout=subprocess.PIPE)
        docker.wait()
        if docker.returncode != 0:
            raise Exception("failure creating docker container")

    def _set_profile(self):
        """Set the Gentoo profile."""

        options.log.info("setting Gentoo profile to %s" %
                         options.OPTIONS.profile)
        self.execute("eselect profile set %s" % options.OPTIONS.profile)

    def _tweak_settings(self):
        """Tweak portage settings."""

        options.log.info("tweaking portage settings")

        # Disable the usersandbox feature, it's not working well inside a
        # docker container.
        self.execute(
            f"echo FEATURES=\\\"{' '.join(options.OPTIONS.features)}\\\" "
            ">> /etc/portage/make.conf")

        self.execute(("echo MAKEOPTS=\\\"-j%d\\\" " %
                      (options.OPTIONS.threads)) +
                     ">> /etc/portage/make.conf")
        if options.OPTIONS.binhost:
            self.execute("getuto")
            self.execute("echo -e '[ebuildtester]\n"
                         "priority = 999\n"
                         "sync-uri = {}\n'"
                         ">> /etc/portage/binrepos.conf/ebuildtester.conf"
                         .format(options.OPTIONS.binhost))
        if options.OPTIONS.unstable:
            self.execute("echo ACCEPT_KEYWORDS=\\\"~amd64\\\" " +
                         ">> /etc/portage/make.conf")
        if options.OPTIONS.with_X:
            self.execute("emerge --verbose gentoolkit")
            self.execute("euse --enable X")
        if options.OPTIONS.python_single_target:
            self.execute(("echo */* PYTHON_SINGLE_TARGET: %s" %
                          (options.OPTIONS.python_single_target)) +
                         " >> /etc/portage/package.use/python")
        if options.OPTIONS.python_targets:
            self.execute(("echo */* PYTHON_TARGETS: %s" %
                          (options.OPTIONS.python_targets)) +
                         " >> /etc/portage/package.use/python")

        # Avoid wasting time generating the whole set
        self.execute('echo "C.UTF-8 UTF-8" > /etc/locale.gen')

    def _get_repo_names(self, overlay_dirs):
        """Get repo names from local overlay settings."""

        repo_names = []
        for o in overlay_dirs:
            with open(os.path.join(o, "profiles/repo_name"), "r") as f:
                for repo_name in f:
                    repo_names.append(repo_name.replace("\n", ""))

        return repo_names

    def _enable_overlays(self, repo_names):
        """Enable overlays."""

        for r in repo_names:
            self.execute(
                "mkdir -p /etc/portage/repos.conf && " +
                "echo -e \"[%s]\\n" % str(r) +
                "location = /var/lib/overlays/%s\\n" % str(r) +
                "master = gentoo\" >> /etc/portage/repos.conf/overlays.conf"
            )

    def _enable_test(self):
        """Enable test FEATURES for ATOM."""

        if options.OPTIONS.atom is not None:
            options.log.info("enabling test feature for %s" %
                             options.OPTIONS.atom)
            self.execute("mkdir -p /etc/portage/env")
            for a in options.OPTIONS.atom:
                self.execute(
                    "echo \"%s tester.conf\" >> /etc/portage/package.env" % a)
            self.execute(
                "echo \"FEATURES=\\\"test splitdebug\\\"\" " +
                "> /etc/portage/env/tester.conf")
        else:
            options.log.info("enabling tests skipped, no atoms specified")

    def _unmask_atom(self):
        """Unmask the atom to install."""

        if options.OPTIONS.atom is not None:
            options.log.info("unmasking %s" % options.OPTIONS.atom)
            for a in options.OPTIONS.atom:
                if options.OPTIONS.live_ebuild:
                    unmask_keyword = "**"
                else:
                    unmask_keyword = "~amd64"
                self.execute("mkdir -p /etc/portage/package.accept_keywords")
                self.execute(
                    "echo \"" + str(a) + "\" " + unmask_keyword + " >> " +
                    "/etc/portage/package.accept_keywords/testbuild")
            if len(options.OPTIONS.use) > 0:
                for a in options.OPTIONS.atom:
                    self.execute(
                        "echo %s %s >> /etc/portage/package.use/testbuild" %
                        (str(a), " ".join(options.OPTIONS.use)))
        else:
            options.log.info("no atoms to unmask")

    def _unmask(self):
        """Unmask other atoms."""

        options.log.info("unmasking additional atoms")
        for a in options.OPTIONS.unmask:
            options.log.info("  unmasking %s" % a)
            self.execute("mkdir -p /etc/portage/package.accept_keywords")
            self.execute(
                "echo \"%s\" ~amd64 >> "
                "/etc/portage/package.accept_keywords/testbuild" % a)

    def _update(self):
        """Update container."""

        if not options.OPTIONS.update:
            options.log.info("skipping update")
        else:
            options.log.info("updating container")
            update_options = ["--verbose", "--update",
                              "--deep", "--newuse", "--changed-deps"]
            self.execute("emerge " + " ".join(update_options) + " @world")

    def _install_basics(self):
        """Install some basic packages."""

        if options.OPTIONS.ccache:
            self.execute("emerge --verbose dev-util/ccache")

        if not options.OPTIONS.install_basic_packages:
            options.log.info("skipping basic packages")
        else:
            options.log.info("installing basic packages: %s" %
                             options.base_packages)
            self.execute("emerge --verbose %s" %
                         " ".join(map(str, options.base_packages)))

        if options.OPTIONS.with_vnc:
            t = ["net-misc/tigervnc", "x11-wm/icewm"]
            options.log.info("installing VNC packages: %s" % t)
            self.execute("emerge --verbose %s" % " ".join(map(str, t)))

    def _enable_global_use(self):
        """Enable global USE settings."""
        if not options.OPTIONS.global_use:
            options.log.info("no global USE flags given, skipping")
        else:
            options.log.info("setting global USE flags")
            self.execute("emerge --verbose gentoolkit")
            for u in options.OPTIONS.global_use:
                self.execute("euse --enable %s" % u)

    def _set_gcc(self):
        """Set gcc in the container."""

        options.log.info("setting gcc")
        if options.OPTIONS.gcc_version:
            self.execute("mkdir -p /etc/portage/package.accept_keywords")
            self.execute(
                ("echo =sys-devel/gcc-%s ** >> " %
                 options.OPTIONS.gcc_version) +
                "/etc/portage/package.accept_keywords/testbuild")
            self.execute("emerge --verbose sys-devel/gcc")
            gcc = re.sub("-r[0-9]+$", "", options.OPTIONS.gcc_version)
            self.execute("gcc-config $(gcc-config --list-profiles | " +
                         ("grep %s | " % gcc) +
                         "sed -e 's:^.*\\[\\([0-9]\\+\\)\\].*:\\1:')")
            self.execute("emerge --verbose --oneshot sys-devel/libtool")

    def _print_summary(self):
        """Print summary."""

        options.log.info("summary")
        self.execute(
            "if [[ -d /etc/portage/package.accept_keywords ]]; then " +
            "cat /etc/portage/package.accept_keywords/*; fi")
        self.execute("if [[ -f /etc/portage/package.use/testbuild ]]; then " +
                     "cat /etc/portage/package.use/testbuild; fi")
        self.execute("emerge --info")
        self.execute("qlop")
