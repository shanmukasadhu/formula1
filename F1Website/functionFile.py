import numpy as np
import pandas as pd
from PIL import Image

import matplotlib.pyplot as plt

def getDriverId(driverName, all_drivers):
    forename = driverName.split(' ')[0]
    surname = driverName.split(' ')[1]
    info = all_drivers.loc[all_drivers["forename"] == forename].loc[all_drivers["surname"] == surname]
    return info.iloc[0]["driverId"]
def convert_time_to_seconds(time_str):
    minutes, seconds = time_str.split(':')
    total_seconds = int(minutes) * 60 + float(seconds)
    return total_seconds
def most_frequent_number(lst):
    counts = {}
    
    for num in lst:
        counts[num] = counts.get(num, 0) + 1
    
    most_frequent = None
    max_count = 0
    for num, count in counts.items():
        if count > max_count:
            most_frequent = num
            max_count = count
    
    return most_frequent

def getLast10quali(driver, year, tracknum, all_drivers ,all_races, all_results):
    driverId = getDriverId(driver, all_drivers)
    qualiTimes = []
    
    
    j = 0
    i=0
    if(int(tracknum) >=11):
        while(len(qualiTimes) < 11 and i < int(tracknum)):
            #print("i is "+str(i))
            #print("j is "+str(j))
            yearIdofFirstRace = all_races[all_races["year"] == int(year)].iloc[int(tracknum)-i-1]["raceId"]
            driverRes = all_results.loc[all_results["driverId"] == int(driverId)].loc[all_results["raceId"] == int(yearIdofFirstRace)]
            if driverRes.empty:
                if(11+j+1 < int(tracknum)):
                    j+=1
            else:
                
                qualifyingRes = driverRes[["grid"]].iloc[0]["grid"]
                qualiTimes.append(int(qualifyingRes))
            i+=1
        
        qualiTimes.reverse()
        plt.plot(range(1,12),qualiTimes, marker="o")
        plt.title(driver+ " last 10 qualification positions.")
        plt.ylabel("Position")
    return qualiTimes[:10]