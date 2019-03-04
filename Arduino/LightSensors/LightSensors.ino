#include <Wire.h>
#include <QTRSensors.h>

#define i2cAddress 0x10

#define TIMEOUT       2500  // waits for 2500 microseconds for sensor outputs to go low
#define EMITTER_PIN   255     // emitter is controlled by digital pin 2

unsigned int position;

//unsigned int CalibratedMinVals[] = {736, 124, 8, 124, 124, 8, 8, 124, 124, 124, 124, 368, 368, 124, 244, 124, 124, 124, 128, 240, 124, 360, 360};
//unsigned int CalibratedMaxVals[] = {2500, 2500, 240, 360, 604, 240, 240, 1468, 2500, 2500, 728, 2500, 2500, 608, 2500, 364, 484, 244, 364, 484, 244, 2500, 2500};
unsigned int CalibratedMinVals[] = {2500, 248, 8, 124, 124, 8, 8, 124, 248, 248, 248, 508, 1028, 248, 376, 124, 124, 124, 124, 244, 124, 376, 500}; 
unsigned int CalibratedMaxVals[] = {2500, 2500, 236, 360, 600, 236, 236, 852, 2500, 1348, 600, 2500, 2500, 600, 2500, 360, 472, 240, 360, 476, 240, 2500, 2500}; 


/*
 *  Ardunio Mega pinout
 *  Digital IO: 22-53
 *  Analog in: A0-A15
 *  Analog/PWM out OR Digital IO: 2-13, 44, 45, 46
*/

#define numSensors 23

//note:per documentation, each strip must be its own object. Therefore, we can only have a max of 16
//sensors on a single light sensor object


QTRSensorsRC lightSensors((unsigned char[]){22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44}, numSensors, TIMEOUT, EMITTER_PIN);



unsigned int sensorValues[numSensors];

void setup() {
  position = 0;

  Wire.begin(i2cAddress);
  Wire.onRequest(sendData);
  Serial.begin(9600);
  delay(500);
  pinMode(13, OUTPUT);

//  manualCalibrate(); 

  autoCalibrate(CalibratedMaxVals, CalibratedMinVals);

  Serial.println();
  delay(1000);
}

void loop() {
  // read calibrated sensor values and obtain a measure of the line position from 0 to 15000
  position = lightSensors.readLine(sensorValues, QTR_EMITTERS_ON, true);

  // print the sensor values as numbers from 0 to 1000, where 0 means maximum reflectance and
  // 1000 means minimum reflectance, followed by the line position
    for (unsigned char i = 0; i < numSensors; i++)
  {
    Serial.print(sensorValues[i]);
    Serial.print('\t');
  }
  Serial.println();
  Serial.println(position); // comment this line out if you are using raw values

  delay(250);
}

void sendData()
{
//  The Arduino code takes the sensor read values and finds the sensor in the middle.
//  We can then return a 6 bit number (0-63) that will indicate this centered position.

  unsigned char centerSensor = position/1000;

//  127 will be our "not found" value
  if(centerSensor == 0 || centerSensor == numSensors-1) centerSensor = 127;
  Wire.write(centerSensor);
}

void manualCalibrate()
{
  digitalWrite(13, HIGH);    // turn on Arduino's LED to indicate we are in calibration mode
  for (int i = 0; i < 400; i++)  // make the calibration take about 10 seconds
  {
    lightSensors.calibrate();
  }
  digitalWrite(13, LOW);     // turn off Arduino's LED to indicate we are through with calibration

  // print the calibration minimum values measured when emitters were on
    for (int i = 0; i < numSensors; i++)
  {
    Serial.print(lightSensors.calibratedMinimumOn[i]);
    Serial.print(' ');
  }
  Serial.println();

  // print the calibration maximum values measured when emitters were on
    for (int i = 0; i < numSensors; i++)
  {
    Serial.print(lightSensors.calibratedMaximumOn[i]);
    Serial.print(' ');
  }
  Serial.println();
}

void autoCalibrate(unsigned int *maxValsList, unsigned int *minValsList)
{
  lightSensors.calibratePreset(maxValsList, minValsList);

  // print the calibration minimum values measured when emitters were on
    for (int i = 0; i < numSensors; i++)
  {
    Serial.print(lightSensors.calibratedMinimumOn[i]);
    Serial.print(' ');
  }
  Serial.println();

  // print the calibration maximum values measured when emitters were on
    for (int i = 0; i < numSensors; i++)
  {
    Serial.print(lightSensors.calibratedMaximumOn[i]);
    Serial.print(' ');
  }
  Serial.println();
}
