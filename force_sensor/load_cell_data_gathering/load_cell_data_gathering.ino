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

// imports
#include "HX711.h"

HX711 scale;

// definitions
#define calibration_factor -438000 //This value is obtained using the SparkFun_HX711_Calibration sketch
#define DOUT  5
#define CLK  6

// globals
float force_data;
int signal_data;
int freq = 500; // data collection frequency (ms)
bool label = true;

void setup() {
  // delay long enough to let me clear the serial monitor and start the python script
  delay(5000);
  Serial.begin(9600);
  // Serial.println("HX711 scale demo");

  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

}

void loop() {
  // print column headers
  while(label){
    Serial.print("Force (kgs)");
    Serial.print(",");
    Serial.println("Input Signal");
    label = false;
  }

  // print load cell data
  force_data = scale.get_units();  // float
  signal_data = 1;
  Serial.print(force_data, 4);
  Serial.print(",");
  Serial.println(signal_data, 4);

  // Serial.println();

  delay(freq);
}
