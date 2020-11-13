import machine
import dht
import time

class Sensor:
    def __init__(self, pin = 4):
        self.pin = pin
        self.sensor = dht.DHT11(machine.Pin(pin))
        
    def measure(self):
        self.sensor.measure()
        while not self.sensor.humidity():
            time.sleep_ms(1200)
            
    def getTemperature(self):
        self.measure()
        return self.sensor.temperature()
        
    def getHumidity(self):
        self.measure()
        return self.sensor.humidity()
