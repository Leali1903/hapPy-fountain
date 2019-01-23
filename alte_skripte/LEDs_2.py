import board
import time
import neopixel
pixels = neopixel.NeoPixel(board.D10, 60)    # Feather wiring!
# pixels = neopixel.NeoPixel(board.D18, 30) # Raspberry Pi wiring!

# pixels[0] = (255, 0, 0)


pixels.fill((0, 0, 0))
strip = neopixel.NeoPixel
