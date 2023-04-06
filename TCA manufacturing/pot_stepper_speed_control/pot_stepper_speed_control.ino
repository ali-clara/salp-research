
/*
   Uno sketch to drive a stepper motor using the AccelStepper library.
   Function runSpeed() is used to run the motor at constant speed. A pot is read to vary the speed.
   Works with a ULN-2003 unipolar stepper driver, or a bipolar, constant voltage motor driver
   such as the L298 or TB6612, or a step/direction constant current driver like the a4988.
   A potentiometer is connected to analog input 0 and to gnd and 5v.

 The motor will rotate one direction. The higher the potentiometer value,
 the faster the motor speed. Because setSpeed() sets the delay between steps,
 you may notice the motor is less responsive to changes in the sensor value at
 low speeds.

 Created 30 Nov. 2009
 Modified 28 Oct 2010
 by Tom Igoe
 12/26/21  Modified to use AccelStepper.  --jkl

 */
// Include the AccelStepper Library
#include <AccelStepper.h>
#include <elapsedMillis.h>

// Motor Connections (constant current, step/direction bipolar motor driver)
const int dirPin = 3;
const int stepPin = 2;

// Sensor Connections
const int potPin = A0;
const int buttonPin = 8;

// Creates an instance
AccelStepper myStepper(AccelStepper::DRIVER, stepPin, dirPin);  // works for a4988 (Bipolar, constant current, step/direction driver)

elapsedMillis printTime;

const int steps_per_rev = 200;
const int maxSpeedLimit = 1000.0;  // set this to the maximum speed you want to use.
int buttonPressed = 0;
int start_pos;

void setup() {
  Serial.begin(115200);
  // set the maximum speed and initial speed.
  myStepper.setMaxSpeed(maxSpeedLimit);
  myStepper.setSpeed(maxSpeedLimit / 5.0);  // initial speed target

  start_pos = myStepper.currentPosition();
  Serial.print("Revolutions: ");
}

void loop() {

  while (buttonPressed == 0) {
    float mSpeed;

    // if (printTime >= 1000) {    // print every second
    //   printTime = 0;
    //   mSpeed = myStepper.speed();
    //   Serial.print(mSpeed);
    //   Serial.print("  ");
    //   Serial.println(myStepper.currentPosition());
    // }

    // read the sensor value:
    int sensorReading = analogRead(potPin);
    // map it to a the maximum speed range
    int motorSpeed = map(sensorReading, 0, 1023, 5, maxSpeedLimit);
    // set the motor speed:
    if (motorSpeed > 0) {
      myStepper.setSpeed((float)motorSpeed);
    }
    myStepper.runSpeed();
    // steps_taken = steps_taken + 1 ;

    if (digitalRead(buttonPin) == HIGH) {
      buttonPressed = 1;
    }
  }

  myStepper.stop();
  myStepper.run();

  Serial.print((myStepper.currentPosition() - start_pos) / steps_per_rev);

  exit(0);
}

// longer mandrel = negative rotation
