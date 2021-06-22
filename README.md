# X735 V2.5 Systemd PWM Fan Control

The [Geekworm X735 V2.5 power management board](https://wiki.geekworm.com/X735) for the Raspberry Pi is a decent piece of hardware. However, the script from the manufacturer to control the cooling fan via PWM works with only a handful of Linux distros. Running Ubuntu Server for Raspi, for example, results in failures and headaches.

I have modified the script to work as a systemd service, and included a service file and installer. The script depends on the pigpio library and pigpiod daemon, which also doesn't seem to come with Ubuntu Server for Raspberry Pi LTS (at least as of this writing).

To install pigpiod, you can download it from [here](http://abyz.me.uk/rpi/pigpio/download.html). Or, as an alternative, you can run the install_pigpio.sh script from the repository here which will download, compile, and install it for you.

## Installing the Script

To install the script, run the install.sh script.
