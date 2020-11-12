from umqtt.robust import MQTTClient
from sensor import Sensor
from battery import Battery

import machine
import network
import time
import ubinascii
import micropython
micropython.alloc_emergency_exception_buf(100)

SSID = "YHHY-IoT"
SSID_PWD = "welcome1"
MQTT_SERVER = "10.0.0.159"


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(SSID, SSID_PWD)

        while not wlan.isconnected():
            machine.idle()

    print("WiFi connected: {}\n".format(wlan.ifconfig()))

def measure():
    client = MQTTClient(ubinascii.hexlify(machine.unique_id()), MQTT_SERVER)

    sensor = Sensor()
    client.publish(f"sensors/{machine.unique_id()}/temperature".encode(), sensor.getTemperature())
    client.publish(f"sensors/{machine.unique_id()}/humidity".encode(), sensor.getHumidity())

    battery = Battery()
    client.publish(f"sensors/{machine.unique_id()}/voltage".encode(), battery.getVoltage())

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
