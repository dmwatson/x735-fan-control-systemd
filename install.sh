#!/bin/bash
# Copy the service file
sudo cp pwm_fan_control.service /etc/systemd/system/pwm_fan_control.service
sudo chown root:root /etc/systemd/system/pwm_fan_control.service
sudo chmod 644 /etc/systemd/system/pwm_fan_control.service

# Install the script
sudo mkdir /usr/local/lib/pwm_fan_control
sudo cp pwm_fan_control.py /usr/local/lib/pwm_fan_control/pwm_fan_control.py
sudo chown root:root /usr/local/lib/pwm_fan_control/pwm_fan_control.py
sudo chmod 644 /usr/local/lib/pwm_fan_control/pwm_fan_control.py

# Create the user account
sudo useradd -r -s /bin/false pwm_fan_control

# Reload the systemd configuration
sudo systemctl daemon-Reload
sudo systemctl enable pwm_fan_control
sudo systemctl restart pwm_fan_control

echo "X735 V2.5 PWM Fan Control Service installed!"