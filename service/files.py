#!/usr/bin/python3
from datetime import datetime
import pytz

def manageFiles(logsFile="/home/pi/iot/store/logs.txt", message='New data added on:', time='No time'):
    with open(logsFile, 'a') as file:
        #if '00:01' in time:
        #    file.write("New data day  --  \n")
        file.write("{} {}  \n" .format(message, time))


def currentTime():
    """
    Captura la fecha actual - genera un dato de tipo datetime.datetime
    """
    zone='America/Bogota'
    getDate = datetime.now(pytz.timezone(zone));
    #Format -> d/m/Y H:M:S
    return getDate

def dateTimeConvert(date):
    """
    Convertir de datetime.datetime  de la fila csv a tipo str
    """
    dateTimeConvert = datetime.strftime(date ,'%d/%m/%Y %H:%M:%S')
    #Format -> d/m/Y H:M:S
    return dateTimeConvert

def strToTime(date):
    """
    Convierte un dato tipo STR a un dato tipo datetime.datetime
    """
    zone='America/Bogota'
    dateTimeString = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    dateTimeString = dateTimeString.astimezone(pytz.timezone(zone))
    return dateTimeString;

def main():
    now = currentTime()
    #print(now)
    newMessage = 'New data added on:'
    nowConvert = dateTimeConvert(now)
    #print(nowConvert)
    #print(type(nowConvert))
    manageFiles(message=newMessage ,time=nowConvert)

    #nowConvert = files.dateTimeConvert(currentDatetime)
    #files.manageFiles(message=newMessage ,time=nowConvert, status=True)




if __name__ == "__main__":
    main()
