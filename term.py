#!/usr/bin/python

import Adafruit_DHT as dht
import argparse
import sys

# Sensor list
sensors = { '11': dht.DHT11,
            '22': dht.DHT22,
            '2302':dht.AM2302}

# GPIOs list
gpio = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

def listUnique(list):
    """Checks if given list has unique arguments"""
    setset = set()
    return not any(element in setset or setset.add(element) for element in list)

def parserCheck(argz):
    """Checks if given command-line arguments are correct"""
    if argz.s in sensors:
        print ('Sensor type: OK')
    else:
        sys.exit("error:Incorrect sensor type. '11' '22' '2302' are correct")
    for gp in argz.g:
        if not gp in gpio:
            sys.exit("error:Incorrect GPIOs given")
    if not listUnique(argz.g):
        sys.exit("error:Some GPIOs are given twice")
    print ('GPIOs: OK')

def parser():
    """Parses arguments from command line"""

    parser = argparse.ArgumentParser()
    # Sensor type
    parser.add_argument('-s', nargs='?', default='2302', help="Sensor type. For exampe 2302 for AM2302 sensor")
    # GPIOs
    parser.add_argument('-g', nargs='+', required=True, type=int, help="GPIOs numbers. For example 14 for GPIO14")
    argz = parser.parse_args()
    parserCheck(argz)
    return argz

print (sys.argv[0])

argz = parser()
sensor = sensors[argz.s]
print("Test passed!\n")

for gp in argz.g:
    humidity, temperature = dht.read(sensor, gp)
    print ("GPIO{}".format(gp))
    if humidity is not None and temperature is not None:
        print ('Temperature: {0:0.1f}\nHumidity: {1:0.1f}'.format(temperature, humidity))
    else:
        print ("Failed to get reading")
    print ("")
