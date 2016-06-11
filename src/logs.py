from datetime import datetime
from os import path

"""Write log about readings to file"""
def log(readings):
    datenow = datetime.now()
    filename = "logs/" + datenow.strftime("%Y-%m-%d")
    if not path.isfile(filename):
        file = open(filename, 'w')
        file.write("time\t\tGPIO\tTemperature, C\tHumidity, %\n")
    file = open(filename, 'a')
    for key,val in readings.items():
        file.write(str(val['timestamp'].strftime("%H:%M:%S")) + "\t")
        file.write(key + "\t")
        file.write(str(val['temp']) + "\t\t")
        file.write(str(val['humid']) + "\n")
    file.write("\n")
    file.close()
