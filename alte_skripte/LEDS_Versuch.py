import time
import board
import neopixel
import random


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D10

# The number of NeoPixels
num_pixels = 60

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def rainbow_cycle_blue(wait):
    for j in range(255):
        if j < 50:
            j = 255
        else:
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel_blue(pixel_index & 255)
                #pixels[i] = wheel_blue(pixel_index)
    pixels.show()
    time.sleep(wait)

    # blau Hex 
    # 0,0,255
    # 0,51,255
    # 0,102,255
    # 0,153,255
    # 0,204,255
    # 0,255,255

def wheel_blue(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = b = g = 0
    elif pos < 85:
        r = 0
        #g = 205
        b = random.randint(100,255)
        g = 0
    elif pos < 170:
        pos -= 85
        r = 0
        #g = 238
        b = random.randint(50,255)
        g = 0
    else:
        pos -= 170
        r = 0
        #g = 255
        b = random.randint(150,255)
        g = 0
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    
    #time.sleep(0)
    rainbow_cycle_blue(0.0000000000000001)
    pixels.show()
