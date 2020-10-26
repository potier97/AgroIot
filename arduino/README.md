## BIBLIOTECA THING

Se propone dar a entender y explicar el funcionamiento de la biblioteca creada [Thing]( https://github.com/potier97/AgroIot/tree/master/arduino/Thing) para este proyecto, la cual puede ser descargada y compilada en el IDE de Arduino, de acuerdo a las siguientes recomendaciones:

1. Instalar las bibliotecas DHT, BH1750, Adafruit_ADS1015, OneWire, DallasTemperature, RF24 y RF24Network.
2. Disponer de los siguientes sensores y módulos: DHT21, YL-100 o YL-69, DS18B20, BH1750 y ADC1115.
3. Instalar el IDE de Arduino con una versión de 1.7 o superior.


El microcontrolador con el cual se desarrolló este proyecto es la [ESP8266](https://www.espressif.com/en/products/socs/esp8266) de Espressif. El ejemplo básico creado para este proyecto es el archivo o Script [SimpleNode.ino](https://github.com/potier97/AgroIot/blob/master/arduino/SimpleNode.ino), y lo vamos a explicar a continuación.


### Importando y declarando variables del ESP8266.
Se definen los pines que van a hacer utilizados para conectar los periféricos del ESP8266 con cada uno de los sensores, módulos y transceptores.

```ino
    #include <Thing.h>  
    #define LED_STATUS 1 
    #define DHT_PIN 0 
    #define TEMP_PIN 3 
    #define CE_PIN 2 
    #define CSN_PIN 15
    #define ID_NODE 05 
    uint8_t addressSense[8] = {0x28, 0xAA, 0x8C, 0x79, 0x97, 0x10, 0x03, 0x00};
```
 -  LED_STATUS: pin donde va a estar conectado un led piloto, para indicar el estado del nodo
 -  DHT_PIN: pin que va a realizar la comunicación del sensor DHT21 y el microcontrolador
 -  TEMP_PIN: pin que va a estar conectado el sensor DS18B20
 -  CE_PIN: pin que indica al transceptor si está en modalidad de esclavo o no
 -  CSN_PIN: pin encargado de la transferencia de datos para la comunicación con el transceptor y el microcontrolador
 -  ID_NODE: Id del Nodo para ser identificado en la red, cuando este se comunique con el Gateway
 -  addressSense: Dirección del sensor DS18B20 al que está conectado el microcontrolador para pedir datos de la temperatura
 

## Inizialidando modulos 

```ino
    Thing thing(LED_STATUS, DHT_PIN, TEMP_PIN, CE_PIN, CSN_PIN, ID_NODE);
    volatile unsigned long lastSent;
    volatile bool statusData = false;
    volatile bool okData = false;
```

 - thing: Declaración de una instancia llamada thing de la biblioteca Thing, importada al inicio, y con los parámetros declarados al inicio
 - lastSent: Estado para actualizar el tiempo cada dos segundos, cuando los datos no han sido enviados y reenviar el paquete de datos al Gateway
 - statusData: Validación del sistema para indicar si los datos censados ya fueron enviados
 - okData: Validación del sistema de que los sensores ya realizaron su acción

## Bucle
Para entender este proceso, se divide en 4 partes:

 - Inicialización del Led Piloto o Indicador
 - Cesado de las variables
 - Envío del paquete de datos al Gateway
 - Suspensión del módulo por 30 min

### Led Piloto

```ino 
    for(int i=0;i<15;i++){
       thing.ledInd(300);
    }
    thing.ledOff();
```

Para indicarle al usuario que el módulo está en funcionamiento, un led parpadea 15 veces en un corto periodo de tiempo antes de empezar a censar, esto se hace con el fin de indicarle al usuario que el Nodo está funcionando de nuevo, después de estar suspendido por 30 minutos o de haber realizado un reinicio al sistema. Al final, el led queda apagado.

### Censado

```ino
    float at, ah, ats, et, eh, lux;
    while(!okData){ 
      at = thing.getAirTemp(); 
      ah = thing.getAirHum(); 
      ats = thing.getAirTempIndex(at, ah); 
      et = thing.getEarthTemp(addressSense); 
      eh = thing.getEarthHum(0, -0.005795758, 9000); 
      lux = thing.getLight(true);
      okData = ( isnan(at) || isnan(ah) || isnan(ats) || isnan(et) || isnan(eh) || isnan(lux)) ? false : true;
    }
```

 Las variables declaradas al inicio corresponden a cada una de las variables ambientales censadas, que son:
 - at: Temperatura del aire
 - ah: Humedad del Aire
 - ats: Sensación térmica del aire
 - et: Temperatura de la tierra
 - eh: Humedad de la Tierra
 - lux: Intensidad de la Luz
 
Luego de ser declaradas entran a un bucle, con el fin de realizar el censado de cada uno de los sensores asignándoles el valor a cada una de las variables declaradas, para que finalmente se valide sí, los variables tienen asignados datos, si no el bucle volverá a iniciar.

### Envío de Datos

```ino  
    do{
      thing.ledOn();
      unsigned long stateTime = millis();
      if ( stateTime - lastSent >= 2000){
          lastSent = stateTime;
          delay(1500);
          statusData = thing.sendData(nodeId, ats, ats, at, ah, et, eh, lux);
      } 
    }while(statusData == false); 
```

Se ejecuta un bucle condicional, en el que hace que el led se encienda mientras se envían los datos, a la variable StatusData se le asigna el resultado del método (SENDDATA), en el que tiene como parámetros cada uno de los datos censado, finalmente este método devolverá VERDADERO cuando los datos han sido enviados, y FALSO, mientras los datos no se han podido enviar, para que finalmente el bucle evalúe si puede continua la ejecución o necesita volver a realizar el proceso.


### Suspención

```ino   
    if(statusData){
       for(int i=0;i<5;i++){
          thing.ledInd(250);
       }
       thing.ledOff();  
        thing.gotoSleep(18.48e8);
    }
```

Finalmente, el sistema evalúa si los datos fueron enviados, con el fin de poner a "Dormir" el microcontrolador por 30 minutos, esto se hace para  realizar el ahorro de energía y memoria del mismo. Por lo tanto, cuando el sistema ha enviado los datos, el Led Piloto le indicara al usuario que se enviaron los datos parpadeando 5 veces, para que luego el microcontrolador se ponga en Suspensión, pasando el parámetro de segundos, escrito en microsegundos al método de (GOTOSLEEP).
