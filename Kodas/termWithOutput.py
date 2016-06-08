#!/usr/bin/python

import Adafruit_DHT as dht
import argparse
import sys
from datetime import datetime

import logs
from emailsend import sendEmail
from readsettings import readSettings
from getStringforCacti import makeStrinng

# Sensor list
sensors = { '11': dht.DHT11,
            '22': dht.DHT22,
            '2302':dht.AM2302}

# Default sensor type
defSensor = '2302'

# GPIOs list
gpio = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

# Dictionary with readings from GPIOs
readings = dict()

# Critical temperature values
minTemp = 10    # Minimal temperature
maxTemp = 30    # Maximal temperature

minHum = 30     # Minimal humidity
maxHum = 70     # Maximal humidity

"""reads settings from file 'settings' """
setings = readSettings(defSensor, sensors, gpio)  # Reads settings file
print("Settings read successfully\n")

"""Reads GPIOs"""
print ("Reading sensors...")
for gp in setings['gpio']:
    readings[str(gp)] = dict()
    humidity, temperature = dht.read_retry(sensors[setings['type']], gp)
    print ("GPIO{}".format(gp))

    if humidity is not None and temperature is not None:
        print ('Temperature: {0:0.1f}\nHumidity: {1:0.1f}'.format(temperature, humidity))
        readings[str(gp)]['temp'] = float('{0:0.1f}'.format(temperature))
        readings[str(gp)]['humid'] = float('{0:0.1f}'.format(humidity))
        readings[str(gp)]['timestamp'] = datetime.now()
    else:
        print ("Failed to get reading")
        readings[str(gp)]['temp'] = None
        readings[str(gp)]['humid'] = None
        readings[str(gp)]['timestamp'] = datetime.now()
    print ("")

logs.log(readings)

"""Checks if data values are normal. If not, sends emails"""
needToSendEmail = False     # Need to send email?
for key,value in readings.items():
    if minTemp <= value['temp'] <= maxTemp or minHum <= value['humid'] <= maxHum or value['temp'] == None or value['humid'] == None:
        needToSendEmail = True

if needToSendEmail:
    sendEmail(readings, setings['email'])
    pass

makeStrinng(readings)
