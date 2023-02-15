int pulse_length = 1000; // ms
int output_pin = 12;

void setup() {
  // put your setup code here, to run once:
  pinMode(output_pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(output_pin, HIGH);
  delay(pulse_length);
  digitalWrite(output_pin, LOW);
  delay(pulse_length);
}
