/*
  Thing.cpp - LLibrary for capture environment variables Data and send to Gateway for Iot solutions in Agro.
  Created by Nicolás P. Anzola, September 1, 2020.
  License: MIT
  //Released into the public domain.
*/

#include "Arduino.h"
#include "Thing.h"
#include <Wire.h>
#define DHTTYPE DHT21

//CONSTRUCTOR METHOD
Thing::Thing(byte ledPin, int dhtPin, int tempPin, byte cePin, byte csnPin, const uint16_t idNode): dht(dhtPin, DHTTYPE),lightMeter(0x23),adcDisp(0x48),_oneWireObj(tempPin),_sensorDS18B20(&_oneWireObj),_radio(cePin, csnPin),_network(_radio)
{
  //INICIAR COMUNICACION I2C
  Wire.begin();
  //COMUNICACION SPI
  SPI.begin();
  //INICIO DE NRF24L01
  _radio.begin();
  _network.begin(/*channel*/ 90, /*node address*/ idNode);  
  //ADC115
  adcDisp.setGain(GAIN_ONE); // 1x gain   +/- 4.096V  1 bit = 0.125mV //1 bit =  0.125mV  con (1x gain +/- 4.096V)
  adcDisp.begin();
  //SENSOR DE TEMPERATURA Y HUMEDAD - AIRE  
  dht.begin();
  //SENSOR DE LUZ
  lightMeter.begin(BH1750::ONE_TIME_HIGH_RES_MODE);

  //SENSOR DE TEMPERATURA DS18B20
  _sensorDS18B20.begin();
   
  //Led Indicator for status
  _ledPin = ledPin;
  pinMode(_ledPin, OUTPUT);
  
  //Métodos por default
  ledOff();
}


//LED INDICATOS METHOD
void Thing::ledInd(unsigned int delayLed)
{
  digitalWrite(_ledPin, !digitalRead(_ledPin));
  delay(delayLed);
}

//LED OFF METHOD
void Thing::ledOff()
{
  digitalWrite(_ledPin, LOW);
}

//LED OFF METHOD
void Thing::ledOn()
{
  digitalWrite(_ledPin, HIGH);
}

//TEMPERATURE FROM AIR - METHOD
float Thing::getAirTemp()
{
  //Get Temperature
  float t = dht.readTemperature();
  delay(100);
  //Validate Data
  if ( isnan(t) ) {
    return 0.0;
  }
  return t;
}

//HUMIDITY FROM AIR - METHOD
float Thing::getAirHum()
{
  //Get Humidity
  float h = dht.readHumidity();
  delay(100);
  //Validate Data
  if (isnan(h)) {
    return 0.0;
  }
  return h;
}


//TEMPERATURE INDEX FROM AIR - METHOD
float Thing::getAirTempIndex(float t, float h)
{
  //Validate Data
  if (isnan(h) || isnan(t)) {
    return 0.0;
  }
  //Index Temperature
  float hic = dht.computeHeatIndex(t, h, false);
  return hic;
}


//TEMPERATURE  FROM EARTH - METHOD
float Thing::getEarthTemp(DeviceAddress deviceAddress)
{
  //SENSOR DE TEMPERATURA DS18B20 
  _sensorDS18B20.requestTemperaturesByAddress(deviceAddress);
  float tempDs = _sensorDS18B20.getTempC(deviceAddress);
  //_sensorDS18B20.requestTemperatures();
  //float tempDs = _sensorDS18B20.getTempCByIndex(0);
  return tempDs;
}


//HUMIDITY FROM EARTH - METHOD
float Thing::getEarthHum(byte idAdc, float pending, float rBytes)
{
  float hum;
  float percent = 100;
  int cycles = 50;
  for(int i=0; i<cycles; i++){
    hum += adcDisp.readADC_SingleEnded(idAdc);
  }
  hum /= cycles; 
  //hum = (hum * 0.125)/1000; Get voltage
  //y = m(x - x0) + y0;
  //return (float)(pending*(hum - rBytes)) + percent;
  float calculate = (pending*(hum - rBytes)) + percent;
  return calculate;
}



//CALIBRATE LIGHT - METHOD
void Thing::calibrateLight(float  lux)
{
  if (lux >= 0) {
    if (lux > 40000.0) {
        // reduce measurement time - needed in direct sun light
        if (lightMeter.setMTreg(32)) {
        }
    }
    else {
        if (lux > 10.0) {
            // typical light environment
            if (lightMeter.setMTreg(69)) {
            }
        }
        else {
            if (lux <= 10.0) {
                //very low light environment
                if (lightMeter.setMTreg(138)) {
                }
            }
       }
    }
  }
}

//LIGHT - METHOD
float Thing::getLight(bool isCalibrate)
{
  float lux = 0.0;
  if(isCalibrate){
    lux = lightMeter.readLightLevel(true);
    calibrateLight(lux);
  }
  lux = lightMeter.readLightLevel(true);
  return lux;
}

//PERCENT VALUE - METHOD
float Thing::getPercent(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

//ADC INPUT A0 - METHOD
float Thing::getAdc(byte idAdc)
{
  float adcInputOne;
  adcInputOne = adcDisp.readADC_SingleEnded(idAdc);
  //return (adcInputOne * 0.125)/1000; 
  return adcInputOne;
}

//SLEEP - METHOD
void Thing::gotoSleep(uint64_t timeToSleep)
{
  //DEFAULT 15e6 --> 15 SEGUNDOS
  //1 Horas = 3.600.000.000 Microsegundos
  delay(500);  
  ESP.deepSleep(timeToSleep, WAKE_RF_DISABLED); 
}

//SEND DATA TX - METHOD
bool Thing::sendData(int nodeId, float ats, float ahs, float at, float ah, float et, float eh, float li)
{
  const uint16_t otherNode = 00;
  _network.update();
  Thing::payloadNode node;
        node.nodeId = nodeId;
        node.aitTempSensation = ats;
        node.airHumSensastion = ahs;
        node.airTemp = at;
        node.airHum = ah;
        node.earthTemp = et;
        node.earthHum = eh;
        node.light = li;
  RF24NetworkHeader header(otherNode);
  return _network.write(header,&node,sizeof(node));
}
