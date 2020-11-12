# Garden

An IoT home garden project leverages NaFuture N1 (光合未来 知悉N1) to measure plant condition, trends and get notified
Ideally each NaFuture N1 sensor would measure the humidity/temperature every 30 minutes of each plant, send the result to MQTT server and deep sleep afterwards (to save battery).

The server side would be composed by eclipse-mosquitto(MQTT) + telegraf (data tranformation) + influxdb + grafana.
Alerts would be generated on grafana side if one plant is too dry or battery voltage is below certain threshold.
