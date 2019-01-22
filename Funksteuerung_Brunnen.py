# /wiringPi/433Utils/RPi_utils $ sudo ./codesend 5506385

from subprocess import call
import time
import os

on = 'sudo /home/pi/wiringPi/433Utils/RPi_utils/codesend 5506385'
off = 'sudo /home/pi/wiringPi/433Utils/RPi_utils/codesend 5506388'

eye_input = 'happy'
 
if eye_input == 'happy':
    os.system(on)
    time.sleep(60) #rausnehmen weil nach Liedern ausgeschaltet
    os.system(off)
elif eye_input == 'sad':
    os.system(on)
    time.sleep(60) #rausnehmen weil nach Liedern ausgeschaltet
    os.system(off)
elif eye_input == 'chillen':
    os.system(on)
    time.sleep(60) #rausnehmen weil nach Liedern ausgeschaltet
    os.system(off)
elif eye_input == 'party':
    os.system(off) # falls Brunnen schon an.
else:
    os.system(off)

