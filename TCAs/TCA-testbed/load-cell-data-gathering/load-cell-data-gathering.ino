/*
 5/2/23
 Ali Jones
 Adapted from:
 
 Example using the SparkFun HX711 breakout board with a scale
 By: Nathan Seidle
 SparkFun Electronics
 Date: November 19th, 2014
 License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).

 This example demonstrates basic scale output. See the calibration sketch to get the calibration_factor for your
 specific load cell setup.

 This example code uses bogde's excellent library: https://github.com/bogde/HX711
 bogde's library is released under a GNU GENERAL PUBLIC LICENSE

 The HX711 does one thing well: read load cells. The breakout board is compatible with any wheat-stone bridge
 based load cell which should allow a user to measure everything from a few grams to tens of tons.
 Arduino pin 2 -> HX711 CLK
 3 -> DAT
 3.3V -> VCC
 GND -> GND

 The HX711 board can be powered from 2.7V to 5V so the Arduino 5V power should be fine.

*/

// Import all the things
#include "HX711.h"  // load cell
#include <Adafruit_MAX31856.h>  // thermocouple
#include <string.h>

HX711 scale;
Adafruit_MAX31856 maxthermo = Adafruit_MAX31856(10, 11, 12, 13);

// definitions
#define calibration_factor 13830 //This value is obtained using the SparkFun_HX711_Calibration sketch
#define DAT  6
#define CLK  5

// globals
int signal_pin = 12;
int signal_data;
long time_interval_signal = 30 * 1000;  // pulse frequency (ms)
long time_interval_load = 0.2 * 1000; // data collection frequency (ms)
unsigned long previous_time_signal = millis();
unsigned long previous_time_load = millis();
unsigned long current_time;


void setup() {
  // Set up signal pin
  pinMode(signal_pin, OUTPUT);
  digitalWrite(signal_pin, LOW);
  signal_data = 0;

  // Set up serial monitor
  Serial.begin(9600);
  while (!Serial) delay(10);

  // Set up load cell
  scale.begin(DAT, CLK);
  scale.set_scale(calibration_factor); // This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); // Assuming there is no weight on the scale at start up, reset the scale to 0

  // Set up thermocouple
  if (!maxthermo.begin()) {
    Serial.println("Could not initialize thermocouple.");
  }
  maxthermo.setThermocoupleType(MAX31856_TCTYPE_K);
  maxthermo.setConversionMode(MAX31856_CONTINUOUS);

  // 5 second delay to let me clear the serial monitor and start any data grabbing scripts 
  delay(5000);

  // Print column headers
  Serial.print("Time (s)");
  Serial.print(",");
  Serial.println("Force (g)");
  // Serial.print(",");
  // Serial.println("Ambient temperature (c)");
}

void loop() {

  current_time = millis();

  // 2-11, not currently using
  // change signal data every square wave interval
  if (current_time - previous_time_signal > time_interval_signal){
    // update the previous time increment
    previous_time_signal = current_time;

    // if pin is on, turn it off
    if(digitalRead(signal_pin) == 1){
      digitalWrite(signal_pin, 0);
      signal_data = 0;
    }
    // otherwise, turn it on
    else{
      digitalWrite(signal_pin, 1);
      signal_data = 1;
    }
  }

  // get load cell data and print every 500ms
  if (current_time - previous_time_load > time_interval_load){
    // update the previous time increment
    previous_time_load = current_time;

    Serial.print(current_time/1000.0);
    Serial.print(",");
    Serial.println(scale.get_units(), 4);
    // Serial.print(",");
    // Serial.println(maxthermo.readThermocoupleTemperature(), 4);
    
    // Serial.print(",");
    // Serial.print(current_time);
    // Serial.print(",");
    // Serial.println(previous_time_signal);
  }

}
