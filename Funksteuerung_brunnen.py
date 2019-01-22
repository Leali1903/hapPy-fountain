# /wiringPi/433Utils/RPi_utils $ sudo ./codesend 5506385

from subprocess import call
import time

print("Start")
print("A an")
call(['sudo', '/home/pi/wiringPi/433Utils/RPi_utils/codesend 5506385'])
time.sleep(2)
print("A aus")
call(['sudo', '/home/pi/wiringPi/433Utils/RPi_utils/codesend 5506388'])
time.sleep(2)
print("Ende")