import board
import neopixel
import os
import time
import random
import pygame
import socket

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
PORT = 60003
stop_input = []

###################### FUNKTIONEN DEFINIEREN ######################

### LED LICHTERKETTE ###
# Funktion zur Verteilung der Farben im Happy-Modus
def wheel_color(pos):
    # Input von verschieden Values zwischen 0 und 255 für RGB-Werte
    # Farben = Übergänge von rot zu gelb zu blau und wieder zu rot
    if pos < 0 or pos > 255:  # input-check nicht null oder kleiner oder größer 250
        r = b = g = 0  # falls doch RGB alle null --> LEDs aus.
    elif pos < 85:  # generieren von rot-gelb-Tönen für ein Drittel der LEDs
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:  # generieren von rot-blau-Tönen für ein Drittel der LEDs
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:  # generieren von blau-gelb-Tönen für ein Drittel der LEDs
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


# Funktion zur Bewegung der Farben im Sad & Happy-Modus
def cycle(wait, wheel):
    for j in range(255):
        for i in range(PIXEL_COUNT):
            pixel_index = (i * 256 // PIXEL_COUNT) + j  # bewegen des 'wheels'
            pixels[i] = wheel(pixel_index & 255)  # einspeichern der Farben aus der Wheel-Funktion
        if wheel == wheel_color:  # kreisförmige Bewegung für das bunte Wheel
            print(pixels)
            pixels.show()
            time.sleep(wait)
    if wheel == wheel_blue:  # 'Wasserbewegung' für das blaue Wheel
        print(pixels)
        pixels.show()
        time.sleep(wait)


# Funktion zur Verteilung der Farben im Sad-Modus
def wheel_blue(pos):
    # Input von verschieden Values zwischen 0 und 255 für RGB-Werte
    # Farben = unterschiedliche random Blautöne
    if pos < 0 or pos > 255:  # input-check nicht null oder kleiner oder größer 250
        r = b = g = 0  # falls doch RGB alle null --> LEDs aus.
    elif pos < 85:  # generieren eines zufälligen Blautons für ein Drittel der LEDs
        r = 40  # mit leichtem Rotanteil
        b = random.randint(120, 190)
        g = 0
    elif pos < 170:  # generieren eines zufälligen Blautons für ein anderes Drittel der LEDs
        pos -= 85
        r = 0
        b = random.randint(50, 120)
        g = 40  # mit leichtem Gelbanteil
    else:  # generieren eines zufälligen Blautons für ein anderes Drittel der LEDs
        pos -= 170  # reines blau
        r = 0
        b = random.randint(190, 255)
        g = 0
    # weitergeben der generierten RGB-Werte, je nach erforderlichem Format der Lichterkette
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


# Funktion zur Verteilung der Farben im Party-Modus
def blink_color(pos):
    if pos < 0 or pos > PIXEL_COUNT:
        r = b = g = 0
    elif pos < 10 or pos > 50:  # für erste und letzte 10 Pixel generieren einer
        r = random.randint(0, 255)  # zufälligen Farbe mit wahrscheinlich höherem Rotanteil
        b = random.randint(85, 255)
        g = random.randint(170, 255)
    elif pos < 20 or pos > 40 & pos < 50:  # für zweite und vorletzte 10 Pixel generieren
        pos -= 10  # einer zufälligen Farbe mit wahrscheinlich
        r = random.randint(85, 255)  # höherem Gelbanteil
        b = random.randint(170, 255)
        g = random.randint(0, 255)
    else:  # für alle anderen Pixel generieren einer zufälligen Farbe
        pos -= 20  # mit wahrscheinlich höherem Blauanteil
        r = random.randint(170, 255)
        b = random.randint(0, 255)
        g = random.randint(85, 255)
    # weitergeben der generierten RGB-Werte, je nach erforderlichem Format der Lichterkette
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


# Funktion zur Verteilung der Farben im Chill-Modus
def chill_color(pos):
    if pos < 0 or pos > 255:
        r = b = g = 0
    elif pos % 3 == 0:  # alle Pixel, die durch 3 teilbar sind in einem Grünton
        r = 34
        b = 34
        g = 139
    elif pos % 3 == 1:  # alle Pixel, die durch 3 mit Rest 1 teilbar sind in anderem Grün
        pos -= 85
        r = 104
        b = 34
        g = 139
    elif pos % 3 == 2:  # alle Pixel, die durch 3 mit Rest 2 teilbar sind in anderem Grün
        pos -= 170
        r = 0
        b = 69
        g = 139
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


### MUSIK FUNKTIONEN ###
# Funktion zum suchen und abspielen der Tracks
def find_tracks(folder):
    tracks = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp3"):
                print(file)
                tracks.append(folder + file)
    return tracks


def continue_playing(tracks_iterator):
    if pygame.mixer.music.get_busy():
        return True
    try:
        next_track = next(tracks_iterator)
        pygame.mixer.music.load(next_track)
        pygame.mixer.music.play()
    except StopIteration:
        return False
    return True


### SOCKET ###
def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        print('Listening for connections')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            eye_input = conn.recv(1024).decode('utf-8')
            # conn.sendall(data)
            print('Received data from client', repr(eye_input))
    return eye_input


###################### STEUERUNG JE NACH INPUT ######################
# Empfangen des Eyetracking Inputs
#eye_input = receive_data()
PORT = PORT + 1

eye_input = 'happy'

# Einschalten des pygame-mixers für die Musik
pygame.mixer.init()

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

tracks = find_tracks(folder)
random.shuffle(tracks)
tracks_iterator = iter(tracks)
while True:
    if wheel_function:
        cycle(0.001, wheel_function)  # Farbübergänge in bunt in Kreisform
    elif eye_input == 'party':
        for num in range(PIXEL_COUNT):
            # bunter Lichtstrahl durch Lichterkette
            pixels[num] = blink_color(PIXEL_COUNT)
            pixels.show()
            # Dauer jeder Farbe pro Pixel
            time.sleep(0.0001)
        # Lichterkette komplett rot bzw. pink einfärben
        pixels.fill((176, 48, 96))
        # weil sonst die Lichterkette crasht
        print(pixels)
        pixels.show()
        time.sleep(0.0001)
        for num in range(PIXEL_COUNT-1, 0, -1):
            # bunter Lichtstrahl durch Lichterkette
            pixels[num] = blink_color(PIXEL_COUNT)
            pixels.show()
            # Dauer jeder Farbe pro Pixel
            time.sleep(0.0001)
        # Lichterkette komplett rot bzw. pink einfärben
        pixels.fill((176, 48, 96))
        # weil sonst die Lichterkette crasht
        print(pixels)
        pixels.show()
        time.sleep(0.0001)
    elif eye_input == 'chillen':
        for num in range(PIXEL_COUNT):
            pixel_index = (num * 256 // PIXEL_COUNT)
            # einmal je nach Postion des Pixels einfärben
            pixels[num] = chill_color(pixel_index & 255)
        print(pixels)
        pixels.show()
    if not continue_playing(tracks_iterator):
        break

