#!/usr/bin/python
# Fan control daemon for the X735 V2.5 power management board
import RPi.GPIO as GPIO
import pigpio
import time
from systemd import daemon, journal

if __name__ == '__main__':
     print('X735 PWM Fan Control Startup...')
     daemon.notify('READY=1')

     try:
          servo = 13

          pwm = pigpio.pi()
          pwm.set_mode(servo, pigpio.OUTPUT)
          pwm.set_PWM_frequency( servo, 25000 )
          pwm.set_PWM_range(servo, 100)
          print("X735 PWM Fan Control connected to GPIO")

          while True:
               # get CPU temp
               file = open("/sys/class/thermal/thermal_zone0/temp")
               temp = float(file.read()) / 1000.00
               temp = float('%.2f' % temp)
               file.close()

               # Set duty cycle based on temperature
               if(temp > 30):
                    pwm.set_PWM_dutycycle(servo, 40)

               if(temp > 50):
                    pwm.set_PWM_dutycycle(servo, 50)

               if(temp > 55):
                    pwm.set_PWM_dutycycle(servo, 75)

               if(temp > 60):
                    pwm.set_PWM_dutycycle(servo, 90)

               if(temp > 65):
                    pwm.set_PWM_dutycycle(servo, 100)

               if(temp < 30):
                    pwm.set_PWM_dutycycle(servo, 0)
               time.sleep(1)


     except KeyboardInterrupt as ki:
          print('X735: Cleaning up GPIOs...')
          GPIO.cleanup()

