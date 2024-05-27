# This program compares 2 Formula 1 Drivers in a specific season(1950-2023)

#Imports
from functionFile import getDriverId
from functionFile import convert_time_to_seconds
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# Pandas Dataframe creation from Kaggle CSV files
all_races = pd.read_csv("kaggleDataset/races.csv").loc[:,["raceId","year","round","circuitId"]]
all_results = pd.read_csv("kaggleDataset/results.csv").loc[:, ["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "points", "laps", "time", "milliseconds", "fastestLap", "fastestLapTime"]]
all_drivers = pd.read_csv("kaggleDataset/drivers.csv").loc[:, ["driverId", "driverRef", "number", "forename", "surname", "nationality"]]


# Ask user-input:
teammate1 = input("Enter Teammate 1: ")
teammate2 = input("Enter Teammate 2: ")
year = input("Enter year: ")


#Array consisting of final race positions
driver1finalarray=[]
driver2finalarray=[]


#Array consisting of final qualifying positions
driver1qualiarray = []
driver2qualiarray = []

#Kaggle data assigns each driver a driver Id
driver1Id = getDriverId(teammate1, all_drivers)
driver2Id = getDriverId(teammate2, all_drivers)
count=0

#Matplotlib: 2 plots in the same figure
figure, axis = plt.subplots(2, 1)


#Obtain races for the specific season given:
racesofThatYear = all_races[all_races["year"] == int(year)]
racesId = np.asarray(racesofThatYear[["raceId"]])

# Tracks who outqualifies, outperforms, and outpaces each other
driver1outquali = 0
driver2outquali = 0

driver1outperform = 0
driver2outperform = 0

driver1outpace = 0
driver2outpace = 0


for num in racesId:
    count+=1
    driver1results = all_results.loc[all_results["driverId"] == int(driver1Id)].loc[all_results["raceId"] == int(num)]
    driver2results = all_results.loc[all_results["driverId"] == int(driver2Id)].loc[all_results["raceId"] == int(num)]
    
    driver1qualipos = driver1results[["grid"]].iloc[0]["grid"]
    driver2qualipos = driver2results[["grid"]].iloc[0]["grid"]
    
    driver1finalpos = driver1results[["position"]].iloc[0]["position"]
    driver2finalpos = driver2results[["position"]].iloc[0]["position"]
    
    if(driver1finalpos == '\\N' and driver2finalpos == '\\N'):
        driver1finalarray.append(None)
        driver2finalarray.append(None)
    elif(driver1finalpos == '\\N'):
        driver1finalarray.append(None)
        driver2finalarray.append(int(driver2finalpos))
    elif(driver2finalpos == '\\N'):
        driver1finalarray.append(int(driver1finalpos))
        driver2finalarray.append(None)
    else:
        if(driver2finalpos<driver1finalpos):
            driver2outperform+=1
        else:
            driver1outperform+=1
        driver1fastestLap = convert_time_to_seconds(driver1results[["fastestLapTime"]].iloc[0]["fastestLapTime"])
        driver2fastestLap = convert_time_to_seconds(driver2results[["fastestLapTime"]].iloc[0]["fastestLapTime"])
    
        if(driver1fastestLap<driver2fastestLap):
            driver1outpace+=1
        else:
            driver2outpace+=1

        
        driver2finalarray.append(int(driver2finalpos))
        driver1finalarray.append(int(driver1finalpos))
        
        
    if(driver1qualipos == '\\N' and driver2qualipos == '\\N'):
        driver1qualiarray.append(None)
        driver2qualiarray.append(None)
    elif(driver1qualipos == '\\N'):
        driver1qualiarray.append(None)
        driver2qualiarray.append(int(driver2qualipos))
    elif(driver2qualipos == '\\N'):
        driver1qualiarray.append(int(driver1qualipos))
        driver2qualiarray.append(None)
    else:
        if(driver2qualipos<driver1qualipos):
            driver2outquali+=1
        else:
            driver1outquali+=1
        driver2qualiarray.append(int(driver2qualipos))
        driver1qualiarray.append(int(driver1qualipos))
     

    

#Plots Qualifying Position between both drivers
axis[0].plot(range(1,count+1),driver1qualiarray, label = teammate1, marker='o')
axis[0].plot(range(1,count+1),driver2qualiarray, label = teammate2, marker='o')
axis[0].legend(loc="upper right")
axis[0].set_xticks(np.arange(1, count+1, step=2))
axis[0].set_title(teammate1+" vs "+ teammate2+" on qualifying positions in "+str(year), pad = 0, fontsize=8)

#Plots Finishing Position between both drivers        
axis[1].plot(range(1,count+1),driver1finalarray, label = teammate1, marker='o')
axis[1].plot(range(1,count+1),driver2finalarray, label = teammate2, marker='o')
axis[1].legend(loc="upper right")
axis[1].set_xticks(np.arange(1, count+1, step=2))
axis[1].set_title(teammate1+" vs "+ teammate2+" of finishing positions in "+str(year), pad = 0, fontsize=8)




plt.show()
print(teammate1+" outqualifed "+teammate2+" "+str(driver1outquali)+" times")
print(teammate2+" outqualifed "+teammate1+" "+str(driver2outquali)+" times")
print(teammate1+" outperformed "+teammate2+" "+str(driver1outperform)+" times")
print(teammate2+" outperformed "+teammate1+" "+str(driver2outperform)+" times")
print(teammate1+" outpaced "+teammate2+" "+str(driver1outpace)+" times")
print(teammate2+" outpaced "+teammate1+" "+str(driver2outpace)+" times")


