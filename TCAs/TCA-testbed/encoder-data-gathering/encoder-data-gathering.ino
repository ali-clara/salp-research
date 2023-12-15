/* Adapted from Encoder Library - TwoKnobs Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>
#include <math.h>

// globals
Encoder enc(2, 3);
long positionEnc  = -999;

int signal_pin = 12;

float disp_data;
int signal_data;

long time_interval_signal = 15 * 1000;  // pulse frequency (ms)
long time_interval_enc = 0.2 * 1000; // data collection frequency (ms)
unsigned long previous_time_signal = millis();
unsigned long previous_time_enc = millis();
int temp;

void setup() {
  // set up signal pin
  digitalWrite(signal_pin, LOW);
  pinMode(signal_pin, OUTPUT);
  signal_data = 0;

  // zero encoder
  enc.write(0);

  // delay long enough to let me clear the serial monitor and start the python script
  delay(5000);

  // set up serial communication and print column headers
  Serial.begin(9600);
  Serial.print("Linear displacement (mm)");
  Serial.print(",");
  Serial.println("Time (s)");
  // Serial.println("Input Signal");
}

void loop() {

  unsigned long current_time = millis();
  long enc_data;
  float rev;
  float dist;

  // change signal data every square wave interval (currently 10 sec)
  if (current_time - previous_time_signal > time_interval_signal){
    // update the previous time increment
    previous_time_signal = current_time;

    temp = digitalRead(signal_pin);

    if (temp == 1){
      digitalWrite(signal_pin, 0);
      signal_data = 0;
    }
    else{
      digitalWrite(signal_pin, 1);
      signal_data = 1;
    }
  }

  // get encoder data and print every 500ms
  if (current_time - previous_time_enc > time_interval_enc){
    // update the previous time increment
    previous_time_enc = current_time;

    enc_data = enc.read();
    rev = pulse_to_rev(enc_data);
    dist = rev_to_dist(rev);
  
    Serial.print(dist, 4);
    Serial.print(",");
    Serial.println(current_time/1000.0);
    // Serial.println(signal_data);
  }
}

float pulse_to_rev(long pulse){
  float enc_rev;
  float encoder_resolution = 1024 * 4; // 1024 P/R, quadrature

  enc_rev = pulse / encoder_resolution; // revolutions of the encoder
  return enc_rev;
}

float rev_to_dist(float rev){
  float theta_enc;
  float r_pulley;
  float dist;

  theta_enc = rev*2*M_PI; // the angle in radians the encoder has travelled
  r_pulley = 11.6/2;  // the radius of the pulley (mm)

  dist = theta_enc*r_pulley;  // linear distance traveled by TCA
  return dist;
}