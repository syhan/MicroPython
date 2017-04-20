import paho.mqtt.client as mqtt
import requests
import json
import time
from datetime import datetime

def send_to_yeelink(topic, value):
    if topic.endswith("temperature"):
        sensor_id = 404020
    else:
        sensor_id = 404021

    url = "http://api.yeelink.net/v1.0/device/356531/sensor/%d/datapoints" % sensor_id
    headers = {"U-ApiKey": "7652d4a07a9f9b6ba5639e3a0b3cd3e3"}
    payload = {"timestamp": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%S"), "value": value}
    requests.post(url, headers=headers, data=json.dumps(payload))

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors/balcony/temperature")
    client.subscribe("sensors/balcony/humidity")

def on_message(client, userdata, msg):
    send_to_yeelink(msg.topic, str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if __name__ == '__main__':
    client.connect("localhost")
    client.loop_forever()
