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
/*#define ID_NODE 01
int nodeId = 201;
uint8_t addressSense[8] = {0x28, 0xF6, 0xEA, 0x79, 0x97, 0x10, 0x03, 0xDE}; //-- 7 - K -- Nodo 1 - ID_NODE 01 - nodeId = 201
*/

/*#define ID_NODE 02
int nodeId = 202;
uint8_t addressSense[8] = {0x28, 0x6A, 0x44, 0x79, 0x97, 0x10, 0x03, 0x83}; //-- 2 - B -- Nodo 2 - ID_NODE 02 - nodeId = 202
*/

/*#define ID_NODE 03
int nodeId = 203;
uint8_t addressSense[8] = {0x28, 0x20, 0xAE, 0x79, 0x97, 0x10, 0x03, 0x5E}; //-- 9 - I -- Nodo 3 - ID_NODE 03 - nodeId = 203
*/

/*#define ID_NODE 04
int nodeId = 204;
uint8_t addressSense[8] = {0x28, 0x99, 0x71, 0x79, 0x97, 0x10, 0x03, 0xFE}; //-- 6 - F -- Nodo 4 - ID_NODE 04 - nodeId = 204
*/

#define ID_NODE 05
int nodeId = 205;
uint8_t addressSense[8] = {0x28, 0xAA, 0x8C, 0x79, 0x97, 0x10, 0x03, 0x00}; //-- 3 - C -- Nodo 5 - ID_NODE 05 - nodeId = 205





Thing thing(LED_STATUS, DHT_PIN, TEMP_PIN, CE_PIN, CSN_PIN, ID_NODE);

volatile unsigned long lastSent;
volatile bool statusData = false;
volatile bool okData = false;




void setup() {
}

void loop() {

    //LED
    for(int i=0;i<15;i++){
       thing.ledInd(300);
    }
    thing.ledOff();

    float at, ah, ats, et, eh, lux;
    
    while(!okData){
      //TEMPERATURE AIR
      at = thing.getAirTemp();
      //HUMIDITY AIR
      ah = thing.getAirHum();
      //TEMPERATURE AIR SENSATION
      ats = thing.getAirTempIndex(at, ah);
      //TEMPERATURE EARTH
      et = thing.getEarthTemp(addressSense);
      //HUMIDITY EARTH
      //Nodo Uno
      //eh = thing.getEarthHum(0, -0.005799791, 9000);
      //Nodo Dos 
      //eh = thing.getEarthHum(0, -0.005790388, 9000);
      //Nodo Tres
      //eh = thing.getEarthHum(0, -0.005907023, 9000);
      //Nodo Cuatro
      //eh = thing.getEarthHum(0, -0.005770008, 9000);
      //Nodo Cinco
      eh = thing.getEarthHum(0, -0.005795758, 9000);
      //LIGHT
      lux = thing.getLight(true);
      okData = ( isnan(at) || isnan(ah) || isnan(ats) || isnan(et) || isnan(eh) || isnan(lux)) ? false : true;
    }
    
    
    
    //SEND DATA NRF24L01
    statusData = false;
    do{
      thing.ledOn();
      unsigned long stateTime = millis();
      if ( stateTime - lastSent >= 2000){
          lastSent = stateTime;
          delay(1500);
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
        //thing.gotoSleep(120e6);

        //Nodo Uno
        //thing.gotoSleep(18.00e8);
        //Nodo Dos
        //thing.gotoSleep(18.12e8);
        //Nodo Tres
        //thing.gotoSleep(18.24e8);
        //Nodo Cuatro
        //thing.gotoSleep(18.36e8);
        //Nodo Cinco
        thing.gotoSleep(18.48e8);
        
    }else{
       for(int i=0;i<5;i++){
          thing.ledInd(1000);
       }
       thing.ledOff();
    }
}
