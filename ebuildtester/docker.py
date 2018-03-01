import ebuildtester.options as options
from ebuildtester.utils import massage_string


class Docker:

    def __init__(self, local_portage, overlay_dirs):
        """Create a new container."""

        import os.path

        docker_image = "gentoo/stage3-amd64"
        overlay_dirs = list(set(overlay_dirs))
        overlay_mountpoints = [os.path.join("/var/lib/overlays", p)
                               for p in map(os.path.basename, overlay_dirs)]

        self._setup_container(docker_image)
        self._create_container(docker_image, local_portage,
                               zip(overlay_dirs, overlay_mountpoints))
        self._start_container()
        self._set_profile()
        self._tweak_settings()
        self._enable_overlays(map(os.path.basename, overlay_dirs))
        self._enable_test()
        self._unmask_atom()
        self._unmask()
        self._update()
        self._install_basics()
        self._set_gcc()
        self._print_summary()

    def execute(self, cmd):
        """Execute command in container.

        cmd is a string which is executed within a bash shell.
        """

        import os
        import subprocess
        import sys

        options.log.info("%s %s" % (self.cid[:6], cmd))
        docker_cmd = ["docker", "exec", "--interactive"]
        docker_cmd += [self.cid, "/bin/bash"]
        docker = subprocess.Popen(docker_cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE,
                                  universal_newlines=True)
        docker.stdin.write(cmd + "\n")
        docker.stdin.close()
        stdout_reader = os.fork()
        if stdout_reader == 0:
            self._reader(docker, docker.stdout, "stdout")
            sys.exit(0)
        stderr_reader = os.fork()
        if stderr_reader == 0:
            self._reader(docker, docker.stderr, "stderr")
            sys.exit(0)
        os.waitid(os.P_PID, stdout_reader, os.WEXITED)
        os.waitid(os.P_PID, stderr_reader, os.WEXITED)
        docker.wait()
        if docker.returncode != 0:
            options.log.error("running in container %s" % (str(self.cid)))
            raise Exception("failed command \"%s\"" % (cmd))

    def shell(self):
        """Run an interactive shell in container."""

        import subprocess

        options.log.info("running interactive shell in container")
        docker = subprocess.Popen(["docker", "exec", "--tty", "--interactive",
                                   self.cid, "/bin/bash"])
        docker.wait()

    def _reader(self, proc, stream, name):
        """Read from a subprocess stream."""

        while True:
            out = stream.readline()
            if out == "" and proc.poll() is not None:
                break
            options.log.info("%s (%s): %s" %
                             (self.cid[:6], name, out.rstrip()))
            options.log_ch.flush()

    def _setup_container(self, docker_image):
        """Setup the container."""

        import subprocess

        docker_args = ["docker", "pull", docker_image]
        docker = subprocess.Popen(docker_args)
        docker.wait()

    def _create_container(self, docker_image, local_portage, overlays):
        """Create new container."""

        import subprocess

        docker_args = [
            "docker", "create",
            "--tty",
            "--cap-add", "SYS_ADMIN",
            "--device", "/dev/fuse",
            "--storage-opt", "size=50G",
            "--workdir", "/root",
            "--volume", "%s:/usr/portage" % local_portage,
            "--volume", "/usr/portage/distfiles:/usr/portage/distfiles"]
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

        import subprocess

        docker_args = ["docker", "start", "%s" % self.cid]
        docker = subprocess.Popen(docker_args, stdout=subprocess.PIPE)
        docker.wait()
        if docker.returncode != 0:
            raise Exception("failure creating docker container")

    def _set_profile(self):
        """Set the Gentoo profile."""

        options.log.info("setting Gentoo profile to %s" %
                         options.options.profile)
        self.execute("eselect profile set %s" % options.options.profile)

    def _tweak_settings(self):
        """Tweak portage settings."""

        options.log.info("tweaking portage settings")

        # Disable the usersandbox feature, it's not working well inside a
        # docker container.
        self.execute("echo FEATURES=\\\"-sandbox -usersandbox\\\" " +
                     ">> /etc/portage/make.conf")
        self.execute(("echo MAKEOPTS=\\\"-j%d\\\" " % (options.options.threads)) +
                     ">> /etc/portage/make.conf")

    def _enable_overlays(self, overlays):
        """Enable overlays."""

        self.execute("mkdir -p /etc/portage/repos.conf")
        for o in overlays:
            self.execute("echo \"[%s]\" >> "
                         "/etc/portage/repos.conf/overlays.conf" % o)
            self.execute("echo \"location = /var/lib/overlays/%s\" >> "
                         "/etc/portage/repos.conf/overlays.conf" % o)
            self.execute("echo \"master = gentoo\" >> "
                         "/etc/portage/repos.conf/overlays.conf")

    def _enable_test(self):
        """Enable test FEATURES for ATOM."""

        if options.options.atom is not None:
            options.log.info("enabling test feature for %s" %
                             options.options.atom)
            self.execute("mkdir -p /etc/portage/env")
            for a in options.options.atom:
                self.execute(
                    "echo \"%s tester.conf\" >> /etc/portage/package.env" % a)
            self.execute(
                "echo \"FEATURES=\\\"test splitdebug\\\"\" > /etc/portage/env/tester.conf")
        else:
            options.log.info("enabling tests skipped, no atoms specified")

    def _unmask_atom(self):
        """Unmask the atom to install."""

        if options.options.atom is not None:
            options.log.info("unmasking %s" % options.options.atom)
            for a in options.options.atom:
                self.execute(
                    "echo \"" + str(a) + "\" ~amd64 >> " +
                    "/etc/portage/package.accept_keywords")
            if len(options.options.use) > 0:
                for a in options.options.atom:
                    self.execute(
                        "echo %s %s >> /etc/portage/package.use/testbuild" %
                        (str(a), " ".join(options.options.use)))
        else:
            options.log.info("no atoms to unmask")

    def _unmask(self):
        """Unmask other atoms."""

        options.log.info("unmasking additional atoms")
        for a in options.options.unmask:
            options.log.info("  unmasking %s" % a)
            self.execute(
                "echo \"%s\" ~amd64 >> /etc/portage/package.accept_keywords" %
                a)

    def _update(self):
        """Update container."""

        if not options.options.update:
            options.log.info("skipping update")
        else:
            options.log.info("updating container")
            update_options = ["--verbose", "--update",
                              "--deep", "--newuse", "--changed-deps"]
            self.execute("emerge " + " ".join(update_options) + " @world")

    def _install_basics(self):
        """Install some basic packages."""

        options.log.info("installing basic packages: %s" %
                         options.base_packages)
        self.execute("emerge --verbose %s" %
                     " ".join(map(str, options.base_packages)))

    def _set_gcc(self):
        """Set gcc in the container."""

        import re

        options.log.info("setting gcc")
        if options.options.gcc_version:
            self.execute(
                ("echo =sys-devel/gcc-%s ** >> " % options.options.gcc_version) +
                "/etc/portage/package.accept_keywords")
            self.execute("emerge --verbose sys-devel/gcc")
            gcc = re.sub("-r[0-9]+$", "", options.options.gcc_version)
            self.execute("gcc-config $(gcc-config --list-profiles | " +
                         ("grep %s | " % gcc) +
                         "sed -e 's:^.*\[\([0-9]\+\)\].*:\\1:')")
            self.execute("emerge --verbose --oneshot sys-devel/libtool")

    def _print_summary(self):
        """Print summary."""

        options.log.info("summary")
        self.execute("if [[ -f /etc/portage/accept_keywords ]]; then " +
                     "cat /etc/portage/package.accept_keywords; fi")
        self.execute("if [[ -f /etc/portage/package.use/testbuild ]]; then " +
                     "cat /etc/portage/package.use/testbuild; fi")
        self.execute("emerge --info")
        self.execute("qlop --list")
