import os
import time
import board
import neopixel
import random
import pygame
from threading import Thread

eye_input = 'party'

###################### KONSTANTEN UND EINSTELLUNGEN ######################

### BRUNNEN ###

# Zustände für den Brunnen definieren
ON = 'sudo /home/pi/wiringPi/433Utils/RPi_utils/codesend 5506385'  # Befehl zum senden via WiringPi in Console
OFF = 'sudo /home/pi/wiringPi/433Utils/RPi_utils/codesend 5506388'  # Befehl zum senden via WiringPi in Console

### LED LICHTERKETTE ###

# Eingabe Data-Output-Pin (18 & 12 = mit PWM, 10 = SPI)
pixel_pin = board.D10

# Anzahl der NeoPixels
num_pixels = 60

# Reihenfolge der pixel-Farben - RGB oder GRB.
ORDER = neopixel.GRB

# Spezifikation des Typs der Lichterkettte und einstellen der Helligkeit
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)


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
    while True:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j  # bewegen des 'wheels'
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
    if pos < 0 or pos > num_pixels:
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
def find_play_tracks(folder):
    for root, dirs, files in os.walk(folder):
        for tracks in files:
            if tracks.endswith(".mp3"):
                print(tracks)
                pygame.mixer.music.load(folder + tracks)
                pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
    return tracks


###################### STEUERUNG JE NACH INPUT ######################

# Einschalten des pygame-mixers für die Musik
pygame.mixer.init()

# Inputschleife
if eye_input == 'happy':
    ### BRUNNEN ###
    os.system(ON)
    time.sleep(60)  # rausnehmen weil nach Liedern ausgeschaltet
    os.system(OFF)
    ### MUSIK ###
    folder = "/home/pi/Music/happy/"
    # tracks = find_play_tracks(folder)
    # ### LED LICHTERKETTE ###
    # while True:  # weil es sich immer weiter bewegen soll.
    #     cycle(0.001, wheel_color)  # Farbübergänge in bunt in Kreisform
    music = Thread(target=find_play_tracks(folder))
    music.start()
    led = Thread(target=cycle(0.001, wheel_color))
    led.start()
    music.join()

elif eye_input == 'sad':
    ### BRUNNEN ###
    os.system(ON)
    time.sleep(60)  # rausnehmen weil nach Liedern ausgeschaltet
    os.system(OFF)
    ### MUSIK ###
    folder = "/home/pi/Music/sad/"
    tracks = find_play_tracks(folder)
    ### LED LICHTERKETTE ###
    while True:  # weil es sich immer weiter bewegen soll.
        cycle(0.001, wheel_blue)  # zum Verändern der Blautöne über die Zeit pro Pixel

elif eye_input == 'chillen':
    ### BRUNNEN ###
    os.system(ON)
    time.sleep(60)  # rausnehmen weil nach Liedern ausgeschaltet
    os.system(OFF)
    ### MUSIK ###
    folder = "/home/pi/Music/chillen/"
    tracks = find_play_tracks(folder)
    ### LED LICHTERKETTE ###
    for num in range(num_pixels):
        chill_color(num)  # da hier keine Veränderung über die Zeit geschieht
        # einmal je nach Postion des Pixels einfärben

elif eye_input == 'party':
    ### BRUNNEN ###
    os.system(OFF)  # falls Brunnen schon an.
    ### MUSIK ###
    folder = "/home/pi/Music/party/"
    tracks = find_play_tracks(folder)
    ### LED LICHTERKETTE ###
    while True:  # weil es sich immer weiter bewegen soll.
        for num in range(num_pixels):
            pixels[num] = blink_color(num)  # bunter Lichtstrahl durch Lichterkette
            pixels.show()
            time.sleep(0.0001)  # Dauer jeder Farbe pro Pixel
        pixels.fill((176, 48, 96))  # Lichterkette komplett rot bzw. pink einfärben
        print(pixels)  # weil sonst die Lichterkette crasht
        pixels.show()
        time.sleep(0.0001)

else:
    ### BRUNNEN ###
    os.system(OFF)
    ### MUSIK ###
    pygame.mixer.music.stop()
    ### LED LICHTERKETTE ###
    pixels.fill((0, 0, 0))  # Ausschalten der Lichterkette









