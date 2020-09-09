#include <Thing.h>

//Definir constantes
//Pin 1 en TXD0 - GPIO-1 -- Led
#define LED_STATUS 1
//Pin 0 en D3 - GPIO-0 --  DHT21 temp y hum 
#define DHT_PIN 0
//Pin 3 en Rx - GPIO-3  -- Temperature DS18B20
#define TEMP_PIN 3
//Pin 2 en D4 - GPIO-2  -- CE NRF24L01
#define CE_PIN 2
//Pin 15 en D8 - GPIO-15 -- CSN NRF24L01
#define CSN_PIN 15
//ID NODE
#define ID_NODE 02

Thing thing(LED_STATUS, DHT_PIN, TEMP_PIN, CE_PIN, CSN_PIN, ID_NODE);

unsigned long lastSent;
volatile bool statusData = false;
volatile bool okData = false;
int nodeId = 200;
uint8_t addressSense[8] = {0x28, 0xF6, 0xEA, 0x79, 0x97, 0x10, 0x03, 0xDE};

void setup() {
  }

void loop() {

    //LED
    for(int i=0;i<10;i++){
       thing.ledInd(250);
    }
    thing.ledOff();
    
    while(!okData){
      //TEMPERATURE AIR
      float at = thing.getAirTemp();
      //HUMIDITY AIR
      float ah = thing.getAirHum();
      //TEMPERATURE AIR SENSATION
      float ats = thing.getAirTempIndex(at, ah);
      //TEMPERATURE EARTH
      float et = thing.getEarthTemp(addressSense);
      //HUMIDITY EARTH
      float eh = thing.getEarthHum();
      //LIGHT
      float lux = thing.getLight(true);
      okData = ( isnan(at) || isnan(ah) || isnan(ats) || isnan(et) || isnan(eh) || isnan(lux)) ? false : true;
    }
    
    
    
    //SEND DATA NRF24L01
    statusData = false;
    do{
      thing.ledOn();
      unsigned long stateTime = millis();
      if ( stateTime - lastSent >= 2000){
          lastSent = stateTime;
          thing.sendData(nodeId, ats, ats, at, ah, et, eh, lux);
          delay(2000);
          statusData = thing.sendData(nodeId, ats, ats, at, ah, et, eh, lux);
      } 
    }while(statusData == false); 

    //GOTO SLEEP
    if(statusData == true){
       for(int i=0;i<5;i++){
          thing.ledInd(250);
       }
       thing.ledOff();
       //SLEEP THING
       //const uint64_t timeToSleep = 36.5e8;
       thing.gotoSleep(36.5e8); 
    }else{
       for(int i=0;i<5;i++){
          thing.ledInd(1000);
       }
       thing.ledOff();
    }
}
