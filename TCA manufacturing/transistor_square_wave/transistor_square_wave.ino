int pulse_length = 10 * 1000; // ms
int output_pin = 12;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(output_pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(output_pin, HIGH);
  Serial.println("high");
  delay(pulse_length);
  digitalWrite(output_pin, LOW);
  Serial.println("low");
  delay(pulse_length);
}
