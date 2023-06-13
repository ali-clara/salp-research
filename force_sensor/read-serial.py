#!/usr/bin/env python3
# adapted from https://www.learnrobotics.org/blog/arduino-data-logger-csv/

import serial
import csv
import time
import keyboard

# setup
start_time = time.time()
# Arduino serial port
arduino_port = "COM7"
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
filename = "force_data/5W/load-cell-data_"+str(start_time)+".csv"
with open (filename, 'w', encoding='UTF8', newline='') as f:
    write = csv.writer(f)
    write.writerows(sensor_data)

print("Created file")