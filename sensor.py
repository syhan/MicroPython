import dht
import machine

def read():
    d = dht.DHT11(machine.Pin(14))
    d.measure()

    return (d.temperature(), d.humidity())
