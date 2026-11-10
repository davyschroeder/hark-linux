#!/usr/bin/env python3
"""Shows the temperature as scrolling text; the colour follows the temperature."""
import time

try:
    from sense_hat import SenseHat
    sense = SenseHat()
except Exception:
    from sense_emu import SenseHat
    sense = SenseHat()

while True:
    t = sense.get_temperature()
    colour = (0, 120, 255) if t < 18 else (0, 255, 0) if t < 25 else (255, 60, 0)
    sense.show_message(f"{t:.1f}C", text_colour=colour, scroll_speed=0.06)
    time.sleep(1)
