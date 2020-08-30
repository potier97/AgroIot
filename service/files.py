#!/usr/bin/python3
from datetime import datetime
import pytz

#"r" - Read - Default value. Opens a file for reading, error if the file does not exist
#"a" - Append - Opens a file for appending, creates the file if it does not exist
#"w" - Write - Opens a file for writing, creates the file if it does not exist
#"x" - Create - Creates the specified file, returns an error if the file exist
#"t" - Text - Default value. Text mode
#"b" - Binary - Binary mode (e.g. images)


def manageFiles(logsFile="logs.txt", message='New data added on:', time='No time', status=False):
    if(status):
        statusData = 'Data Send'
    else:
        statusData = 'No Data Send'
    with open(logsFile, 'a') as file:
        file.write("{} {}  --  Status: {} \n" .format(message, time, statusData))
        #print('ok')


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

def main():
    now = currentTime()
    #print(now)
    newMessage = 'New data added on:'
    nowConvert = dateTimeConvert(now)
    #print(nowConvert)
    #print(type(nowConvert))
    manageFiles(message=newMessage ,time=nowConvert)

if __name__ == "__main__":
    main()
