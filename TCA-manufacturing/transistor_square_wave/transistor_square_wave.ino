#include <stdbool.h>

int start_delay = 10 * 1000; // ms
int pulse_length = 30 * 1000; // ms
int output_pin = 6;
int finished_startup = 0;

bool analog_flag = false;

void setup() {
  Serial.begin(9600);
  digitalWrite(output_pin, LOW);
  pinMode(output_pin, OUTPUT);
}

void loop() {
  // run a square wave pulse using either a digital or PWM 'analog' output depending on the flag
  if (analog_flag == false){
    if (finished_startup == 0){
      delay(start_delay);
      finished_startup = 1;
    }
    digitalWrite(output_pin, HIGH);
    Serial.println("high");
    delay(pulse_length);

    digitalWrite(output_pin, LOW);
    Serial.println("low");
    delay(pulse_length);
  }

  else if (analog_flag == true){
    analogWrite(output_pin, 81); // should be 3V
    Serial.println("high");
    delay(pulse_length);
    analogWrite(output_pin, 0);
    Serial.println("low");
    delay(pulse_length);
  }
}
