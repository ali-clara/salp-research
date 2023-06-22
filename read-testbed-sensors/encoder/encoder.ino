/* Adapted from Encoder Library - TwoKnobs Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>
#include <math.h>

// Change these pin numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder enc(2, 3);
//   avoid using pins with LEDs attached

long positionEnc  = -999;

void setup() {
  Serial.begin(9600);
  Serial.println("Encoder Test:");
}

void loop() {
  long newEnc;
  float rev;
  float dist;

  newEnc = enc.read();
  rev = pulse_to_rev(newEnc);
  dist = rev_to_dist(rev);

  if (newEnc != positionEnc) {

    Serial.print("Pulses = ");
    Serial.print(newEnc);
    Serial.print(", Revolutions = ");
    Serial.print(rev);
    Serial.print(", Distance (mm) = ");
    Serial.print(dist);
    Serial.println();
    positionEnc = newEnc;
  }
  // if a character is sent from the serial monitor,
  // reset both back to zero.
  if (Serial.available()) {
    Serial.read();
    Serial.println("Reset to zero");
    enc.write(0);
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