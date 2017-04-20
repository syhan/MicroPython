from umqtt.robust import MQTTClient

import machine
import ubinascii

import wifi
import hcrs501 as sensor
import micropython
micropython.alloc_emergency_exception_buf(100)

client = MQTTClient(ubinascii.hexlify(machine.unique_id()), "192.168.0.20")

def notify():
    client.publish(b"sensors/motion", b"detected")

def main():
    wifi.connect()
    client.connect()

    sensor.detect(notify)

if __name__ == "__main__":
    main()
