# EE_250_Final_Project
IoT temperature and humidity sensor + user controller bridged by MQTT broker

Team member names:
Ian Gravallese

Video Demonstration link:


HOW TO COMPILE:

  sensor side:
  
    required software:
    
      Eclipse paho-mqtt:
        intsall with:
          pip install paho-mqtt
          
      Dexter GrovePi:
        install with:
          curl -kL dexterindustries.com/update_grovepi | bash
  
  
python library imports:
    
      import time
      import math
      import paho.mqtt.client as mqtt
      import grovepi
      from grovepi import *
      from grove_rgb_lcd import *
      
      
  controller side:
    
    required software:
    
