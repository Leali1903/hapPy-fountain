from __future__ import print_function
from api import EyeXInterface
import time

lib_location = 'C:/Program Files (x86)/Tobii/Tobii EyeX Interaction/Tobii.EyeX.Client.dll'          # Speicherort dll-Datei
eye_api = EyeXInterface(lib_location)               # Zugriff auf die dll-Datei des EyeX mittels Function EyeXInterface aus api.py


def eyetracking(coordinates):           # Function zum Auslesen der Koordinaten
    print(coordinates)
    print('x: ' + str(coordinates.x))
    print('y: ' + str(coordinates.y))
    timestamp = []
    list_x = []
    list_y = []
    timestamp = timestamp.append(coordinates.timestamp)
    list_x = list_x.append(coordinates.x)
    list_y = list_y.append(coordinates.y)

    return timestamp, list_x, list_y


eye_api.on_event += [lambda coordinates: eyetracking(coordinates)]

# Timestamp: Der erfasste Zeitstempel in Millisekunden ab dem Beginn des EyeTrackings (in ms)
# x & y

sec = 10
timeout = time.time() + sec   # sec Sekunden ab Start -> danach wird Skript gestoppt

while True:
    pass
    if time.time() > timeout:
        break

