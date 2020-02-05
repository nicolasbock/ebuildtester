Vagrant.configure("2") do |config|
  config.vm.box = "generic/gentoo"

  config.vm.provision "shell", inline: <<-SHELL
    mkdir -p /etc/portage/sets
    echo "app-emulation/docker" > /etc/portage/sets/ebuildtester
    echo "sys-fs/fuse" >> /etc/portage/sets/ebuildtester
    emerge @ebuildtester

    /usr/share/docker/contrib/check-config.sh

    echo '{"storage-driver":"devicemapper"}' > /etc/docker/daemon.json
  SHELL

end
