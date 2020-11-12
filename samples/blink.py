import time
from machine import Pin

pin = Pin(16, Pin.OUT)

def blink_once():
    pin.low()
    time.sleep_ms(100)
    pin.high()
    time.sleep_ms(100)

def blink(n):
    for _ in range(n):
        blink_once()

def blink_twice():
    blink(2)

def blink_infintive():
    while True:
        blink_once()
