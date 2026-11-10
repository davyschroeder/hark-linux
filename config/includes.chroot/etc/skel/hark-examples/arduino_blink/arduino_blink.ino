// Arduino Uno/Nano blink
// arduino-cli compile -b arduino:avr:uno . && arduino-cli upload -b arduino:avr:uno -p /dev/ttyACM0 .
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
