#!/usr/bin/python3
import time
import datetime

#"r" - Read - Default value. Opens a file for reading, error if the file does not exist
#"a" - Append - Opens a file for appending, creates the file if it does not exist
#"w" - Write - Opens a file for writing, creates the file if it does not exist
#"x" - Create - Creates the specified file, returns an error if the file exist
#"t" - Text - Default value. Text mode
#"b" - Binary - Binary mode (e.g. images)





def manageFiles(txt="/home/pi/iot/service/logs.txt", message='New message', time='algo'):
    with open(txt, 'a') as file:
        file.write('{} {} \n'.format(message, time))


def currentTime():
    getDate = datetime.datetime.now();
    #Format
    # dd/mm/YY H:M:S
    #strftime()The method creates a formatted string from a given datetime
    return getDate.strftime("%d/%m/%Y %H:%M:%S")


def main():
    now = currentTime()
    newMessage = 'New data added on:'
    manageFiles(message=newMessage,time=now)


if __name__ == "__main__":
    main()
