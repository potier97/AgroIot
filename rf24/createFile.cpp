#include <iostream>
#include <stdio.h>
#include <fstream>

using namespace std;


int main()
{
	// file pointer
	std::fstream fout;
	// opens an existing csv file or creates a new file.
	fout.open("weatherData.csv", ios::out | ios::app);

        //Header Doc
        fout << "dateCaptured" << ","
	<< "airTempSensationOne" << ","
	<< "airHumSensationOne" << ","
	<< "airTempOne" << ","
	<< "airHumOne" << ","
	<< "earthTempOne" << ","
	<< "earthHumOne" << ","
	<< "lightOne" << ","

	<< "airTempSensationTwo" << ","
        << "airHumSensationTwo" << ","
        << "airTempTwo" << ","
        << "airHumTwo" << ","
        << "earthTempTwo" << ","
        << "earthHumTwo" << ","
        << "lightTwo" << ","

	<< "airTempSensationThree" << ","
        << "airHumSensationThree" << ","
        << "airTempThree" << ","
        << "airHumThree" << ","
        << "earthTempThree" << ","
        << "earthHumThree" << ","
        << "lightThree" << ","

	<< "airTempSensationFour" << ","
        << "airHumSensationFour" << ","
        << "airTempFour" << ","
        << "airHumFour" << ","
        << "earthTempFour" << ","
        << "earthHumFour" << ","
        << "lightFour" << ","

	<< "airTempSensationFive" << ","
        << "airHumSensationFive" << ","
        << "airTempFive" << ","
        << "airHumFive" << ","
        << "earthTempFive" << ","
        << "earthHumFive" << ","
        << "lightFive" << ","
	<< "statusCloud" << ","
	<< "timeSent" << "\n";

        fout.close();
}
