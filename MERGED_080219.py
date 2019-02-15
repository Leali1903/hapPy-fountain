import board
import neopixel
import os
import time
import random
import pygame
import socket
import threading


###################### KONSTANTEN UND EINSTELLUNGEN ######################

### BRUNNEN ###
# Zustände für den Brunnen definieren
ON = 'sudo /home/pi/wiringPi/433Utils/RPi_utils/codesend 5506385'  # Befehl zum senden via WiringPi in Console
OFF = 'sudo /home/pi/wiringPi/433Utils/RPi_utils/codesend 5506388'  # Befehl zum senden via WiringPi in Console

### LED LICHTERKETTE ###
# Eingabe Data-Output-Pin (18 & 12 = mit PWM, 10 = SPI)
pixel_pin = board.D10
# Anzahl der NeoPixels
PIXEL_COUNT = 64
# Reihenfolge der pixel-Farben - RGB oder GRB.
ORDER = neopixel.GRB
# Spezifikation des Typs der Lichterkettte und einstellen der Helligkeit
pixels = neopixel.NeoPixel(pixel_pin, PIXEL_COUNT, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

# Socket für Datenempfang
HOST = '172.16.107.164'
EYE_INPUT_PORT = 60003
STOP_PORT = EYE_INPUT_PORT + 1
RUNNING = True

###################### FUNKTIONEN DEFINIEREN ######################

### LED LICHTERKETTE ###
# Funktion zur Verteilung der Farben im Happy-Modus
def wheel_color(pos):
    # Input von verschieden Values zwischen 0 und 255 für RGB-Werte
    # Farben = Übergänge von rot zu gelb zu blau und wieder zu rot
    if pos < 0 or pos > 255:
        r = b = g = 0
    # generieren von rot-gelb-Tönen für ein Drittel der LEDs
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    # generieren von rot-blau-Tönen für ein Drittel der LEDs
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    # generieren von blau-gelb-Tönen für ein Drittel der LEDs
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


# Funktion zur Bewegung der Farben im Sad & Happy-Modus
def cycle(wait, wheel):
    for j in range(255):
        for i in range(PIXEL_COUNT):
            # bewegen des 'wheels'
            pixel_index = (i * 256 // PIXEL_COUNT) + j
            # einspeichern der Farben aus der Wheel-Funktion
            pixels[i] = wheel(pixel_index & 255)
        # kreisförmige Bewegung für das bunte Wheel
        if wheel == wheel_color:
            # Ausgabe der Pixeldaten, weil LED sonst überfordert
            print(pixels)
            pixels.show()
            time.sleep(wait)
    # 'Wasserbewegung' für das blaue Wheel
    if wheel == wheel_blue:
        # Ausgabe der Pixeldaten, weil LED sonst überfordert
        print(pixels)
        pixels.show()
        time.sleep(wait)


# Funktion zur Verteilung der Farben im Sad-Modus
def wheel_blue(pos):
    # Input von verschieden Values zwischen 0 und 255 für RGB-Werte
    # Farben = unterschiedliche random Blautöne
    if pos < 0 or pos > 255:
        r = b = g = 0
        # generieren eines zufälligen Blautons für ein Drittel der LEDs mit leichtem Rotanteil
    elif pos < 85:
        r = 40
        b = random.randint(120, 190)
        g = 0
    # generieren eines zufälligen Blautons für ein anderes Drittel der LEDs, leichter Gelbanteil
    elif pos < 170:
        pos -= 85
        r = 0
        b = random.randint(50, 120)
        g = 40
    # generieren eines zufälligen Blautons für ein anderes Drittel der LEDs, reines blau
    else:
        pos -= 170
        r = 0
        b = random.randint(190, 255)
        g = 0
    # weitergeben der generierten RGB-Werte, je nach erforderlichem Format der Lichterkette
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


# Funktion zur Verteilung der Farben im Party-Modus
def blink_color(pos):
    if pos < 0 or pos > PIXEL_COUNT:
        r = b = g = 0
    # für erste und letzte 10 Pixel generieren einer zufälligen Farbe mit wahrscheinlich höherem Rotanteil
    elif pos < 10 or pos > 50:
        r = random.randint(0, 255)
        b = random.randint(85, 255)
        g = random.randint(170, 255)
    # für zweite und vorletzte 10 Pixel generieren einer zufälligen Farbe mit wahrscheinlich höherem Gelbanteil
    elif pos < 20 or pos > 40 & pos < 50:
        pos -= 10
        r = random.randint(85, 255)
        b = random.randint(170, 255)
        g = random.randint(0, 255)
    # für alle anderen Pixel generieren einer zufälligen Farbe mit wahrscheinlich höherem Blauanteil
    else:
        pos -= 20
        r = random.randint(170, 255)
        b = random.randint(0, 255)
        g = random.randint(85, 255)
    # weitergeben der generierten RGB-Werte, je nach erforderlichem Format der Lichterkette
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


#alle LEDs Rot für Teil des Party-Modus
def fill_red():
    # Lichterkette komplett rot bzw. pink einfärben
    pixels.fill((176, 48, 96))
    # weil sonst die Lichterkette crasht
    print(pixels)
    pixels.show()


# einfärben der LED in Bunt für den 2. Teil des Partymodus
def fill_blink(start, end):
    updater = 1 if start <= end else -1
    for num in range(start, end, updater):
        # bunter Lichtstrahl durch Lichterkette
        pixels[num] = blink_color(PIXEL_COUNT)
        pixels.show()
        # Dauer jeder Farbe pro Pixel
        time.sleep(0.0001)


# Funktion zur Verteilung der Farben im Chill-Modus
def chill_color(pos):
    if pos < 0 or pos > 255:
        r = b = g = 0
    # alle Pixel, die durch 3 teilbar sind in einem Grünton
    elif pos % 3 == 0:
        r = 34
        b = 34
        g = 139
    # alle Pixel, die durch 3 mit Rest 1 teilbar sind in anderem Grün
    elif pos % 3 == 1:
        pos -= 85
        r = 104
        b = 34
        g = 139
    # alle Pixel, die durch 3 mit Rest 2 teilbar sind in anderem Grün
    elif pos % 3 == 2:
        pos -= 170
        r = 0
        b = 69
        g = 139
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


### MUSIK FUNKTIONEN ###
# Funktion zum suchen und abspielen der Tracks
def find_tracks(folder):
    tracks = []
    # durchsuchen des Folders nach Inhalten
    for root, dirs, files in os.walk(folder):
        for file in files:
            # Filtern aller mp3 files
            if file.endswith(".mp3"):
                print(file)
                # alle mp3 files in eine Liste schreiben
                tracks.append(folder + file)
    # Trackliste zurück geben
    return tracks

# Funktion zum abspielen der Tracks
def continue_playing(tracks_iterator):
    # falls noch Lied gespielt - nichts ändern
    if pygame.mixer.music.get_busy():
        return True
    # falls nicht nächsten track laden und spielen
    try:
        next_track = next(tracks_iterator)
        pygame.mixer.music.load(next_track)
        pygame.mixer.music.play()
    # außer es gibt keine Lieder mehr
    except StopIteration:
        return False
    return True


### SOCKET ###
# Socket zum Empfangen der Eye-Input Daten
def receive_eye_input_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bereit machen für Empfang
        s.bind((HOST, EYE_INPUT_PORT))
        s.listen()
        print('Listening for connections')
        # akzeptieren der Daten
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            received_data = conn.recv(1024).decode('utf-8')
            print('Received data from client ', repr(received_data))
    # Zurückgabe der Empfangenen Daten
    return received_data


# Socket zum Empfangen der Stopdaten
def receive_stop_data():
    # damit Threading möglich ist --> globale Variable
    global RUNNING
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bereit machen für Empfang
        s.bind((HOST, STOP_PORT))
        s.listen()
        print('Listening for connections')
        # akzeptieren der Daten
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            received_data = conn.recv(1024).decode('utf-8')
            print('Received data from client ', repr(received_data))
            # Beenden des Output
            if received_data == 'stop':
                RUNNING = False
    # Zurückgabe der empfangenen Daten
    return received_data

###################### STEUERUNG JE NACH INPUT ######################
# Empfangen des Eyetracking Inputs
eye_input = receive_eye_input_data()

# Einschalten des pygame-mixers für die Musik
pygame.mixer.init()

# Generieren der Outputparameter je nach Input
folder = ""
wheel_function = None
if eye_input == 'happy':
    os.system(ON)
    folder = "/home/pi/Music/happy/"
    wheel_function = wheel_color
elif eye_input == 'sad':
    os.system(ON)
    folder = "/home/pi/Music/sad/"
    wheel_function = wheel_blue
elif eye_input == 'chillen':
    os.system(ON)
    folder = "/home/pi/Music/chillen/"
    wheel_function = None
elif eye_input == 'party':
    os.system(OFF)
    folder = "/home/pi/Music/party/"
    wheel_function = None

# Auf weiteren Input hoeren im Hintergrund
thread = threading.Thread(target=receive_stop_data)
thread.daemon = True
thread.start()

# Suchen der Tracks
tracks = find_tracks(folder)
# Mischen der Tracks, damit nicht immer die gleiche Reihenfolge
random.shuffle(tracks)
# Iterator zum Abspielen der Tracks
tracks_iterator = iter(tracks)

# Laufen solange kein Stopinput erhalten
while RUNNING:
    # wenn es eine wheelfunction gibt diese abspielen
    if wheel_function:
        time.sleep(0.0001)
        cycle(0.001, wheel_function)  # Farbübergänge in bunt in Kreisform
    # falls nicht und der Input Party ist, Partyfunktionen aufrufen
    elif eye_input == 'party':
        fill_blink(0, PIXEL_COUNT)
        fill_red()
        time.sleep(0.0001)
        fill_blink(PIXEL_COUNT, 0)
        fill_red()
        time.sleep(0.0001)
    # falls nicht und der Input chillen ist, Chillcolor einfärben
    elif eye_input == 'chillen':
        for num in range(PIXEL_COUNT):
            pixel_index = (num * 256 // PIXEL_COUNT)
            # einmal je nach Postion des Pixels einfärben
            pixels[num] = chill_color(pixel_index & 255)
        print(pixels)
        pixels.show()
    # Aufhören falls keine Tracks mehr vorhanden sind
    if not continue_playing(tracks_iterator):
        break

# wenn stop_input erhalten alle Funktionen abschalten
# Musik aus
pygame.mixer.music.stop()
# Brunnen aus
os.system(OFF)
# LED aus
pixels.fill((0,0,0))
pixels.show()
