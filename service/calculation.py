#!/usr/bin/python3
import math

def average(dataOne=0, dataTwo=0, dataThree=0, dataFour=0, dataFive=0):
    averageList = [dataOne, dataTwo, dataThree, dataFour, dataFive]
    sum = 0
    for numberList in averageList:
        sum += numberList
    sum = sum/5
    return  round(sum, 2)


def averageVar(data):
    averageNode = []
    #algo = [[ y[x] for y in data.values()] for x in range(7)]
    #print(algo)
    for x in range(7):
        sum = 0
        for y in data.values():
            #print(y)
            sum += y[x]
        average = round(sum/5 ,2)
        #print('average: {}'.format(average))
        averageNode.append(average)

    return averageNode


def genereRandomList():
    import random
    randomFloatList = []
    for i in range(7):
        x = round(random.uniform(0.00, 100.00), 2)
        randomFloatList.append(x)
    #print(randomFloatList)
    return randomFloatList



def main():
    nodeList = genereRandomList()
    print(nodeList)
    number = average(nodeList[0], nodeList[1], nodeList[2], nodeList[3], nodeList[4])
    print(number)



if __name__ == "__main__":
    main()



