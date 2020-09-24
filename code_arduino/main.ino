
#include <SoftwareSerial.h>
#define nut 4
#define vo 5
#define nghieng 6

int randNumber;

SoftwareSerial mySerial(2, 3); //TX, RX

void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);
  pinMode(nut, INPUT_PULLUP);
  pinMode(vo, INPUT_PULLUP);
  pinMode(nghieng, INPUT_PULLUP);
  // cảm biến rung
  pinMode(A0, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  delay(1);
}

void loop() {
  def_nut();
  def_rung();
  def_nghieng();
  def_vo();
}


void def_nut() {
  if (digitalRead(nut) != 0) {
   mySerial.print("1");
   delay(1000);
  }
  else {
    mySerial.print("a"); 
    delay(100);
  }
}

void def_vo() {

  if (digitalRead(vo) == 0) {
    mySerial.print("1");
    delay(1000);
  }
  else {
    mySerial.print("a"); 
    delay(1000);
  }
}

void def_nghieng() {
  if (digitalRead(nghieng) == 0) {
    mySerial.print("1");
    delay(1000);
  }
  else {
    mySerial.print("a"); 
    delay(1000);
  }
}

void def_rung() {
  if (digitalRead(A0) == HIGH) {
    digitalWrite(13, HIGH);
    mySerial.print("1");
    delay(1000);
  }
  else {
    mySerial.print("a"); 
    delay(1000);
  }
}
