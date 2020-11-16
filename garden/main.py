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
    print("Start measuring sensor: {}\n".format(machine_id))

    client = MQTTClient(machine_id.encode(), MQTT_SERVER)
    client.connect()

    try:
        sensor = Sensor()
        t, h = sensor.getTemperature(), sensor.getHumidity()
        
        # follow influxdb line protocol defined in https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/
        client.publish("sensors/{}/temperature".format(machine_id).encode(), "temperature,sensor={} value={}".format(machine_id, t))
        print("Publish measurement {} to topics sensors/{}/temperature\n".format(t, machine_id))

        client.publish("sensors/{}/humidity".format(machine_id).encode(), "humidity,sensor={} value={}".format(machine_id, h))
        print("Publish measurement {} to topics sensors/{}/humidity\n".format(h, machine_id))

        battery = Battery()
        v = battery.getVoltage()
        client.publish("sensors/{}/voltage".format(machine_id).encode(), "voltage,sensor={} value={}".format(machine_id, v))
        print("Publish measurement {} to topics sensors/{}/voltage\n".format(v, machine_id))    
    finally:
        client.disconnect()


def deep_sleep(msecs):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    rtc.alarm(rtc.ALARM0, msecs)

    # put the device to sleep
    print("Deep sleep {} millesecond".format(msecs))
    machine.deepsleep()

def main():
    # before we start, let's give the chipset a breath
    time.sleep_ms(1200)

    connect_wifi()
    
    measure()

    # sleep 30 minutes then wake up
    deep_sleep(30 * 60 * 1000)
    
    
if __name__ == "__main__":
    main()