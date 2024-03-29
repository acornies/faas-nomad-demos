# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/bionic64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 4646, host: 4646
  config.vm.network "forwarded_port", guest: 8500, host: 8500
  config.vm.network "forwarded_port", guest: 8200, host: 8200
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 9090, host: 9090
  config.vm.network "forwarded_port", guest: 3000, host: 3000

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.synced_folder "./contrib", "/vagrant/contrib"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb, override|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = false
  
    # Customize the amount of memory on the VM:
    vb.memory = "4096"
    vb.cpus = 2
    override.vm.provision :salt do |salt|
      salt.minion_config = "contrib/salt/etc/minion_virtualbox.yaml"
      salt.verbose = true
      salt.run_highstate = true
      salt.salt_call_args = ["--id=vagrant"]
    end
    # pre-populate Vault
    override.vm.provision "shell", path: "contrib/scripts/vault_populate.sh"
  end

  config.vm.provider "vmware_fusion" do |vmf, override|
    override.vm.box = "generic/ubuntu1804"
    vmf.gui = false
    vmf.memory = "4096"
    vmf.cpus = 2
    override.vm.provision :salt do |salt|
      salt.minion_config = "contrib/salt/etc/minion_vmware.yaml"
      salt.verbose = true
      salt.run_highstate = true
      salt.salt_call_args = ["--id=vagrant"]
    end
    # pre-populate Vault
    override.vm.provision "shell", path: "contrib/scripts/vault_populate.sh"
  end

  config.vm.provision :docker do |d|
    d.run 'dev-vault', image: 'vault:latest',
      args: '-p 8200:8200 -e "VAULT_DEV_ROOT_TOKEN_ID=vagrant" -v /vagrant:/vagrant'
    d.run 'dev-consul', image: 'consul:latest',
      cmd: 'consul agent -dev -ui -client 0.0.0.0',
      args: '-p 8500:8500 --network host'
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
  config.vm.provision :salt do |salt|
    salt.install_type = "git"
    salt.install_args = "v2019.2.0"
  end
  config.vm.provision "shell", path: "contrib/scripts/formulas.py"
end
