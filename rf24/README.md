# Gateway - Captura de datos

El objetivo de este servicio es el de recibir contantemente los paquetes de datos, enviados por cada uno de los nodos y guardar los datos recibidos en una base de datos local, para este caso un archivo CSV. Para ello se realiza un Script en C++ y se utiliza la biblioteca de RF24NETWORK para su correcto funcionamiento. 


## Servicio - RF24

Antes de esto, se indica la manera de crear un servicio que se ejecute constantemente en el sistema operativo de la Raspberry Pi usando Systemd, así que es necesario crear un archivo llamada `telemetryData.service`, lo puede crear y editar con las siguientes instrucciones en la línea de comandos (SHELL): 

``` sh
    $ nano telemetryData.service
    $ sudo chmod 777 telemetryData.service
    $ sudo chmod +x telemetryData.service
```

Las dos últimas instrucciones corresponden a permisos de ejecución en el sistema. El contenido básico del archivo del servicio debe contener: 

``` sh
    [Unit]
    Description=Mi Service description
    After=multi-user.target
    
    [Service]
    Type=idle
    ExecStart=/home/pi/iot/rf24/telemetryNetwork
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=pi
    
    [Install]
    WantedBy=multi-user.target
```

 - Description: es la descripción de lo que hace este servicio
 - After: Indica que el Script asociado se debe ejecutar después de que el sistema este totalmente inicializado
 - ExecStart: Es la ruta general en la que se encuentra el Script que debe ejecutar


Luego de  tener el archivo  declarado se procede a validar el servicio.}
``` sh
    $ sudo cp telemetryData.service /etc/systemd/system/telemetryData.service

    $ sudo systemctl start telemetryData.service

    $ sudo systemctl stop telemetryData.service

    $ sudo systemctl enable telemetryData.service

    $ sudo systemctl status telemetryData.service
```

 - sudo cp telemetryData.service /etc/systemd/system/telemetryData.service: Copia el archivo creado y lo coloca en el directorio etc/systemd/system en donde se ejecutan todos los servicios y/o tareas automatizadas
 - sudo systemctl start telemetryData.service: Inicia el servicio que ha sido creado
 - sudo systemctl stop telemetryData.service: Detiene el servicio que se ha creado
 - sudo systemctl enable telemetryData.service: Arranca el servicio cada vez que la máquina se reinicia
 - sudo systemctl status telemetryData.service:  Le indica al usuario el estado de ejecución del servicio


Para saber más acerca de los servicios creados por Systemd, visite la   [documentación](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)
 
## Comunicación con red de telemetría

Como se mencionó anteriormente se creó un script denominado `telemetryNetwork`, aunque este es el que se ejecuta en la máquina, ya que es compilado por medio de [Makefile](https://github.com/potier97/AgroIot/blob/master/rf24/Makefile) y su contenido es binario, puede revisar el archivo [Makefile](https://github.com/potier97/AgroIot/blob/master/rf24/Makefile) para entender las comprobaciones que hace con las bibliotecas RF24 y RF24Network, estas son utilizadas para la comunicación en la red de telemetría. Por lo tanto, el Script que es editado se llama `telemetryNetwork.cpp`, y se describe a continuación: 

### Inicializar Módulos 

``` c++
    #include <RF24/RF24.h>
    #include <RF24Network/RF24Network.h>
    #include <iostream>
    #include <ctime>
    #include <stdio.h>
    #include <time.h>
    #include <fstream> 
    
    using namespace std;
```

Se hace el llamado a las bibliotecas RF24 y RF24NETWORK que realizan la comunicación de la red de telemetría, se llama a IOSTRIM y FSTREAM para el manejo de archivos, en este caso se utiliza un CSV, CTIME y TIME para el manejo de fechas, y se declara un puntero STD

### Declarando el protocolo de comunicación

``` c++ 
    RF24 radio(22, 0);
    RF24Network network(radio);
```

Se utilizan los pines 22 para el CE (Chip Enable), y el 0 para el CSN (Chip Select/eneable) de la Raspberry Pi. Se instancia radio de la clase RF24, y con este último se vuelve a instanciar Network de la clase RF24Network, esta es la que se utiliza para la comunicación.

### Declarando Variables y estructuras

``` c++ 
    //Data from Node 1
    float airTempSensationOne;
    float airHumSensationOne;
    float airTempOne;
    float airHumOne;
    float earthTempOne;
    float earthHumOne;
    float lightOne;
    //Data from Node 2
    float airTempSensationTwo;
    float airHumSensationTwo;
    float airTempTwo;
    float airHumTwo;
    float earthTempTwo;
    float earthHumTwo;
    float lightTwo;
    //Data from Node 3
    float airTempSensationThree;
    float airHumSensationThree;
    float airTempThree;
    float airHumThree;
    float earthTempThree;
    float earthHumThree;
    float lightThree;
    //Data from Node 4
    float airTempSensationFour;
    float airHumSensationFour;
    float airTempFour;
    float airHumFour;
    float earthTempFour;
    float earthHumFour;
    float lightFour;
    //Data from Node 5
    float airTempSensationFive;
    float airHumSensationFive;
    float airTempFive;
    float airHumFive;
    float earthTempFive;
    float earthHumFive;
    float lightFive;
    
    //Validation from New data
    bool newFromOne   = false;
    bool newFromTwo   = false;
    bool newFromThree = false;
    bool newFromFour  = false;
    bool newFromFive  = false;
    
    
    //Structure to read data
    struct nodeData {
      int nodeId;
      float airTempSensation;
      float airHumSensation;
      float airTemp;
      float airHum;
      float earthTemp;
      float earthHum;
      float light;
    };
```

Se declaran las variables de cada nodo que van a hacer recibidas, se declara variables para validar el recibido de dichos datos enviados, y finalmente se declara la estructura de datos, de lo que va a recibir el Gateway de cada nodo

### Método de Generar Fecha Actual

``` c++
   string getDate(){
        time_t ttime = time(0);
        tm* gmt_time = localtime(&ttime);
        //Date
        int day = gmt_time->tm_mday;
        int month =  1 + gmt_time->tm_mon;
        int year = 1900 + gmt_time->tm_year;
        //Hour
        int hour = gmt_time->tm_hour;
        int min = gmt_time->tm_min;
        int second =  gmt_time->tm_sec;
        string space = " ";
        string slash = "/";
        string points = ":";
        string date = to_string(day) + slash + to_string(month) + slash + to_string(year) + space + to_string(hour) + points + to_string(min) + points + to_string(second);
        return date;
    }
```

Se declara un método que devuelve un String, este contiene la fecha actual, este método es utilizado para generar la fecha de cuando se reciben todos los datos de los nodos y posteriormente son guardados en un archivo CSV.

### Método para guardar datos en Archivo CSV

``` c++ 
     void writeCSV(){ 
     
        fstream fout; 
        fout.open("/home/pi/iot/store/weatherData.csv", ios::out | ios::app);

	 
	    string now = getDate(); 
 
 
        fout << now << ","
        << airTempSensationOne << ","
        << airHumSensationOne << ","
        << airTempOne << ","
        << airHumOne << ","
        << earthTempOne << ","
        << earthHumOne << ","
        << lightOne << ","

        << airTempSensationTwo << ","
        << airHumSensationTwo << ","
        << airTempTwo << ","
        << airHumTwo << ","
        << earthTempTwo << ","
        << earthHumTwo << ","
        << lightTwo << ","

	<< airTempSensationThree << ","
        << airHumSensationThree << ","
        << airTempThree << ","
        << airHumThree << ","
        << earthTempThree << ","
        << earthHumThree << ","
        << lightThree << ","

        << airTempSensationFour << ","
        << airHumSensationFour << ","
        << airTempFour << ","
        << airHumFour << ","
        << earthTempFour << ","
        << earthHumFour << ","
        << lightFour << ","

        << airTempSensationFive << ","
        << airHumSensationFive << ","
        << airTempFive << ","
        << airHumFive << ","
        << earthTempFive << ","
        << earthHumFive << ","
        << lightFive << ","
        << "false"  << ","
        << now << "\n";

        fout.close();
    }
```

Se declara un método que no devuelve nada, su función es insertar los datos de las variables ambientales que ha recibido el Gateway y lo guarda en un archivo CSV, llamado: weatherData.csv, fout es el puntero, este hace referencia al archivo CSV que se crea si no existe, o que lo abre si este existe, luego de esto pide la fecha actual para que posteriormente guardar los datos de cada variable y su fecha y finalmente cierra el documento. 


### Validación de Datos

``` c++ 
    bool validationData(bool one, bool two, bool three, bool four, bool five) {
    
        bool isComplete = true;
        if(!one){
          isComplete = false;
        }
        if(!two){
          isComplete = false;
        }
        if(!three){
          isComplete = false;
        }
        if(!four){
          isComplete = false;
        }
        if(!five){
          isComplete = false;
        }
        return isComplete;
    }
```

Este método, tiene la función de validar si todos los nodos han enviado los datos, si esto es así devuelve un verdadero, pero si no, devolverá falso, este se hace con el fin de, al validar esto, los datos puedan ser guardados en un archivo.


### Proceso General

Teniendo en cuenta que este método es general  y repetitivo se divide en:

1. Inicializar comunicación
2. Bucle repetitivo
3. Recepción de datos
4. Validación de datos
5. Escritura de datos


#### Inicializar comunicación


``` c++ 
    radio.begin();
	delay(10);
	network.begin(90, 00); 
```

Se inicia la comunicación del Transceptor nrf24l01, se selecciona el canal de comunicación en el 90 (0-254), y se declara que este módulo es el Gateway declarándolo con el código 00.

#### Bucle repetitivo

``` c++ 
    while(1)
	{
	    ...
	}
	return 0;
```

Se realiza un bucle que nunca termine, el código se ejecute siempre hasta que sea interrumpido por el usuario.

#### Recepción de datos

``` c++ 
    network.update();
  		 while ( network.available() ) {     // Is there anything ready for us?

		 	RF24NetworkHeader header;        // If so, grab it and print it out
   			nodeData payload;
  			network.read(header,&payload,sizeof(payload));
			nodeIdTx = payload.nodeId;
                        printf("Node from %i : \n",nodeIdTx);

			    switch (nodeIdTx)
      			    {
		                 case 201:
		                        if(!newFromOne){
					                    printf("Received data from Node # %u ...",payload.nodeId);
                                    	printf(" data: ATS %0.2f data: AHS %0.2f  data: AT %0.2f  data: AH %0.2f   ",payload.airTempSensation,payload.airHumSensation,payload.airTemp,payload.airHum);
                                    	printf(" data: ET %0.2f data: EH %0.2f  data: L %0.2f  \n",payload.earthTemp,payload.earthHum,payload.light);

					                    airTempSensationOne = payload.airTempSensation;
                        				airHumSensationOne = payload.airHumSensation;
                        				airTempOne = payload.airTemp;
                        				airHumOne = payload.airHum;
                        				earthTempOne = payload.earthTemp;
                        				earthHumOne = payload.earthHum;
                        				lightOne = payload.light;
					                    newFromOne = true;
				                }
            			        break;
		                case 202:
                                if(!newFromTwo){
					                       printf("Received data from Node # %u ...",payload.nodeId);
                                    	printf(" data: ATS %0.2f data: AHS %0.2f  data: AT %0.2f  data: AH %0.2f   ",payload.airTempSensation,payload.airHumSensation,payload.airTemp,payload.airHum);
                                    	printf(" data: ET %0.2f data: EH %0.2f  data: L %0.2f  \n",payload.earthTemp,payload.earthHum,payload.light);

					                    airTempSensationTwo = payload.airTempSensation;
                                        airHumSensationTwo = payload.airHumSensation;
                                        airTempTwo = payload.airTemp;
                                        airHumTwo = payload.airHum;
                                        earthTempTwo = payload.earthTemp;
                                        earthHumTwo = payload.earthHum;
                                        lightTwo = payload.light;
					                    newFromTwo = true;
                                }
				                break;
                         case 203:
                                if(!newFromThree){
					                    printf("Received data from Node # %u ...",payload.nodeId);
                                        printf(" data: ATS %0.2f data: AHS %0.2f  data: AT %0.2f  data: AH %0.2f   ",payload.airTempSensation,payload.airHumSensation,payload.airTemp,payload.airHum);
                                        printf(" data: ET %0.2f data: EH %0.2f  data: L %0.2f  \n",payload.earthTemp,payload.earthHum,payload.light);

                                        airTempSensationThree = payload.airTempSensation;
                                        airHumSensationThree = payload.airHumSensation;
                                        airTempThree = payload.airTemp;
                                        airHumThree = payload.airHum;
                                        earthTempThree = payload.earthTemp;
                                        earthHumThree = payload.earthHum;
                                        lightThree = payload.light;

                                        newFromThree = true;
                                }
                                break;
                         case 204:
                                if(!newFromFour){
					                    printf("Received data from Node # %u ...",payload.nodeId);
                                        printf(" data: ATS %0.2f data: AHS %0.2f  data: AT %0.2f  data: AH %0.2f   ",payload.airTempSensation,payload.airHumSensation,payload.airTemp,payload.airHum);
                                        printf(" data: ET %0.2f data: EH %0.2f  data: L %0.2f  \n",payload.earthTemp,payload.earthHum,payload.light);

                                        airTempSensationFour = payload.airTempSensation;
                                        airHumSensationFour = payload.airHumSensation;
                                        airTempFour = payload.airTemp;
                                        airHumFour = payload.airHum;
                                        earthTempFour = payload.earthTemp;
                                        earthHumFour = payload.earthHum;
                                        lightFour = payload.light;
                                        newFromFour = true;
                                }
                                break;
                         case 205:
                                if(!newFromFive){
					                    printf("Received data from Node # %u ...",payload.nodeId);
                                        printf(" data: ATS %0.2f data: AHS %0.2f  data: AT %0.2f  data: AH %0.2f   ",payload.airTempSensation,payload.airHumSensation,payload.airTemp,payload.airHum);
                                        printf(" data: ET %0.2f data: EH %0.2f  data: L %0.2f  \n",payload.earthTemp,payload.earthHum,payload.light);

					                    airTempSensationFive = payload.airTempSensation;
                                        airHumSensationFive = payload.airHumSensation;
                                        airTempFive = payload.airTemp;
                                        airHumFive = payload.airHum;
                                        earthTempFive = payload.earthTemp;
                                        earthHumFive = payload.earthHum;
                                        lightFive = payload.light;
					                    newFromFive = true;
                                }
                                break;
			            default: 
				            delay(100);
		                break;
		      	}
  		 }
```

Se actualiza el estado de la red de telemetría y se escucha por el canal seleccionado, si se recibe un nuevo paquete, se verifica que la estructura de datos contenga el ID y se verifica cual es el nodo que le pertenece ese ID, para que posteriormente se seleccionen los datos enviados y se guarden en sus respectivas variables del nodo, y además se le indica al sistema que ese nodo ya ha enviado, por lo que si vuelve a enviar simplemente se ignora. Si esto no ocurre, el sistema seguirá escuchando hasta que reciba un paquete que cumpla con dicha estructura.


#### Validación de datos

``` c++  
    bool statusData = validationData(newFromOne, newFromTwo, newFromThree, newFromFour, newFromFive);
```

Después de realizar la comunicación, el sistema valida si todos los nodos ya han enviado los datos correspondientes, haciendo un llamado al método o VALIDATIONDATA, asignándole la variable y pasando los argumentos del estado de envío de cada nodo, si todos han enviado el sistema devolverá verdadero y si no, devolverá falso.

#### Escritura de datos

``` c++ 
    if(statusData){
                         
        newFromOne   = false;
		newFromTwo   = false;
        newFromThree = false;
        newFromFour  = false;
        newFromFive  = false;
		writeCSV();
		delay(2000);
    }
    delay(100);
```

Finalmente, de acuerdo con el resultado de VALIDATIONDATA el sistema decide si puede guardar los datos en un archivo CSV y  reiniciar las variables para volver a iniciar el proceso.

