// Include the AccelStepper Library
#include <AccelStepper.h>

// Motor Connections (constant current, step/direction bipolar motor driver)
const int dirPin = 3;
const int stepPin = 2;

// Creates an instance
AccelStepper myStepper(AccelStepper::DRIVER, stepPin, dirPin);  // works for a4988 (Bipolar, constant current, step/direction driver)

const int steps_per_rev = 200;
float length;
int twists_per_m;
long goal_pos;

void setup() {
  // Serial.begin(9600);
  
  // calculate goal position
  length = 1.0;    // meters -- CHANGE BASED ON THREAD LENGTH
  twists_per_m = 700;
  goal_pos = length*twists_per_m*steps_per_rev;

  myStepper.setMaxSpeed(1000.0);
  myStepper.setAcceleration(50.0); // larger accelerations can lead to skipped steps
  myStepper.moveTo(goal_pos);

  delay(5000); // 5 sec delay
}

void loop(){

  myStepper.run();
  if (myStepper.distanceToGo() == 0) {   // run() returns true as long as the final position has not been reached and speed is not 0.
    myStepper.stop();
  }

}

