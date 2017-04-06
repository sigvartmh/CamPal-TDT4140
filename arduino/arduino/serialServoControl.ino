#include <Arduino.h>

#include <Servo.h>

#define SERVO_X_PIN 5

#define ENABLE_UNIT_TEST //Uncomment to enable unit test

Servo servoX;

int pos = 0;

void setup() {
  Serial.begin(9600);

  #ifndef ENABLE_UNIT_TEST
  servoX.attach(SERVO_X_PIN);
  servoX.write(90); //center camera
  #else
  Serial.println("\nUnit test enabled");
  #endif
}

void loop() {
  //Serial.print("Pos: ");
  //Serial.println(pos);
  if (pos > 170) {
    pos = 170;
  }
  if (pos < 12) {
    pos = 12;
  }
  #ifndef ENABLE_UNIT_TEST
  servoX.write(pos);
  #else
  Serial.print("Current position: ");
  Serial.println(pos);
  delay(500);
  #endif
}

void serialEvent() {
  pos = Serial.parseInt();
}
