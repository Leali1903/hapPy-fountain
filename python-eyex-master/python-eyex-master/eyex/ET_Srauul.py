from __future__ import print_function               # import für ET
from api import EyeXInterface
import time

# import für GUI


######################### KONSTANTEN & EINSTELLUNGEN #########################
# Initialisierung Eyetracking
lib_location = 'C:/Program Files (x86)/Tobii/Tobii EyeX Interaction/Tobii.EyeX.Client.dll'          # Speicherort dll-Datei
eye_api = EyeXInterface(lib_location)               # Zugriff auf die dll-Datei des EyeX mittels Function EyeXInterface aus api.py


def eyetracking(coordinates):           # Function zum Auslesen der Koordinaten
    list_coordinates.append([coordinates.timestamp/1000, coordinates.x, coordinates.y]) # Liste des Zeitstempels seit Start Eyetracker (in ms/1000 = Sek), x- & y-Koordinaten
    return list_coordinates

# Initialisierung GUI





######################### EYETRACKING #########################
list_coordinates = []
eye_api.on_event += [lambda coordinates: eyetracking(coordinates)]

sec = 10
timeout = time.time() + sec   # sec Sekunden ab Start -> danach wird Skript gestoppt

while True:
    if time.time() > timeout:
        print(list_coordinates)
        break