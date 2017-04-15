from umqtt.robust import MQTTClient

import machine
import time
import ubinascii

import wifi
import sensor.dht11 as sensor
import micropython
micropython.alloc_emergency_exception_buf(100)

timer = machine.Timer(42)
client = MQTTClient(ubinascii.hexlify(machine.unique_id()), "192.168.0.20")

def work():
    current = sensor.read()

    client.publish(b"sensors/balcony/temperature", str(current[0]))
    client.publish(b"sensors/balcony/humidity", str(current[1]))

def main():
    wifi.connect()
    client.connect()

    timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=lambda _: work())

if __name__ == "__main__":
    main()
