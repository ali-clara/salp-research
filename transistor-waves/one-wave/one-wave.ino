// globals
int led0 = 13;
int led1 = 12;
int led2 = 11;
int led3 = 10;
int led4 = 9;

long start_time = 5 * 1000; // (ms)
long pulse_length = 15 * 1000;  // how long each LED is on or off (ms)
long phase_shift = 10 * 1000; // delay between LEDs (ms)

int start0 = 0, start1 = 0, start2 = 0, start3 = 0, start4 = 0;
int finished_startup = 0;

void setup() {
  // set up signal pins
  digitalWrite(led0, LOW);
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  digitalWrite(led4, LOW);

  pinMode(led0, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);

  // delay long enough to let me clear the serial monitor and start the python script
  // delay(5000);

  // set up serial communication and print column headers
  // Serial.begin(9600);
  // Serial.print("Pin 1");
  // Serial.print(",");
  // Serial.println("Pin 2");

}

unsigned long previous_time_led0 = millis();
unsigned long previous_time_led1 = millis();
unsigned long previous_time_led2 = millis();
unsigned long previous_time_led3 = millis();
unsigned long previous_time_led4 = millis();

void loop() {

  unsigned long current_time = millis();
  // start the LEDs offset from each other, where
    // time_interval_led1 = phase_shift
    // time_interval_led2 = 2*phase_shift

    // led0
    if (start0 == 0){
      if (current_time - previous_time_led0 > start_time){
        previous_time_led0 = current_time;
        digitalWrite(led0, HIGH);
        start0 = 1;
      }
    }
    else if (current_time - previous_time_led0 > pulse_length){
      // update the previous time increment for led0
      previous_time_led0 = current_time;
      digitalWrite(led0, LOW);
      }

    // led1
    if (start1 == 0){
      if ((current_time - previous_time_led1) > (start_time + phase_shift)){
        previous_time_led1 = current_time;
        digitalWrite(led1, HIGH);
        start1 = 1;
      }
    }
    // if it's time to change the state of LED1
    else if (current_time - previous_time_led1 > pulse_length){
      // update the previous time increment for led1
      previous_time_led1 = current_time;
      digitalWrite(led1, LOW);
      }

    // led2
    if (start2 == 0){
      if ((current_time - previous_time_led2) > (start_time + 2*phase_shift)){
        previous_time_led2 = current_time;
        digitalWrite(led2, HIGH);
        start2 = 1;
      }
    }
     // if it's time to change the state of LED2
    else if (current_time - previous_time_led2 > pulse_length){
      // update the previous time increment for led2
      previous_time_led2 = current_time;
      digitalWrite(led2, LOW);
      }

    // led3
    if (start3 == 0){
      if ((current_time - previous_time_led3) > (start_time + 3*phase_shift)){
        previous_time_led3 = current_time;
        digitalWrite(led3, HIGH);
        start3 = 1;
      }
    }
    // if it's time to change the state of LED3
    else if (current_time - previous_time_led3 > pulse_length){
      // update the previous time increment for led0
      previous_time_led3 = current_time;
      digitalWrite(led3, LOW);
      }

    // led4
    if (start4 == 0){
      if ((current_time - previous_time_led4) > (start_time + 4*phase_shift)){
        previous_time_led4 = current_time;
        digitalWrite(led4, HIGH);
        start4 = 1;
      }
    }
    // if it's time to change the state of LED4
    else if (current_time - previous_time_led4 > pulse_length){
      // update the previous time increment for led0
      previous_time_led4 = current_time;
      digitalWrite(led4, LOW);
    } 
}

void change_led(int led_pin) {
  // either turn on or off led accordingly
    if (digitalRead(led_pin) == HIGH){
      digitalWrite(led_pin, LOW);
    }
    else{
      digitalWrite(led_pin, HIGH);
    }
}
