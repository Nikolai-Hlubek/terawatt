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

Add the following alias to the config file in .git/-directory:

  [alias]
    lg1 = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all
    lg = !"git lg1"

### Push to github repository

```git add <file>```

```git commit -a -m "Blah Blah Blah"```

```git push origin master```

## Good to know

You need 0.1 kWh for bringing 1l water from 15°C to 100°C (without boiling).

According to http://www.bmw.com/com/de/newvehicles/i/i3/2015/showroom/range_charging.html#comparison_calculator_charging_time it takes three hours at a maximum of 7.4kW to charge the i3 back to 80%. According to some articles, te charging process is artificially slowed down above 80% to save the battery.

See: https://de.wikipedia.org/wiki/Watt_Peak for definition of kWp.

## MQTT

MQTT (Mesage Queue Telemetry Transport) is a transport protocoll for unreliable networks.

A broker (Mosquitto, see https://mosquitto.org/) can be installed with:

  sudo apt-get install -y mosquitto

Once installed, the mosquitto service is automatically started.

The subfolder mqtt contains two examples of how a sensor (sensor.py) and and actor (actor.py) works. In the course of this project, we are focussing on the actor part. The sensor data should come from the different devices.

### Start the sensor

  python3 sensor.py

### Start the actor

  python3 actor.py

## Subscriptions

Subscriptions use a topic filter. Topic levels are separated by "/". There are two wildcards:

* #: This level and **all** below. If used, has to be the last character in a topic filter.
* +: This level with all direct children. Something like "first/+/temperature" is possible.

## Service levels

* 0: At most once
* 1: At least once
* 2: Exactly once

## Payloads

Although the mqtt specification is payload agnostic, the paho implementation for python insists on the following data types:

* string
* bytearray
* int
* float
* None

## Starting the data download

Start the programm staubsauger.py. It will read the config file staubsauger_config.txt every minute and updates the mqttt-clients.

The config file expects a name (will be he file name for the results), a topic, the host url of the broker and a port. Invalid configuration will be skipped.

The data is retrieved via mqqt and saved in the folder data with a file name corresponding to the given name in the config.

Data is appended to the file

### Test

1. Start the mqtt/sensor.py
2. Start the mqtt/staubsauger.py
3. Change the config file
4. Watch the changes
