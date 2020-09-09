/*
  Thing.h - Library for capture environment variables Data and send to Gateway for Iot solutions in Agro.
  Created by Nicolás P. Anzola, September 1, 2020.
  License: MIT
*/
#ifndef Thing_h
#define Thing_h

#include "Arduino.h"
#include "DHT.h"
#include <BH1750.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>

class Thing
{
  public:
    Thing(byte ledPin, int dhtPin, int tempPin, byte cePin, byte csnPin, const uint16_t idNode);
    void ledInd(unsigned int delayLed = 250);
    void ledOff();
    void ledOn();
    float getAirTemp();
    float getAirHum();
    float getAirTempIndex(float t, float h);
    float getEarthTemp(DeviceAddress deviceAddress);
    float getEarthHum(byte idAdc = 0, float pending = -0.005973002, float rBytes = 9500);
    float getLight(bool isCalibrate = false);
    void calibrateLight(float lux);
    float getPercent(float x, float in_min, float in_max, float out_min, float out_max);
    float getAdc(byte idAdc = 0);
    void gotoSleep(uint64_t timeToSleep = 15e6);
    bool sendData(int nodeId = 201, float ats = 10.55, float ahs = 15.55, float at = 20.55, float ah = 25.55, float et = 30.55, float eh = 35.55, float li = 2000.55);
    struct payloadNode {           
        int nodeId;
        float aitTempSensation;
        float airHumSensastion;
        float airTemp;
        float airHum;
        float earthTemp;
        float earthHum;
        float light;
    };
  private:
    RF24 _radio;
    RF24Network _network;
    OneWire _oneWireObj;
    DallasTemperature _sensorDS18B20;
    Adafruit_ADS1115 adcDisp;
    BH1750 lightMeter;
    DHT dht;
    byte _ledPin;
};
#endif
