# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network :private_network, ip: "10.0.10.100"
  config.vm.synced_folder ".", "/home/vagrant/d0018e"

  config.vm.network :forwarded_port, guest: 3306, host: 3406 # TODO?

  # provision
  config.vm.provision :shell, path: "provision/dev.sh", privileged: false
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.network :forwarded_port,
    guest: 22,
    host: 2322,
    host_ip: "127.0.0.1",
    id: "ssh",
    auto_correct: true

end
