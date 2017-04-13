from umqtt.simple import MQTTClient

import machine
import time
import ubinascii

import wifi
import blink
import sensor_dht11 as sensor
import micropython

micropython.alloc_emergency_exception_buf(100)

timer = machine.Timer(42)

client = MQTTClient(ubinascii.hexlify(machine.unique_id()), "192.168.0.20")
client.set_callback(sub)

def sub(topic, msg):
    if msg == b"off":
        timer.deinit()
        client.disonnect()
    elif msg == b"on":
        main()

def work():
    current = sensor.read()
    blink.blink_once()

    client.publish(b"/temp", str(current[0]))
    client.publish(b"/humi", str(current[1]))
    blink.blink_twice()

def main():
    wifi.connect()
    client.connect()

    client.subscribe("/ops")
    blink.blink_twice()

    timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=work)

if __name__ == "__main__":
    main()
