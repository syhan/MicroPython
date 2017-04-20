@echo off
del main.py
rem copy main_temp_humi.py main.py
copy main_motion_detect.py main.py
ampy --port COM6 put dht11.py
ampy --port COM6 put hcrs501.py
ampy --port COM6 put wifi.py
ampy --port COM6 put main.py