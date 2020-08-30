#!/usr/bin/python3
import json


def struct( date,
            airHum0, airHumSensation0, airTemp0, airTempSensation0, earthHum0, earthTemp0, light0,
            airHum1, airHumSensation1, airTemp1, airTempSensation1, earthHum1, earthTemp1, light1,
            airHum2, airHumSensation2, airTemp2, airTempSensation2, earthHum2, earthTemp2, light2,
            airHum3, airHumSensation3, airTemp3, airTempSensation3, earthHum3, earthTemp3, light3,
            airHum4, airHumSensation4, airTemp4, airTempSensation4, earthHum4, earthTemp4, light4,
            airHum5, airHumSensation5, airTemp5, airTempSensation5, earthHum5, earthTemp5, light5):

    data={
      "currentDate": date,
      "nodeId0": {
        "airHum":  airHum0,
        "airHumSensation":  airHumSensation0,
        "airTemp":  airTemp0,
        "airTempSensation":  airTempSensation0,
        "earthHum":  earthHum0,
        "earthTemp":  earthTemp0,
        "light":  light0,
      },
      "nodeId1": {
        "airHum":  airHum1,
        "airHumSensation":  airHumSensation1,
        "airTemp":  airTemp1,
        "airTempSensation":  airTempSensation1,
        "earthHum":  earthHum1,
        "earthTemp":  earthTemp1,
        "light":  light1,
      },
      "nodeId2": {
        "airHum":  airHum2,
        "airHumSensation":  airHumSensation2,
        "airTemp":  airTemp2,
        "airTempSensation":  airTempSensation2,
        "earthHum":  earthHum2,
        "earthTemp":  earthTemp2,
        "light":  light2,
      },
      "nodeId3": {
        "airHum":  airHum3,
        "airHumSensation":  airHumSensation3,
        "airTemp":  airTemp3,
        "airTempSensation":  airTempSensation3,
        "earthHum":  earthHum3,
        "earthTemp":  earthTemp3,
        "light":  light3,
      },
      "nodeId4": {
        "airHum":  airHum4,
        "airHumSensation":  airHumSensation4,
        "airTemp":  airTemp4,
        "airTempSensation":  airTempSensation4,
        "earthHum":  earthHum4,
        "earthTemp":  earthTemp4,
        "light":  light4,
      },
      "nodeId5": {
        "airHum":  airHum5,
        "airHumSensation":  airHumSensation5,
        "airTemp":  airTemp5,
        "airTempSensation":  airTempSensation5,
        "earthHum":  earthHum5,
        "earthTemp":  earthTemp5,
        "light":  light5,
      },
      "aditional":{

      }
    }
    return data




def main():
    import random
    z = struct("19/08/2020 23:11:01", round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
              round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2))
    y = json.dumps(z, indent=4)
    print(y)




if __name__ == '__main__':
    main()




