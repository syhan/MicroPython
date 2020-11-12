import time
from machine import Pin

pin = Pin(14, Pin.IN)

def detect(callback):
    # from https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/pins.html
    # the IRQ callback is limited, e.g. memory allocation is not allowed
    # pin.irq(trigger=Pin.IRQ_RISING, handler=callback)
    while True:
        while True:
            if pin.value() == 1:
                break
            time.sleep_ms(20)
        callback()
        time.sleep_ms(2000)
