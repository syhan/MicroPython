import dht
import machine

d = dht.DHT11(machine.Pin(14))

def read():
    d.measure()

    return (d.temperature(), d.humidity())
