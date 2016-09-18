# terawatt
Project for what-the-data hackathlon.


## Installation

### Install Vagrant

Vagrant 1.8.5 is unable to create new Linux boxes due to Vagrant bug #7610. 
Use Vagrant 1.8.4 until version 1.8.6 is released.
https://releases.hashicorp.com/vagrant/1.8.4/

### Install Virtualbox

Install Virtualbox 5.0.24. The newer versions don't play nicely with Vagrant.
https://www.virtualbox.org/wiki/Download_Old_Builds_5_0

#### Change VBOX_INSTALL_PATH system path

The environment variable that was automatically created for me had a keyname of "VBOX_MSI_INSTALL_PATH." However, the "base.rb" file inside one of the many subfolders of the Vagrant directory looks for the environment variable keyname "VBOX_INSTALL_PATH." So all I did was right-click on "My Computer"-->Properties-->Advanced System Settings-->Environment Variables. Here I scrolled down to find "VBOX_MSI_INSTALL_PATH" and I changed it to "VBOX_INSTALL_PATH."

#### Setup virtual machine

Adapt VirtualBox virtual machine path to your liking by starting VirtualBox and going to settings.

### Shared folders on virtual machine

After having installed the virtual machine with ´vagrant up´
Enable CD-ROM by virtual box gui. 
Add guest additions from menu. 

  mount /dev/sr0 /mnt

run guest additions .sh file.

### Adapt gitconfig ###

Set github username and email in .gitconfig

### Push to github repository

```git add <file>```

```git commit -a -m "Blah Blah Blah"```

```git push origin master```
