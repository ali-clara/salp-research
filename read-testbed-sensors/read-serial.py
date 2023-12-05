#!/usr/bin/env python3
# adapted from https://www.learnrobotics.org/blog/arduino-data-logger-csv/

import serial
import csv
import time
import keyboard

# setup
start_time = time.time()
# Arduino serial port
arduino_port = "COM3"
# Arduino baud rate (make sure it matches)
baud = 9600
# serial connection
ser = serial.Serial(arduino_port, baud)
print(f"Connected to Arduino port {arduino_port}")
print("Beginning load cell data collection, press 'q' when finished")
sensor_data = []
# loop until the "q" key is pressed
while not keyboard.is_pressed("q"):
    # parse and print Arduino data (split with commas)
    get_data = ser.readline()
    data_string = get_data.decode('utf-8')
    data_raw = data_string[0:][:-2]
    data_out = data_raw.split(",")
    print(data_out)

    sensor_data.append(data_out)

print("Exiting data collection")

# save data to csv

############# CHANGE THESE PARAMS #############
sensor = "encoder"
watts = "4"

try:
    filename = sensor+"_data/"+watts+"W/"+sensor+"-data_"+str(start_time)+".csv"    
    with open (filename, 'w', encoding='UTF8', newline='') as f:
        write = csv.writer(f)
        write.writerows(sensor_data)
except FileNotFoundError:
    print("Folder not found, check your working directory or your spelling. Saving to parent directory instead")
    filename = str(start_time)+".csv"
    with open (filename, 'w', encoding='UTF8', newline='') as f:
        write = csv.writer(f)
        write.writerows(sensor_data)

print("Created file")

# 8/15
# first 2w - 154mm

#9/24
# 3W
# [148.3, 148.3, 151.9, 146.0, 154]
# 2W
# [154, ]
# all ~13.3 ohms

# 9/25
# 3W
# [135, 135, 146]

# 4W

