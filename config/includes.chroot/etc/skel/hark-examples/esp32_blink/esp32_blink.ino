// ESP32 blink + serial hello
// Compile:  arduino-cli compile -b esp32:esp32:esp32 .
// Upload:   arduino-cli upload -b esp32:esp32:esp32 -p /dev/ttyUSB0 .
#ifndef LED_BUILTIN
#define LED_BUILTIN 2   // most ESP32 devkits
#endif

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("Hello from Hark Linux!");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  Serial.printf("Uptime: %lu s, free heap: %u bytes\n", millis() / 1000, ESP.getFreeHeap());
}
