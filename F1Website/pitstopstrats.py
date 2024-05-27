# Using K-Means Clustering to determine Pit-Stop Strategies for certain tracks

#Imports
from functionFile import getDriverId
from functionFile import convert_time_to_seconds
from functionFile import getDriverId
from functionFile import convert_time_to_seconds
from functionFile import most_frequent_number
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import KMeans

# Pandas Dataframe creation from Kaggle CSV files
all_races = pd.read_csv("kaggleDataset/races.csv").loc[:,["raceId","year","round","circuitId"]]
all_results = pd.read_csv("kaggleDataset/results.csv").loc[:, ["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "points", "laps", "time", "milliseconds", "fastestLap", "fastestLapTime"]]
all_drivers = pd.read_csv("kaggleDataset/drivers.csv").loc[:, ["driverId", "driverRef", "number", "forename", "surname", "nationality"]]
all_circuits = pd.read_csv("kaggleDataset/circuits.csv").loc[:,["circuitId","circuitRef","name","location","country","lat","lng","alt"]]
pitstops = pd.read_csv("kaggleDataset/pit_stops.csv")


# Ask user-input:
circuitinfo = input("Enter a formula 1 circuit: ")

#Finds the circuitID of the circuit given by the user:
mask = all_circuits["name"].str.contains(circuitinfo, case=False, na=False)
circuit_data = all_circuits[mask]
circuitId = circuit_data[["circuitId"]].iloc[0]["circuitId"].item()

#Retrieves all races at that specific circuit:
allcustomraces = all_races.loc[all_races["circuitId"] == circuitId]
#Gets all raceIds of races at that circuits
racesId = np.asarray(allcustomraces[["raceId"]])


# Getting Qualifying position and pre-processing
goodDriver = []
Biglapstops = []
BigpitstopArray = []
whatsurpos = input("Whats your position: ")
aliaspos = {1:"Front 5", 2:"Front 5", 3:"Front 5", 4:"Front 5", 5:"Front 5", 6:"Second 10", 
            7:"Second 10", 8:"Second 10", 9:"Second 10",10:"Second 10", 11:"Third 15", 12:"Third 15", 
            13:"Third 15", 14:"Third 15", 15:"Third 15", 16:"Final Four", 17:"Final Four", 
           18:"Final Four", 19:"Final Four", 20:"Final Four"}
for race in racesId: 
      if(race>=841 and race<=1110):#2007-2023(They started tracking pistop info in 2007)
        lum = all_results.loc[all_results["raceId"] == race[0]]
        dum = pitstops.loc[pitstops["raceId"] == race[0]]
        for row in lum.iterrows(): # Checks if the driver finished in a position greater than where they started
            if(row[1]["position"] != "\\N" and int(row[1]["grid"]) > int(row[1]["position"])):
                
                if(row[1]["grid"] <= 20 and aliaspos[row[1]["grid"]] == aliaspos[int(whatsurpos)]):
                    goodDriver.append(row[1]["driverId"])
        for driver in goodDriver:
            rum = dum.loc[dum["driverId"] == driver]
            
            if(len(rum) != 0):
                if(':' not in str(rum[["duration"]])):
                    Biglapstops.append(len(rum))
                    for num in np.asarray(rum[["lap"]]):
                        Biglapstops.append(num[0])
                    BigpitstopArray.append(Biglapstops)
                    Biglapstops = []
            
print(BigpitstopArray) 


# Use K-Means Clustering:

flattened_laps = []
mostFrequentArray=[]
for num in BigpitstopArray:
    mostFrequentArray.append(num[0])




optimal_clusters = most_frequent_number(mostFrequentArray)
for strategy in BigpitstopArray:
    if(strategy[0] == optimal_clusters):
        for i in range(1,optimal_clusters+1):
            flattened_laps.append(strategy[i])


X = np.array(flattened_laps).reshape(-1, 1)

# K-Means vs KMedoids

kmeans = KMedoids(n_clusters=optimal_clusters, random_state=19)
kmeans.fit(X)

kmeansorg = KMeans(n_clusters=optimal_clusters, random_state=19)
kmeansorg.fit(X)



print(f"Optimal number of pitstops: {optimal_clusters}")
print(f"Optimal pitstop laps: {sorted(kmeansorg.cluster_centers_.flatten())}")


optimal_laps = sorted(kmeans.cluster_centers_.flatten())
print(f"Optimal number of pitstops: {optimal_clusters}")
print(f"Optimal pitstop laps: {optimal_laps}")
prev_lap = 0
tires= []

# Determines through the number of laps and stops, which tires to use: 
for lap in optimal_laps:
    if(lap - prev_lap<10):
        print("Soft Tires")
        tires.append('S')
    elif(lap - prev_lap>= 10 and lap-prev_lap < 30):
        print("Medium tires")
        tires.append('M')
    else:
        print("Hard Tires")
        tires.append('H')
    prev_lap = lap
if(63 - prev_lap<10):
    print("Soft Tires")
    tires.append('S')
elif(63 - prev_lap>= 10 and 63-prev_lap < 30):
    print("Medium tires")
    tires.append('M')
else:
    print("Hard Tires")
    tires.append('H')

#Plots all the clusters so they can be visualized and is the purpose of K-means clustering.
plt.plot([optimal_clusters]*len(flattened_laps),flattened_laps, marker="o")
plt.show()
for strategy in BigpitstopArray:
    if(strategy[0] == optimal_clusters):
        print(strategy)
