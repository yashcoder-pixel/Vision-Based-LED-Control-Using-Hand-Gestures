
const int ledPins[] = {3, 4, 5, 6, 7};
const int NUM_LEDS = 5;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
}

void loop() {
  if (Serial.available() >= 5) {
    char states[5];
    bool valid = true;

    for (int i = 0; i < 5; i++) {
      states[i] = Serial.read();

      if (states[i] != '0' && states[i] != '1') {
        valid = false;
      }
    }

    if (valid) {
      for (int i = 0; i < NUM_LEDS; i++) {
        digitalWrite(ledPins[i],
                     states[i] == '1' ? HIGH : LOW);
      }
    }
  }
}
