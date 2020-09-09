#include <iostream>
#include <stdio.h>
#include <fstream>
#include <ctime>

using namespace std;



int main()
{

	time_t ttime = time(0);
        tm* gmt_time = localtime(&ttime);

	//time_t ttime = time(0);
	/*//tm* gmt_time = localtime(&ttime);
        cout  << gmt_time->tm_mday << "/" 
	<< 1 + gmt_time->tm_mon << "/" 
	<< 1900 + gmt_time->tm_year  << " " 
	<< gmt_time->tm_hour << ":" 
	<< gmt_time->tm_min << ":" 
	<< gmt_time->tm_sec << endl;*/

	//Date
	int day = gmt_time->tm_mday;
	int month =  1 + gmt_time->tm_mon;
	int year = 1900 + gmt_time->tm_year;
	//Hour
	int hour = gmt_time->tm_hour;
	int min = gmt_time->tm_min;
	int second =  gmt_time->tm_sec;
        string space = " ";
	string slash = "/"; string points = ":"; string fecha = to_string(day) + slash + to_string(month) + slash + to_string(year) + space + to_string(hour) + points + to_string(min) + points + to_string(second); 
	printf("%s\n",fecha.c_str());

/*

        // file pointer
        std::fstream fout;
        // opens an existing csv file or creates a new file.
        fout.open("weatherData.csv", ios::out | ios::app);

        //Header Doc
        fout <<  << ", "
        << 11 << ", "
        << 11 << ", "
        << 11 << ", "
        << 11 << ", "
        << 11 << ", "
        << 11 << ", "
        << 11 << ", "

        << 22 << ", "
        << 22 << ", "
        << 22 << ", "
        << 22 << ", "
        << 22 << ", "
        << 22 << ", "
        << 22 << ", "

        << 33 << ", "
        << 33 << ", "
        << 33 << ", "
        << 33 << ", "
        << 33 << ", "
        << 33 << ", "
        << 33 << ", "

        << 44 << ", "
        << 44 << ", "
        << 44 << ", "
        << 44 << ", "
        << 44 << ", "
        << 44 << ", "
        << 44 << ", "

        << 55 << ", "
        << 55 << ", "
        << 55 << ", "
        << 55 << ", "
        << 55 << ", "
        << 55 << ", "
        << 55 <<"\n";

        fout.close();
*/
}
