# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel

from config import *

class LED_strips:
    def __init__(self):
        global pixels
        pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
        ## Turn off pixels by default
        pixels.fill((0, 0, 0, 0))       ## WRGB
        pixels.show()
        time.sleep(0.1)
    
    def apply_signal_to_leds(self, inputMatrix):
        global pixels
        #if previous == current 
        #    doNothing = 1
        #    time.sleep(0.5)
        #    continue

        ## Set light for main/top panel
        for i in range(pos_led_top[0],pos_led_top[1]):
            val = int(inputMatrix[0][0]*150)
            pixels[i] = (0,0,0,val)         ## WRGB
            
        ## Set light for left led panel
        for i in range(pos_led_left[0],pos_led_left[1]):
            val = int(inputMatrix[1][0]*150)
            pixels[i] = (0,0, 0, val)         ## WRGB
            
        ## Set light for right led panel
        for i in range(pos_led_right[0],pos_led_right[1]):
            val = int(inputMatrix[2][0]*150)
            pixels[i] = (0,0,0,val)         ## WRGB
            

        # Comment this line out if you have RGBW/GRBW NeoPixels
        #pixels.fill((0, 255, 0))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        #pixels.fill((0, 0, 0, 0))
        pixels.show()
        time.sleep(0.1)

        # Comment this line out if you have RGBW/GRBW NeoPixels
        #pixels.fill((0, 0, 255))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        # pixels.fill((0, 0, 255, 0))
        #pixels.show()
        #time.sleep(1)

        #rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
