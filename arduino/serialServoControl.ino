#include <Servo.h>

#define SERVO_X_PIN 5

Servo servoX;

int pos = 0;

void setup() {
  Serial.begin(9600);
  servoX.attach(SERVO_X_PIN);
  servoX.write(90); //center camera
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
  servoX.write(pos);
}

void serialEvent() {
  pos = Serial.parseInt();
}

