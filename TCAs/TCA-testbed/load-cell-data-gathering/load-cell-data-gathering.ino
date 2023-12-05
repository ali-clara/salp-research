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
#define calibration_factor 13400 //This value is obtained using the SparkFun_HX711_Calibration sketch
#define DOUT  10
#define CLK  9

// globals
int signal_pin = 12;

float force_data;
int signal_data;

long time_interval_signal = 30 * 1000;  // pulse frequency (ms)
long time_interval_load = 0.2 * 1000; // data collection frequency (ms)
unsigned long previous_time_signal = millis();
unsigned long previous_time_load = millis();

void setup() {
  // set up signal pin
  digitalWrite(signal_pin, LOW);
  pinMode(signal_pin, OUTPUT);
  signal_data = 0;

  // set up load cell
  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); //Assuming there is no weight on the scale at start up, reset the scale to 0

  // delay long enough to let me clear the serial monitor and start the python script
  delay(5000);

  // set up serial communication and print column headers
  Serial.begin(9600);
  // Serial.println("HX711 scale demo");
  Serial.print("Force (g)");
  Serial.print(",");
  Serial.println("Input Signal");
}

void loop() {

  unsigned long current_time = millis();

  // change signal data every square wave interval (currently 10 sec)
  if (current_time - previous_time_signal > time_interval_signal){
    // update the previous time increment
    previous_time_signal = current_time;

    if (digitalRead(signal_pin) == HIGH){
      digitalWrite(signal_pin, LOW);
      signal_data = 0;
    }
    else{
      digitalWrite(signal_pin, HIGH);
      signal_data = 1;
    }
  }

  // get load cell data and print every 500ms
  if (current_time - previous_time_load > time_interval_load){
    // update the previous time increment
    previous_time_load = current_time;
    
    force_data = scale.get_units();  // float
    Serial.print(force_data, 4);
    Serial.print(",");
    Serial.println(signal_data);
  }

}
