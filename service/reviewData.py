#!/usr/bin/python3
import os
import time
import files
import pandas as pd


def newData():
    algo = false
    if(algo):
        return True
    else:
        return False



def main():
    file = "/home/pi/iot/rf24/weatherData.csv"
    df = pd.read_csv(file, index_col=False, sep = ',', header=0,
         names=["dateCaptured", "airTempSensationOne", "airHumSensationOne", "airTempOne", "airHumOne", "earthTempOne", "earthHumOne",
                "lightOne", "airTempSensationTwo", "airHumSensationTwo", "airTempTwo", "airHumTwo", "earthTempTwo", "earthHumTwo", "lightTwo",
		"airTempSensationThree", "airHumSensationThree", "airTempThree", "airHumThree", "earthTempThree", "earthHumThree", "lightThree",
                "airTempSensationFour", "airHumSensationFour", "airTempFour", "airHumFour", "earthTempFour", "earthHumFour", "lightFour", "airTempSensationFive",
                "airHumSensationFive", "airTempFive", "airHumFive", "earthTempFive", "earthHumFive", "lightFive", "statusCloud", "timeSent"])
    #df.shape
    #a = df.head(10);
    #print(a)
    #for _, row in df.iterrows():
    #    if row.statusCloud == "false":
    #        print(row)
    #print(df.iloc[0])
    #getRow = df[df.statusCloud == true].iloc(0)
    #print(df[['statusCloud']])
    algo =df[df['statusCloud'] == False]
    print(algo)


if __name__ == "__main__":
    main()
