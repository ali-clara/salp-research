// globals
int led0 = 11;
int led1 = 12;
int led2 = 13;

long start_time = 10 * 1000; // (ms)
long pulse_length = 20 * 1000;  // how long each LED is on or off (ms)
long phase_shift = 5 * 1000; // delay between LEDs (ms)

int start0 = 0, start1 = 0, start2 = 0;
int finished_startup = 0;

void setup() {
  // set up signal pins
  digitalWrite(led0, LOW);
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  pinMode(led0, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);

  // delay long enough to let me clear the serial monitor and start the python script
  delay(5000);

  // set up serial communication and print column headers
  Serial.begin(9600);
  // Serial.println("HX711 scale demo");
  Serial.print("Pin 1");
  Serial.print(",");
  Serial.println("Pin 2");

}

unsigned long previous_time_led0 = millis();
unsigned long previous_time_led1 = millis();
unsigned long previous_time_led2 = millis();

void loop() {

  unsigned long current_time = millis();
  // start the LEDs offset from each other, where
    // time_interval_led1 = phase_shift
    // time_interval_led2 = 2*phase_shift

  if (finished_startup == 0){
    // led0
    if (start0 == 0){
      if (current_time - previous_time_led0 > start_time){
        previous_time_led0 = current_time;
        digitalWrite(led0, HIGH);
        start0 = 1;
      }
    }
      
    // led1
    else if (start1 == 0){
      if ((current_time - previous_time_led1) > (start_time + phase_shift)){
        previous_time_led1 = current_time;
        digitalWrite(led1, HIGH);
        start1 = 1;
      }
    }
      
    // led2
    else{
      if ((current_time - previous_time_led2) > (start_time + 2*phase_shift)){
        previous_time_led2 = current_time;
        digitalWrite(led2, HIGH);
        finished_startup = 1;
      }
    }
  }
      
  else{
  // do the normal thing

    // if it's time to change the state of LED0
    if (current_time - previous_time_led0 > pulse_length){
      // update the previous time increment for led0
      previous_time_led0 = current_time;
      change_led(led0);
      }

    // if it's time to change the state of LED1
    if (current_time - previous_time_led1 > pulse_length){
      // update the previous time increment for led0
      previous_time_led1 = current_time;
      change_led(led1);
      }

    // if it's time to change the state of LED2
    if (current_time - previous_time_led2 > pulse_length){
      // update the previous time increment for led0
      previous_time_led2 = current_time;
      change_led(led2);
      }
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
