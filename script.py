#!/usr/bin/python3
from datetime import datetime
import schedule
import time
import sys
"""
    Main cron job.
    The main cronjob to be run continuously.
"""


__autor__="Nicolás Potier Anzola"
__copyright__="Copyright 2020"
__credits__="EJEMPLO"

__license__="MIT"
__version__="0.1.0"
__maintainer__="nicolaspotier97@gmail.com"
__status__="Dev"

#Forma de acceder a la metadarta
# import module
#help(module)



#Argv
#Pasa argumentos cuando se ejecuta desde la consoala con argumentos
#se necesita importat Sys

#validar argumentos
#if(len(sys.argv) > 0):
#    print('Estos son los argumentos')
#    print(sys.argv)
#else:
#    print('Sin argumentos')
class nodo:
    def __init__(self, nombretres='nombreeeo'):
        self.color: 'rojo'
        self.edad= 12
        self.nombre = nombretres

    def algo(self, nombredos='dfvdfvdfv'):

        #nombremas = nombredos
        #print('Esto esta pasando');
        return self.nombre


create = nodo('cdscsdc')
algomas = create.algo()


print(algomas)

def geeks():
    print("Good Luck for Test")

def work():
    """
    Main cron job.
    The main cronjob to be run continuously.
    """
    print("Study and work hard")

# Defining main function
def main():
    print("hey there")
    print(datetime.now())
    print("hola mundooooo!!!!!")


#si es el pricipal, ejecutese, si no es llamado por otra función
if __name__=="__main__":
    main()


# sacado de https://www.geeksforgeeks.org/python-schedule-library/
# After every 10mins geeks() is called.
schedule.every(10).minutes.do(geeks)


#while True:
#    # Checks whether a scheduled task
#    # is pending to run or not
#    schedule.run_pending()
#    time.sleep(1)




