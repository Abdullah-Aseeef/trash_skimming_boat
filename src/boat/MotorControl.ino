#include <Wire.h>
#include <LiquidCrystal.h>
#include <Servo.h>
// Set the LCD I2C address to 0x27 or 0x3F depending on your module
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

Servo ESC_B;
Servo ESC_A;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2); 
  ESC_A.attach(8);
  ESC_B.attach(9);
  delay(4000);
  // lcd.setCursor(0, 0);
  lcd.print("Arduino Ready");
  ESC_A.writeMicroseconds(1550); // 1500 means motor is stopped. 1900 is full speed forward. 1100 is full speed backward.
  ESC_B.writeMicroseconds(1550);
  delay(4000);

  lcd.print("Ready to receive commands: F (forward), L (left), R (right)");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Received: ");
    lcd.print(command);

    lcd.setCursor(0, 1);
    if (command == 'L') 
    {
      lcd.print("left");
      ESC_A.writeMicroseconds(1300); //left motor back
      ESC_B.writeMicroseconds(1700); //right motor forward
    } 

    else if (command == 'F') 
    {
      lcd.print("forward");
      ESC_A.writeMicroseconds(1700); //both motors forward
      ESC_B.writeMicroseconds(1700);
    } 

    else if (command == 'R')
    {
      lcd.print("left");
      ESC_A.writeMicroseconds(1700); //left motor forward
      ESC_B.writeMicroseconds(1300); //right motor back
    } 

    else 
    {
      lcd.print("Unknown Cmd");
    }
  }

  else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("No Data Avail");
    ESC_A.writeMicroseconds(1500);
    ESC_B.writeMicroseconds(1500); // stop motors if no command.
  }

  delay(1000);
}
