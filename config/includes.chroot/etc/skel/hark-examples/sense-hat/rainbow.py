#!/usr/bin/env python3
"""Rainbow on the Sense HAT LED matrix + sensor readings.
Works on a real Raspberry Pi with a Sense HAT, and on Hark Linux with the emulator:
  1. start  sense_emu_gui
  2. run    sense-python rainbow.py
"""
import colorsys
import time

try:
    from sense_hat import SenseHat
    sense = SenseHat()
except Exception:
    from sense_emu import SenseHat  # no real HAT found -> emulator
    sense = SenseHat()

step = 0
frame = 0
try:
    while True:
        pixels = []
        for y in range(8):
            for x in range(8):
                h = ((x + y) / 16 + step) % 1.0
                r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
                pixels.append((int(r * 255), int(g * 255), int(b * 255)))
        sense.set_pixels(pixels)
        step += 0.02
        frame += 1
        if frame % 50 == 0:
            print(f"Temp {sense.get_temperature():.1f} °C | "
                  f"Humidity {sense.get_humidity():.0f} % | "
                  f"Pressure {sense.get_pressure():.0f} hPa")
        time.sleep(0.05)
except KeyboardInterrupt:
    sense.clear()
