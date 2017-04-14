import network
import machine

SSID = 'YHHY'
SSID_PW = 'xxxx'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(SSID, SSID_PW)

        while not wlan.isconnected():
            machine.idle()

    return wlan.ifconfig()
