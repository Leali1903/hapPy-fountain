import os
import time
import board
import neopixel
import pygame
from threading import Thread

pixel_pin = board.D10

# Anzahl der NeoPixels
num_pixels = 60

# Reihenfolge der pixel-Farben - RGB oder GRB.
ORDER = neopixel.GRB

# Spezifikation des Typs der Lichterkettte und einstellen der Helligkeit
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

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
class led(Thread):
    def __init__(self):
        Thread.__init__(self)

    def cycle(wait, wheel, self):
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


class music(Thread):
    def __init__(self):
        Thread.__init__(self)

    def find_play_tracks(folder, self):
        for root, dirs, files in os.walk(folder):
            for tracks in files:
                if tracks.endswith(".mp3"):
                    print(tracks)
                    pygame.mixer.music.load(folder + tracks)
                    pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
        return tracks



folder = "/home/pi/Music/happy/"
wheel = wheel_color()
wait = 0.0001

if __name__ == '__main__':
    a = led()
    b = music()

    a.start()
    b.start()