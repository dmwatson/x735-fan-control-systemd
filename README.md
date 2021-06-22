# X735 V2.5 Systemd PWM Fan Control

The [X735 V2.5 power management board](https://wiki.geekworm.com/X735) for the Raspberry Pi is a nice piece of hardware. However, the script from the manufacturer to control the cooling fan via PWM is limited to only a handful of Linux distros. Running Ubuntu Server for Raspi, for example, results in failures and headaches.

I have modified the script to be systemd-friendly, and included a service file. The script depends on the pigpio library and pigpiod daemon, which also doesn't seem to come with Ubuntu Server for Raspberry Pi LTS (at least as of this writing).

To install pigpiod, you can download it from [here](http://abyz.me.uk/rpi/pigpio/download.html). It's only a couple of steps and installs painlessly.

## Installing the Script

To install the script, run the install.sh script.
