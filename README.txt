# EE_250_Final_Project
IoT temperature and humidity sensing device + user controller bridged by MQTT broker

Team member names:
Ian Gravallese

Video Demonstration link:
https://drive.google.com/drive/folders/1-wWi51HbLVvCdJqoO6Y6B84e50Zxb_mW?usp=sharing

HOW TO COMPILE:
To compile my project, first you need an MQTT-Broker up and running. I installed Eclipse Mosquitto on my
Windows laptop, editing the network firewall to allow other computers to connect to mine and editing the
Mosquitto configuration file, adding "allow_anonymous_true" and "listener 1883" (the port I was using) 
in order to get it up and running functionally (simply open Windows powershell as an adminstrator and 
type "net start mosquitto" to begin the MQTT-Broker service). However, if you have an MQTT-Broker up 
and running already, that will do as well. I originally had the IP adress and port number of my MQTT-Broker 
hard coded into my python scripts, but have since edited them so that the user enters the IP adress and 
port number of the MQTT-Broker they wish to connect to. So just enter those in the terminal upon running 
the scripts and they should connect to your MQTT-Broker and work. Both Scripts work essentially 
independently of the other, meaning you don't need one up for the other to begin, so starting them 
in either order works. Just scp the rpi script to an rpi with all of the required libraries installed 
and the file can be run on the rpi with a simple "python3 <filename>.py" Then clone the VM script to 
an ubuntu machine that has all of the required libraries installed and that should run with a simple 
with a simple "python3 <filename>.py" as well.



All external libraries required are listed below:

  sensor (Rpi) side:
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
  
  controller (VM) side:
    required software:
      Eclipse paho-mqtt:
        install with:
          pip install paho-mqtt
      Plotly Express:
        install with:
          pip install plotly_express==0.4.0
      Pandas:
        install with:
          pip install pandas
      Kaleido:
        install with:
          pip install -U kaleido
    python library imports:
      import paho.mqtt.client as mqtt
      import time
      import pandas as pd
      import plotly.express as px
