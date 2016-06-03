from sys import exit
from os import path, stat, chown
import re

"""Generates new settings file"""
def generateSettings():
    file = open('settings', 'w+')

    file.write("# Sensor type. 11 22 or 2302\n")
    file.write("type:\n\n")
    file.write("# Used GPIOs (separate with spaces)\n")
    file.write("GPIO:\n\n")
    file.write("# Email addresses (separate with spaces). Used to send errors\n")
    file.write("email:\n")

    file.close()
    uid = stat('.').st_uid          # Change directory owner
    gid = stat('.').st_gid          # Get directory owner group
    chown("settings", uid, gid)     # Change file owner

"""Checks if given list has unique arguments"""
def listUnique(list):
    setset = set()
    return not any(element in setset or setset.add(element) for element in list)

"""Splits given value to list"""
def splitValue(key, value):         # Error if lines contain bad symbols
    if not re.match("^[a-z0-9.@ ]*$", value):
        print ("Settings file error. Line near '{}' contains bad symbols".format(key))
        print ("Allowed symbols are letters, numbers, spaces, '.', '@'")
        exit()

    if key == 'gpio':   # Checks if GPIOs are numbers and splits to int list
        try:
            value = value.split(' ')
            value = map(int, value)
        except ValueError:
            print ("Settings file error. Line near '{}'. GPIO can only be numbers".format(key))
            exit()
        except Exception:
            print ("Settings file error. Line near '{}'. Check example".format(key))
            exit()
        if not listUnique(value):
            print("Settings file error. 2 or more same GPIOs given.")
            exit()

    if key == 'email':  # Checks if email is good and splits to list
        value = value.split(' ')
        for elem in value:
            if not len(elem.split('@')) == 2:
                print ("Settings file error. Line near '{}'. Bad email given.".format(key))
                exit()
            if not len(elem.split('.')) > 1:
                print ("Settings file error. Line near '{}'. Bad email given.".format(key))
                exit()
        if not listUnique(value):
                print ("Settings file error. 2 or more same emails given.")
                exit()
    return value

"""Checks if settings file has all needed information: type, gpio and email"""
def checkSettingsFinal(sett):
    correct = True      # if false, then settings are not correct
    if not 'type' in sett:
        print ("Settings file error. Missing sensor type. Check settings.")
        correct = False
    if not 'gpio' in sett:
        print ("Settings file error. Missing GPIOs. Check settings.")
        correct = False
    if not 'email' in sett:
        print ("Settings file error. Missing email. Check settings.")
        correct = False

    if not correct:
        exit()

"""Checks if keys and values are correct"""
def checkKeyValue(key, value, sett, defaulttype, sensors):
    if key.strip() == "":       # Error if key is empty
        print ("Settings file error. Check example")
        exit()

    if key in sett:             # Error if key already exists
        print ("Settings file error. Setting '{}' already exists".format(key))
        exit()

    if value.strip() == "":     # Error if value is empty
        if key == 'type':       # but if value, then use defaul
            value = defaulttype
        else:
            print ("Settings file error. Missing values near {}. Check example".format(key))
            exit()
    elif key == 'type':         # Error if value is not alowed sensor type
        if not value in sensors:
            print ("Settings file error. Line near '{}'. Bad sensor type".format(key))
            print ("Alowed sensor types are: '2302' '11' '22'")
            exit()
    return key, value


"""Reads settings from file"""
def readSettings(defaulttype, sensors):
    if not path.isfile('settings'): # If no settings file - generate it and exit
        generateSettings()
        print("Settings file error. Settings file missing")
        print ("Settings file generated. Check it.")
        exit()
    sett = dict()
    file = open("settings", "r")
    for line in file:
        if line.isspace():          # Skip spaces
            continue
        if line[0:1] == "#":        # Skip comments
            continue

        try:                        # Error if line format is bad no : symbol
            key, value = line.split(":", 1)
            key = key.lower().strip()
            value = value.lower().strip()
        except ValueError:
            print ("Settings file contains errors. Check example")
            exit()
        
        key, value = checkKeyValue(key, value, sett, defaulttype, sensors)
        if key in ['email', 'gpio']:
            value = splitValue(key, value)
        sett[key.lower()] = value
        
    file.close()
    checkSettingsFinal(sett)
    return sett
