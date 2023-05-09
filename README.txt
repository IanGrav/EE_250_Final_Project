# EE_250_Final_Project
IoT temperature and humidity sensor + user controller bridged by MQTT broker

Team member names:
Ian Gravallese

How to compile:

  sensor side:
  
  required software:
    Eclipse paho-mqtt:
      pip install paho-mqtt
    dexter
  
  
  python library imports:
    import time
    import math
    import paho.mqtt.client as mqtt
    import grovepi
    from grovepi import *
    from grove_rgb_lcd import *
