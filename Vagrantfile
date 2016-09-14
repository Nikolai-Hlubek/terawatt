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
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/ubuntu-16.04"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 8888 on the guest machine.
  config.vm.network "forwarded_port", guest: 8888, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = true
  
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
    apt-get install -y ubuntu-desktop
    apt-get install -y build-essential python3 python3-dev python3-pip
	apt-get install -y vim
	
	# Jupyter with RISE, plotly and iplantuml
    pip3 install --upgrade pip
    pip3 install jupyter
    pip3 install RISE
    jupyter-nbextension install rise --py --sys-prefix
    jupyter-nbextension enable rise --py --sys-prefix
    pip3 install plotly
	pip3 install iplantuml
	pip3 install numpy
	apt-get install -y plantuml
	cp /usr/share/plantuml/plantuml.jar /usr/local/
	
	# German support
	locale-gen de_DE.UTF-8
	update-locale LANG=de_DE.UTF-8 LC_MESSAGES=POSIX
	sed -i 's/us/de/g' /etc/default/keyboard
	
	# Git
	apt-get install -y git

	mkdir -p what-the-data
	git clone https://github.com/nikolai-hlubek/terawatt /home/vagrant/what-the-data
  SHELL
 
  config.vm.provision "shell", 
    inline: "nohup jupyter-notebook --ip 0.0.0.0 --port 8888 --notebook-dir=/home/vagrant/what-the-data --no-browser &",
    privileged: false,
    run: "always"

end
