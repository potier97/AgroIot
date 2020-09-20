#include <RF24/RF24.h>
#include <RF24Network/RF24Network.h>
#include <iostream>
#include <ctime>
#include <stdio.h>
#include <time.h>
#include <fstream>
#include <sqlite3.h>

using namespace std;

//CE CSC
RF24 radio(22, 0);
RF24Network network(radio);

// Address of our node in Octal format
const uint16_t this_node = 00;
//Get ID from node
int nodeIdTx = 0;

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


//Get current dateTime
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

void writeCSV(){
	// file pointer
        fstream fout;
        // opens an existing csv file or creates a new file.
        fout.open("/home/pi/iot/store/weatherData.csv", ios::out | ios::app);

	//Get Date
	string now = getDate();
        //printf("%s\n",today.c_str());

	//Header Doc
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

void insertDB(){

	// Pointer to SQLite connection
	sqlite3* DB;
	// Save the result of opening the file
    	//int rc;
	// Saved SQL
    	//char* sql;
	// Compiled SQLite Statement
    	sqlite3_stmt *stmt;
	//Validation Conecction
        int exit = 0;
        exit = sqlite3_open("/home/pi/iot/store/sensordata.db", &DB);

        if (exit) {
                printf("No Abrio");
        }
        else{
                printf("Abrio base de datos");
        }


	//INSERT INTO dhtreadings(temperature, humidity, currentdate, currentime, device) values(22.4, 48, date('now'), time('now'), "manual");
	//INSERT INTO dhtreadings(temperature, humidity, currentdate, currentime, device) values(22.5, 48.7, date('now'), time('now'), "manual");
	char* query = NULL;
	asprintf(&query,  "INSERT INTO greenhouseData ('currentdate', 'airTempSensationOne', 'airHumSensationOne', 'airTempOne', 'airHumOne', 'earthTempOne', 'earthHumOne', 'lightOne', " \
        "'airTempSensationTwo', 'airHumSensationTwo', 'airTempTwo', 'airHumTwo', 'earthTempTwo', 'earthHumTwo', 'lightTwo',  " \
        "'airTempSensationThree', 'airHumSensationThree', 'airTempThree', 'airHumThree', 'earthTempThree', 'earthHumThree', 'lightThree',  " \
        "'airTempSensationFour', 'airHumSensationFour', 'airTempFour', 'airHumFour', 'earthTempFour', 'earthHumFour', 'lightFour',  " \
        "'airTempSensationFive', 'airHumSensationFive', 'airTempFive', 'airHumFive', 'earthTempFive', 'earthHumFive', 'lightFive')  " \
        "VALUES (datetime('now'), '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', " \
	" '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', " \
        " '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', " \
	" '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', " \
	" '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f', '%0.2f'  ); ", \
	airTempSensationOne, airHumSensationOne, airTempOne, airHumOne, earthTempOne, earthHumOne, lightOne,  \
	airTempSensationTwo, airHumSensationTwo, airTempTwo, airHumTwo, earthTempTwo, earthHumTwo, lightTwo,  \
	airTempSensationThree, airHumSensationThree, airTempThree, airHumThree, earthTempThree, earthHumThree, lightThree,  \
	airTempSensationFour, airHumSensationFour, airTempFour, airHumFour, earthTempFour, earthHumFour, lightFour,  \
	airTempSensationFive, airHumSensationFive, airTempFive, airHumFive, earthTempFive, earthHumFive, lightFive );


	//printf(query);
	sqlite3_prepare(DB, query, strlen(query), &stmt, NULL);
	sqlite3_step(stmt);
	sqlite3_finalize(stmt);
	//printf("%s /n ",rc.c_str());
	//free(query);
	sqlite3_close(DB);

}

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

int main(int argc, char** argv)
{
	radio.begin();
	delay(10);
	network.begin(/*channel*/ 90, /*node address*/ this_node);
	radio.printDetails();

	while(1)
	{
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
				//printf("No data from Network Nodes \n");
				delay(100);
		                break;
		      	}
  		 }


		 //Estado para guardar data en base de datos
		 bool statusData = validationData(newFromOne, newFromTwo, newFromThree, newFromFour, newFromFive);

		 if(statusData){
                        //string nowValidate = getDate();
                        //printf("Datos validados en:   %s \n",nowValidate.c_str());
                       	newFromOne   = false;
		       	newFromTwo   = false;
                       	newFromThree = false;
                       	newFromFour  = false;
                       	newFromFive  = false;
			//writeCSV();
			//insertDB();
			delay(2000);
                 }
                 delay(100);
	}
	return 0;
}

