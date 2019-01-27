from __future__ import print_function
from api import EyeXInterface
import time

lib_location = 'C:/Program Files (x86)/Tobii/Tobii EyeX Interaction/Tobii.EyeX.Client.dll'          # Speicherort dll-Datei
eye_api = EyeXInterface(lib_location)               # Zugriff auf die dll-Datei des EyeX mittels Function EyeXInterface aus api.py


def eyetracking(coordinates):           # Function zum Auslesen der Koordinaten
    print(coordinates)
    print('x: ' + str(coordinates.x))
    print('y: ' + str(coordinates.y))

   # file = open('et.txt', 'w')
    #lines = file.readlines()

    #while time.time() < 8:
        #coordinates.x, coordinates.y, coordinates.timestamp = line.split(",");
     #   file.write("%s\n" % [coordinates.x, coordinates.y, coordinates.timestamp])
    #file.close()


    #return file

# print(list_x)
#    print(list_y)
#   print(timestamp)

sec = 10
timeout = time.time() + sec   # sec Sekunden ab Start -> danach wird Skript gestoppt


#while time.time() < timeout:

eye_api.on_event += [lambda coordinates: eyetracking(coordinates)]









# Timestamp: Der erfasste Zeitstempel in Millisekunden ab dem Beginn des EyeTrackings (in ms)
# x & y





