from umqtt.robust import MQTTClient
from sensor import Sensor
from battery import Battery

import machine
import network
import time
import ubinascii

SSID = "<SSID>"
SSID_PWD = "<PASSWORD>"
MQTT_SERVER = "<MQTT_SERVER>"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(SSID, SSID_PWD)

        while not wlan.isconnected():
            machine.idle()

    print("WiFi connected: {}\n".format(wlan.ifconfig()))

def measure():
    machine_id = ubinascii.hexlify(machine.unique_id()).decode()

    client = MQTTClient(machine_id.encode(), MQTT_SERVER)
    client.connect()

    sensor = Sensor()

    print("publish to topic `sensors/{}`".format(machine_id))

    client.publish("sensors/{}/temperature".format(machine_id).encode(), str(sensor.getTemperature()))
    client.publish("sensors/{}/humidity".format(machine_id).encode(), str(sensor.getHumidity()))

    battery = Battery()
    client.publish("sensors/{}/voltage".format(machine_id).encode(), str(battery.getVoltage()))

def deep_sleep(msecs):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    rtc.alarm(rtc.ALARM0, msecs)

    # put the device to sleep
    machine.deepsleep()

def main():
    connect_wifi()

    measure()

    # sleep 30 minutes then wake up
    deep_sleep(30 * 60 * 1000)

if __name__ == "__main__":
    main()
