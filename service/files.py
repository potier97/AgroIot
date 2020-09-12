#!/usr/bin/python3
from datetime import datetime
import pytz

def manageFiles(logsFile="logs.txt", message='New data added on:', time='No time', status=False):
    if status:
        statusData = 'Data Send'
    else:
        statusData = 'No Data Send'
    with open(logsFile, 'a') as file:
        #if '00:01' in time:
        #    file.write("New data day  --  \n")
        file.write("{} {}  --  Status: {} \n" .format(message, time, statusData))


def currentTime():
    zone='America/Bogota'
    getDate = datetime.now(pytz.timezone(zone));
    #print(getDate)
    #print(type(getDate))
    #Format -> d/m/Y H:M:S
    return getDate

def dateTimeConvert(date):
    dateTimeConvert = datetime.strftime(date ,'%d/%m/%Y %H:%M:%S')
    #dateTimeConvert = time.timestamp(dateTimeConvert)
    #print(type(dateTimeConvert))
    #print(dateTimeConvert)
    return dateTimeConvert

def strToTime(date):
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
