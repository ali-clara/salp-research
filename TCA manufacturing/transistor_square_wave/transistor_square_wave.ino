#include <stdbool.h>

int pulse_length = 20 * 1000; // ms
int output_pin = 12;

bool analog_flag = false;

void setup() {
  Serial.begin(9600);
  pinMode(output_pin, OUTPUT);
}

void loop() {
  // run a square wave pulse using either a digital or PWM 'analog' output depending on the flag
  if (analog_flag == false){
    digitalWrite(output_pin, HIGH);
    Serial.println("high");
    delay(pulse_length);
    digitalWrite(output_pin, LOW);
    Serial.println("low");
    delay(pulse_length);
  }

  else if (analog_flag == true){
    analogWrite(output_pin, 155); // should be 3V
    Serial.println("high");
    delay(pulse_length);
    analogWrite(output_pin, 0);
    Serial.println("low");
    delay(pulse_length);
  }
}
