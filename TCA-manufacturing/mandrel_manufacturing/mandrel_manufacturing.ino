
/*
   Uno sketch to drive a stepper motor using the AccelStepper library.
   Function runSpeed() is used to run the motor at constant speed.
   Works with a ULN-2003 unipolar stepper driver, or a bipolar, constant voltage motor driver
   such as the L298 or TB6612, or a step/direction constant current driver like the a4988.

 Created 30 Nov. 2009
 Modified 28 Oct 2010
 by Tom Igoe
 12/26/21  Modified to use AccelStepper.  --jkl

 */
// Include the AccelStepper Library
#include <AccelStepper.h>
#include <elapsedMillis.h>
#include <string.h>

// Motor Connections (constant current, step/direction bipolar motor driver)
// right stepper motor pins
const int stepPinR = 46;
const int dirPinR = 47;
// left stepper motor pins
const int stepPinL = 48;
const int dirPinL = 49;
// lead screw motor pins
const int stepPinS = 50;
const int dirPinS = 51;

// Creates an instance
// works for a4988 (Bipolar, constant current, step/direction driver)
AccelStepper rightStepper(AccelStepper::DRIVER, stepPinR, dirPinR);  
AccelStepper leftStepper(AccelStepper::DRIVER, stepPinL, dirPinL);
AccelStepper screwStepper(AccelStepper::DRIVER, stepPinS, dirPinS);

elapsedMillis printTime;

const int steps_per_rev = 200;
// const int maxSpeedLimit = 1500.0;  // set this to the maximum speed you want to use.

const int travelerSpeed = 125.0;
const int mandrelSpeed = 926.7;

String direction = "right";

int start_pos;

void setup() {
  Serial.begin(115200);
  // set the maximum speed and initial speed.
  rightStepper.setMaxSpeed(mandrelSpeed);
  leftStepper.setMaxSpeed(mandrelSpeed);
  screwStepper.setMaxSpeed(travelerSpeed);

  if (direction == "right"){
      Serial.print("initialize right");
      rightStepper.setSpeed(-(float)mandrelSpeed);
      leftStepper.setSpeed((float)mandrelSpeed);
      screwStepper.setSpeed(-(float)travelerSpeed);
    }

  else if (direction == "left"){
      Serial.print("initialize left");
      rightStepper.setSpeed((float)mandrelSpeed);
      leftStepper.setSpeed(-(float)mandrelSpeed);
      screwStepper.setSpeed((float)travelerSpeed);      
    }
    
  start_pos = rightStepper.currentPosition();
  // Serial.print("Revolutions: ");
}

void loop() {

    if (direction == "right"){
      rightStepper.setSpeed(-(float)mandrelSpeed);
      leftStepper.setSpeed((float)mandrelSpeed);
      screwStepper.setSpeed(-(float)travelerSpeed);
    }

    else if (direction == "left"){
      rightStepper.setSpeed((float)mandrelSpeed);
      leftStepper.setSpeed(-(float)mandrelSpeed);
      screwStepper.setSpeed((float)travelerSpeed);      
    }
    
    rightStepper.runSpeed();
    leftStepper.runSpeed();
    screwStepper.runSpeed();
  
  // if some stop configuration 

  // myStepper.stop();
  // myStepper.run();

  // Serial.print((myStepper.currentPosition() - start_pos) / steps_per_rev);

  // exit(0);
}
