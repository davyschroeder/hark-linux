# MicroPython blink for ESP32 (pin 2) or Pi Pico ("LED")
# Upload and run:  mpremote connect /dev/ttyUSB0 run blink.py
# Or open this file in Thonny and pick your board in the bottom-right corner.
import machine
import time
import sys

pin = "LED" if "rp2" in sys.platform else 2
led = machine.Pin(pin, machine.Pin.OUT)

while True:
    led.toggle()
    time.sleep(0.5)
