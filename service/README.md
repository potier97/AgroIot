# Gateway - Envío de Datos

El objetivo de este servicio es el de verificar si existe nueva información de la red de telemetría en la base datos local que corresponde a un archivo CSV, para que esta sea: organizada, promediada, analizada y finalmente enviada a la plataforma de la nube de Firebase, allí se envían nuevos registros a la base de datos en tiempo real (FireStore) y también se cargan nuevas imágenes (Store), que corresponden al análisis geoespacial por medio de mapas de calor. Finalmente, el servicio le indica al archivo que los nuevos registros ya han sido cargados, por lo que este volverá a esperar por nuevos datos registrados dentro de este. Para ello se realiza un Script en Python y se utilizan las siguientes bibliotecas y sus respectivas versiones utilizadas:

 - firebase-admin = 4.4.0
 - grpcio = 1.13.0rc3
 - google-cloud-firestore = 0.29.0
 - google-cloud-storage = 1.10.0
 - scipy = 1.5.2
 - gstools = 1.2.1
 - emcee = 3.0.2
 - hankel = 1.1.0
 - mpmath = 1.1.0
 - matplotlib = 3.3.2
 - numpy = 1.19.2
 - pykrige = 1.5.1


## Servicio - iotFirebase

Se crea un archivo llamado: `iotFirebase.service` para ser ejecutado en la Raspberry Pi mediante Sistemd, para entender el funcionamiento y la manera en cómo se crea el servicio puede revisar el servicio del [RF24](https://github.com/potier97/AgroIot/blob/master/rf24/README.md)

El contenido de este archivo debe llevar lo siguiente:

``` sh
    [Unit]
    Description=Service cron Iot data for send data to Firebase
    After=multi-user.target
    
    [Service]
    Type=idle
    ExecStart=/usr/bin/python3 /home/pi/iot/service/main.py
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=pi
    
    [Install]
    WantedBy=multi-user.target
```

 - ExecStart: contiene la ruta al archivo que se debe ejecutar  las instrucciones adicionales que este debe llevar


Para saber más acerca de los servicios creados por Systemd, visite la   [documentación](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)

##  Envío de datos a Firebase
Para el desarrollo del proyecto se crea un Script en Python, llamado `main.py`, y es descrito a continuación, y también  las importaciones necesarias para su funcionamiento. 

### main

#### Importaciones
``` py
    #!/usr/bin/python3
    import os
    import schedule
    from blink import blink
    import time
    import files
    import firebase
    import heatMap
    import calculation
    import pandas as pd 
```

 - #!/usr/bin/python3: Le indica al sistema operativo cual es el intérprete utilizado para el siguiente archivo
 - import os: Biblioteca para realizar instrucciones con el sistema operativo
 - import schedule: Biblioteca para la automatización y ejecución de tareas
 - from blink import blink: Biblioteca creada para prender y apagar un led de los periféricos de la Raspberry
 - import time: Biblioteca para manejar y obtener fechas
 - import files: Biblioteca para el manejo de archivos
 - import firebase: Biblioteca para la conexión y envío de información a la base de datos de firebase y al storage
 - import heatMap: Biblioteca creada para la realización de mapas de calor por medio de Krigrin
 - import calculation: Biblioteca creada para la realización de cálculos básicos
 - import pandas as pd: Biblioteca para el manejo de Dataframes con el fin de manipular series temporales y/o tablas

#### Método principal

``` py
def main():
    schedule.every().hour.at(":01").do(simpleJob)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
```

Se declara el método principal, el cual después es ejecutado al ser el archivo principal que es llamado, en la declaración del método de main, se encuentra: la declaración de la función que debe ser ejecutada cada hora a las "XX:01", por lo tanto, la función que debe ser llamada en ese momento es "simpleJob". Luego de esto se entra a un bucle sin fin, con el objetivo de estar preguntando siempre, sí las tareas que han sido programadas ya deben de ser ejecutadas de acuerdo a los parámetros asignados, y posteriormente se coloca un retardo de un segundo con el fin de no saturar la ejecución del programa.

#### Tarea Automatizada

``` py
firebase.validateAccount()
newBlink = blink()

def simpleJob():
    try:
        for i in range(10):
            newBlink.ledOn(0.25)
            newBlink.ledOff(0.25)
        fileName="/home/pi/iot/store/weatherData.csv"
        df = pd.read_csv(fileName)
        
        currentDatetime = files.currentTime()
        currentDatetimeStr = files.dateTimeConvert(currentDatetime)
        newDataStatus = False
        
        for id, row in df.iterrows():
            if row.statusCloud == False:
            
                newDataStatus = True
                nodeOne   = [row.airHumOne, row.airHumSensationOne, row.airTempOne, row.airTempSensationOne, row.earthHumOne, row.earthTempOne, row.lightOne]
                nodeTwo   = [row.airHumTwo, row.airHumSensationTwo, row.airTempTwo, row.airTempSensationTwo, row.earthHumTwo, row.earthTempTwo, row.lightTwo]
                nodeThree = [row.airHumThree, row.airHumSensationThree, row.airTempThree, row.airTempSensationThree, row.earthHumThree, row.earthTempThree, row.lightThree]
                nodeFour  = [row.airHumFour, row.airHumSensationFour, row.airTempFour, row.airTempSensationFour, row.earthHumFour, row.earthTempFour, row.lightFour]
                nodeFive  = [row.airHumFive, row.airHumSensationFive, row.airTempFive, row.airTempSensationFive, row.earthHumFive, row.earthTempFive, row.lightFive]

                telemetryTime = files.strToTime(row.dateCaptured)

                telemetryTimeStr =  files.dateTimeConvert(telemetryTime)

                #airHum0, airHumSensation0, airTemp0, airTempSensation0, earthHum0, earthTemp0, light0,
                airTemp   = [nodeOne[2], nodeTwo[2], nodeThree[2], nodeFour[2], nodeFive[2]]
                airHum    = [nodeOne[0], nodeTwo[0], nodeThree[0], nodeFour[0], nodeFive[0]]
                earthTemp = [nodeOne[5], nodeTwo[5], nodeThree[5], nodeFour[5], nodeFive[5]]
                earthHum  = [nodeOne[4], nodeTwo[4], nodeThree[4], nodeFour[4], nodeFive[4]]
                light     = [nodeOne[6], nodeTwo[6], nodeThree[6], nodeFour[6], nodeFive[6]]


                #Charts
                fileImagePath_AirTemp,   fileName_AirTemp   = heatMap.myPlot(0, airTemp,   telemetryTimeStr)
                fileImagePath_AirHum,    fileName_AirHum    = heatMap.myPlot(1, airHum,    telemetryTimeStr)
                fileImagePath_EarthTemp, fileName_EarthTemp = heatMap.myPlot(2, earthTemp, telemetryTimeStr)
                fileImagePath_EarthHum,  fileName_EarthHum  = heatMap.myPlot(3, earthHum,  telemetryTimeStr)
                fileImagePath_Light,     fileName_Light     = heatMap.myPlot(4, light,     telemetryTimeStr)


                #Upload image to Storage
                pathUrl_AirTemp   = firebase.insertFile(0, fileImagePath_AirTemp,   fileName_AirTemp)
                pathUrl_AirHum    = firebase.insertFile(1, fileImagePath_AirHum,    fileName_AirHum)
                pathUrl_EarthTemp = firebase.insertFile(2, fileImagePath_EarthTemp, fileName_EarthTemp)
                pathUrl_EarthHum  = firebase.insertFile(3, fileImagePath_EarthHum,  fileName_EarthHum)
                pathUrl_Light     = firebase.insertFile(4, fileImagePath_Light,     fileName_Light)
                
                nodes = firebase.dicNodes(currentDatetime, telemetryTime,
                                 fileImagePath_AirTemp, fileImagePath_AirHum, fileImagePath_EarthTemp, fileImagePath_EarthHum, fileImagePath_Light,
                                 pathUrl_AirTemp, pathUrl_AirHum, pathUrl_EarthTemp, pathUrl_EarthHum, pathUrl_Light,
                                 nodeOne, nodeTwo, nodeThree, nodeFour, nodeFive)
                                 
                firebase.insertData(nodes)
                
                df.at[id,'dateCaptured'] = telemetryTimeStr
                df.at[id,'statusCloud'] = True
                df.at[id,'timeSent'] = currentDatetimeStr

        files.manageFiles(message='New data added on:', time=currentDatetimeStr, status=newDataStatus)
        df.to_csv(fileName, index=False, float_format='%.2f')

        for i in range(10):
            newBlink.ledOn(0.25)
            newBlink.ledOff(0.25)
        
    except:
        newBlink.ledOff()
```

Antes de dar entender el funcionamiento de la tarea principal, hay que explicar dos instrucciones:

 - firebase.validateAccount(): Realiza la conexión y autenticación con Firebase y sus servicios antes de enviar cualquier contenido o solicitud
 - newBlink = blink(): Instancia un objeto llamado newBlinck, la cual va a hacer que prenda y apague un led piloto, que le indica al usuario el funcionamiento de la tarea generada

Luego de lo anterior, se puede empezar a explicar el funcionamiento de la tarea principal.

Se declara un try except antes de la ejecución de la tarea principal, el cual tiene como objetivo la ejecución de un bloque de código dentro de try para la búsqueda de errores, el cual llega a encontrar alguno va a hacer manejado con except y reiniciara la ejecución de todo el código.

``` py
        for i in range(10):
            newBlink.ledOn(0.25)
            newBlink.ledOff(0.25)
            
        fileName="/home/pi/iot/store/weatherData.csv"
        df = pd.read_csv(fileName)
        
        currentDatetime = files.currentTime()
        currentDatetimeStr = files.dateTimeConvert(currentDatetime)
        newDataStatus = False
```

La tarea principal consiste en prender y  apagar un led 10 veces, esto para indicar al usuario que se está ejecutando la tarea. Luego de ello se declara una variable la cual va a hacer la ruta al archivo CSV el cual va a hacer la base de datos local donde están guardados todos los registros hasta el momento de su llamado. Luego es llamado por medio de la librería Pandas, el cual permite abrir el documento y ser leído por medio de la instrucción "pd.read_csv". Luego, se le pide al sistema la hora actual y se obtiene en un formato tipo TIME para Python, lo que es necesario convertirlo a un simple string con la instrucción "files.dateTimeConvert", finalmente se declara una variable en falso, el cual va a hacer el validador si hay o no nuevos datos en el registro del archivo CSV.


``` py
        for id, row in df.iterrows():
            if row.statusCloud == False:
            
                newDataStatus = True
                nodeOne   = [row.airHumOne, row.airHumSensationOne, row.airTempOne, row.airTempSensationOne, row.earthHumOne, row.earthTempOne, row.lightOne]
                nodeTwo   = [row.airHumTwo, row.airHumSensationTwo, row.airTempTwo, row.airTempSensationTwo, row.earthHumTwo, row.earthTempTwo, row.lightTwo]
                nodeThree = [row.airHumThree, row.airHumSensationThree, row.airTempThree, row.airTempSensationThree, row.earthHumThree, row.earthTempThree, row.lightThree]
                nodeFour  = [row.airHumFour, row.airHumSensationFour, row.airTempFour, row.airTempSensationFour, row.earthHumFour, row.earthTempFour, row.lightFour]
                nodeFive  = [row.airHumFive, row.airHumSensationFive, row.airTempFive, row.airTempSensationFive, row.earthHumFive, row.earthTempFive, row.lightFive]

                telemetryTime = files.strToTime(row.dateCaptured)

                telemetryTimeStr =  files.dateTimeConvert(telemetryTime)

                #airHum0, airHumSensation0, airTemp0, airTempSensation0, earthHum0, earthTemp0, light0,
                airTemp   = [nodeOne[2], nodeTwo[2], nodeThree[2], nodeFour[2], nodeFive[2]]
                airHum    = [nodeOne[0], nodeTwo[0], nodeThree[0], nodeFour[0], nodeFive[0]]
                earthTemp = [nodeOne[5], nodeTwo[5], nodeThree[5], nodeFour[5], nodeFive[5]]
                earthHum  = [nodeOne[4], nodeTwo[4], nodeThree[4], nodeFour[4], nodeFive[4]]
                light     = [nodeOne[6], nodeTwo[6], nodeThree[6], nodeFour[6], nodeFive[6]]


                #Charts
                fileImagePath_AirTemp,   fileName_AirTemp   = heatMap.myPlot(0, airTemp,   telemetryTimeStr)
                fileImagePath_AirHum,    fileName_AirHum    = heatMap.myPlot(1, airHum,    telemetryTimeStr)
                fileImagePath_EarthTemp, fileName_EarthTemp = heatMap.myPlot(2, earthTemp, telemetryTimeStr)
                fileImagePath_EarthHum,  fileName_EarthHum  = heatMap.myPlot(3, earthHum,  telemetryTimeStr)
                fileImagePath_Light,     fileName_Light     = heatMap.myPlot(4, light,     telemetryTimeStr)


                #Upload image to Storage
                pathUrl_AirTemp   = firebase.insertFile(0, fileImagePath_AirTemp,   fileName_AirTemp)
                pathUrl_AirHum    = firebase.insertFile(1, fileImagePath_AirHum,    fileName_AirHum)
                pathUrl_EarthTemp = firebase.insertFile(2, fileImagePath_EarthTemp, fileName_EarthTemp)
                pathUrl_EarthHum  = firebase.insertFile(3, fileImagePath_EarthHum,  fileName_EarthHum)
                pathUrl_Light     = firebase.insertFile(4, fileImagePath_Light,     fileName_Light)
                
                nodes = firebase.dicNodes(currentDatetime, telemetryTime,
                                 fileImagePath_AirTemp, fileImagePath_AirHum, fileImagePath_EarthTemp, fileImagePath_EarthHum, fileImagePath_Light,
                                 pathUrl_AirTemp, pathUrl_AirHum, pathUrl_EarthTemp, pathUrl_EarthHum, pathUrl_Light,
                                 nodeOne, nodeTwo, nodeThree, nodeFour, nodeFive)
                                 
                firebase.insertData(nodes)
                
                df.at[id,'dateCaptured'] = telemetryTimeStr
                df.at[id,'statusCloud'] = True
                df.at[id,'timeSent'] = currentDatetimeStr
```

Esta es la tarea más larga del código, en el que todo está incluido en un FOR, por el cual el sistema lee cada registro y valida si hay nuevos campos los cuales no han sido analizados y enviados a la base de datos en la nube. Por lo que en cada ciclo evalúa si "row.statusClous" es falso, por lo que, si lo es, esta sería necesario analizar y procesar a la nube.

Entonces, cuando el registro no ha sido enviado, el sistema obtendrá todos los datos de ese registro y lo organizará en 5 listas, las cuales corresponden a cada nodo, su orden dentro de estas listas es: Humedad Aire, Sensación térmica, temperatura Aire, sensación térmica, Humedad Tierra, Temperatura Tierra y Luz. Luego de tener estas listas, el sistema lee la fecha en la que fue capturada esta información y la transforma en un formato de hora válida para el sistema, luego, el sistema organiza las listas por tipo de variable, para que pueda generar el análisis geoespacial por medio de la técnica del [Krigrin](https://geostat-framework.github.io/), esto generará 5 imágenes, una por cada tipo de variable, las guardara en la máquina y obtendrá las rutas a estos archivos. Después, el sistema subirá las imágenes a la Store de Firebase obteniendo la URL para poder ser visualizadas en la web, luego, el sistema generará un diccionario de Python, con cada una de las listas formadas al principio, esto generará un promedio de los datos listados, también tendrá las fechas en el que los datos fueron insertados a la base de datos y la fecha en la que los datos fueron enviados desde la red de telemetría, y las rutas de las imágenes en la máquina y las url, finalmente esta nueva estructura de datos será enviada a la nube, y este registro ahora tendrá la hora a la cual fue registrado en la nube y de que ya fue enviado a la nube finalizando así el proceso.



``` py
        files.manageFiles(message='New data added on:', time=currentDatetimeStr, status=newDataStatus)
        df.to_csv(fileName, index=False, float_format='%.2f')

        for i in range(10):
            newBlink.ledOn(0.25)
            newBlink.ledOff(0.25)
```

Finalmente, el código termina en el registro de logs, en el cual indica la hora en el que ha hecho el registro, así mismo, el archivo CSV leído correspondiente a la base de datos local, se vuelve a guardar toda la información leída y con los campos modificados, que corresponden con el estado de registro, esto con el fin de que no vuelva a enviar los mismos datos a la base de datos. y, por último, se vuelve a encender y apagar el led 10 veces, para indicar a usuario que el registro ya terminó.

