# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
import re
from decimal import Decimal

arrayOfLogs = [line.rstrip() for line in sys.stdin.readlines()]  #reads stdin into list
endPoint = []  #array to store endpoint
tempArray = []
resCode = []  #array
time = [] #list of time
temptime = [] #another list of time
prevEndPoint = []
prevTime = []
tempList = []
mon = []
result = [] #list that will contain r

def convertMonth(mon):
    if mon == 'Jan':
        return 1
    elif mon == 'Feb':
        return 2
    elif mon == 'Mar':
        return 3
    elif mon == 'Apr':
        return 4
    elif mon == 'May':
        return 5
    elif mon == 'Jun':
        return 6
    elif mon == 'Jul':
        return 7
    elif mon == 'Aug':
        return 8
    elif mon == 'Sep':
        return 9
    elif mon == 'Oct':
        return 10
    elif mon == 'Nov':
        return 11
    elif mon == 'Dec':
        return 12

def processEndPoints(arrayOfIdenticalLogs):
    noneFiveHundredRC = 0
    global noneFiveHundredRC
    for k in range(len(arrayOfIdenticalLogs)):
        resCode = re.findall(r'\"\s\d\d\d', arrayOfIdenticalLogs[k]) #extract response code from log including " and whitespace before code
        responseCode = resCode[0] #resCode is an array of one character
        responseCode = responseCode[2:] #get rid of " and whitespace before response code
        if responseCode != '500':
            noneFiveHundredRC += 1;
    successRate = Decimal((noneFiveHundredRC / len(arrayOfIdenticalLogs) ) * 100.00)
    successRate = round(successRate, 2)
    tempList = re.findall(r'\d\d\d\d\:', arrayOfIdenticalLogs[0])
    dateAndTime = tempList[0]
    dateAndTime = dateAndTime[:-1]  # get rid of : after year
    dateAndTime += '-'
    mon = re.findall(r'\/[a-zA-Z][a-z][a-z]\/', arrayOfIdenticalLogs[0])
    month = mon[0]
    month = month[1:]
    month = month[:-1]
    month = convertMonth(month)
    dateAndTime += '0'
    dateAndTime += str(month)
    dateAndTime += '-'
    tempList = re.findall(r'\[\d\d', arrayOfIdenticalLogs[0])
    day = tempList[0]
    day = day[1:]
    dateAndTime += str(day)
    dateAndTime += 'T'
    tempList = re.findall(r'\:\d\d\:\d\d', arrayOfIdenticalLogs[0])
    timeAndSec = tempList[0]
    timeAndSec = timeAndSec[1:]
    dateAndTime += str(timeAndSec)
    arrayOfIdenticalLogs = re.findall(r'\s\/\d+\.\d+\/[a-zA-Z]+\/[a-zA-Z]+\.\bjson\b', arrayOfIdenticalLogs[0])
    dateAndTime += arrayOfIdenticalLogs[0]
    dateAndTime += " "
    dateAndTime += str(successRate)
    #print(dateAndTime)

    return dateAndTime

endPoint = re.findall(r'[a-zA-Z]{3,}\s\/\d+\.\d+\/[a-zA-Z]+\/[a-zA-Z]+\.\bjson\b', arrayOfLogs[0])  #store first endpoint
time = re.findall(r'\:\d\d\:\d\d', arrayOfLogs[0]) #store minute and time of first log

for i in range(len(arrayOfLogs)):
    arrayOfSimilarEP = []
    prevEndPoint = endPoint  #keep track of previous endpoint
    prevTime = time
    endPoint = re.findall(r'[a-zA-Z]{3,}\s\/\d+\.\d+\/[a-zA-Z]+\/[a-zA-Z]+\.\bjson\b', arrayOfLogs[i])  #store endpoint
    time = re.findall(r'\:\d\d\:\d\d', arrayOfLogs[i]) #store hour and minute
    if(endPoint[0] == prevEndPoint[0] and time[0] == prevTime[0] and i > 0):  #check for duplicate
        continue
    tempArray = arrayOfLogs[i:]

    for j in range(len(tempArray)):
        tempEndPoint = re.findall(r'[a-zA-Z]{3,}\s\/\d+\.\d+\/[a-zA-Z]+\/[a-zA-Z]+\.\bjson\b', tempArray[j])
        tempTime = re.findall(r'\:\d\d\:\d\d', tempArray[j])
        if(endPoint[0] == tempEndPoint[0] and time[0] == tempTime[0]):
            arrayOfSimilarEP.append(tempArray[j]) #store similar endpoints in list
    res = processEndPoints(arrayOfSimilarEP)
    result.append(res)


for i in range(len(result)):
    print(result[i])
