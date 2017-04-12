from umqtt.simple import MQTTClient

import machine
import time
import ubinascii

import wifi
import blink
import sensor

client = MQTTClient(ubinascii.hexlify(machine.unique_id()), "192.168.0.20")

def work():
    current = sensor.read()
    blink.blink_once()

    client.connect()
    client.publish(b"/temp", str(current[0]))
    blink.blink_twice()
    client.publish(b"/humi", str(current[1]))
    blink.blink_twice()
    client.disconnect()

def main():
    wifi.connect()
    blink.blink_twice()

    while True:
        work()
        time.sleep(5)

if __name__ == '__main__':
    main()
