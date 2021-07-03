#!/usr/bin/python
# Fan control daemon for the X735 V2.5 power management board
import pigpio
import time
import os
import sys
import logging
from configparser import ConfigParser
from systemd import daemon
from systemd.journal import JournalHandler

logger = None
journald_handler = None

poll_rate = 1
shutoff_temp = 30
thresholds = []

def init():
     global logger
     global journald_handler

     logger = logging.getLogger('pwm_fan_control')
     journald_handler = JournalHandler()

     logger.addHandler( journald_handler )
     logger.setLevel(logging.DEBUG)
# end init


def load_configuration() -> None:
    global poll_rate
    global shutoff_temp
    global thresholds
    global logger

    dname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dname)

    config = ConfigParser()
    config.read("pwm_fan_control.conf")
    poll_rate = config.getint('Config', 'poll_rate', fallback=1)
    logger.info("Polling rate set to {} seconds\n".format( poll_rate ) )
    # Anything below this temperature shuts the fan off
    shutoff_temp = config.getint('Config', 'shutoff_temp', fallback=30)
    logger.info("Shutoff temperature: {} C\n".format(shutoff_temp) )

    for i in range(1, 101):
        thresh_temp = config.getint(
            'Thresholds', "threshold_{}_temp".format(i), fallback=0)
        thresh_duty = config.getint(
            'Thresholds', "threshold_{}_duty".format(i), fallback=0)

        if thresh_temp > 0 and thresh_duty > 0:
            thresholds.append({'temp': thresh_temp, 'duty': thresh_duty})
            logger.info(
                "Temperature: {} C -- Duty {}%\n".format(thresh_temp, thresh_duty))

# end load_configuration

def run_daemon():
     global thresholds
     global poll_rate

     try:
          # PWM pin is 13
          pin = 13
          pwm = pigpio.pi()
          pwm.set_mode( pin, pigpio.OUTPUT )
          pwm.set_PWM_frequency( pin, 25000 )
          pwm.set_PWM_range( pin, 100 )

          logger.info( "X735 PWM Fan Control connected to RPi GPIO\n" )

          while True:
               # get CPU temp
               file = open("/sys/class/thermal/thermal_zone0/temp")
               temp = float(file.read()) / 1000.00
               temp = float("%.2f" % temp)
               file.close()

               # Set duty cycle based on temperature thresholds
               for thresh in thresholds:
                    if temp > thresh['temp']:
                         pwm.set_PWM_dutycycle(pin, thresh['duty'])

               if(temp < shutoff_temp):
                    pwm.set_PWM_dutycycle(pin, 0)

               # Sleep for the pollrate amount
               time.sleep(poll_rate)

     except KeyboardInterrupt:
          logger.info("X735: Shutdown signal received. Cleaning up GPIOs...\n")
          pwm.stop()
          # Give a clean exit signal
          logger.info("X735: Shutting down\n")
          sys.exit(0)
# end run_daemon()

if __name__ == '__main__':
     init()
     load_configuration()
     daemon.notify('READY=1')
     run_daemon()
