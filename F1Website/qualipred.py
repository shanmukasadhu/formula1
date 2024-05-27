# Prediction of a drivers Qualifying Result using historical data

# Imports
from functionFile import getDriverId
from functionFile import convert_time_to_seconds
from functionFile import getDriverId
from functionFile import convert_time_to_seconds
from functionFile import most_frequent_number
from functionFile import getLast10quali
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import HuberRegressor
from sklearn.tree import DecisionTreeRegressor

# Pandas Dataframe creation from Kaggle CSV files
all_races = pd.read_csv("kaggleDataset/races.csv").loc[:,["raceId","year","round","circuitId"]]
all_results = pd.read_csv("kaggleDataset/results.csv").loc[:, ["resultId", "raceId", "driverId", "constructorId", "number", "grid", "position", "points", "laps", "time", "milliseconds", "fastestLap", "fastestLapTime"]]
all_drivers = pd.read_csv("kaggleDataset/drivers.csv").loc[:, ["driverId", "driverRef", "number", "forename", "surname", "nationality"]]
all_circuits = pd.read_csv("kaggleDataset/circuits.csv").loc[:,["circuitId","circuitRef","name","location","country","lat","lng","alt"]]
pitstops = pd.read_csv("kaggleDataset/pit_stops.csv")

# Find the last 10 drivers qualifications
# - Race number should be above the 10th race
driver = input("Enter drivers name: ")
driverId = getDriverId(driver,all_drivers)

driverRes = all_results.loc[all_results["driverId"] == int(driverId)]


count = 0
countOfRace = 0
last10qualies = []
tenthgrid = []

#Finds last 10 driver qualifying results in a current year
for idx, row in driverRes.iterrows():
    qualifyingRes = row["grid"]
    raceId = row["raceId"]
    year = all_races.loc[all_races["raceId"] == raceId, "year"].values[0]
    if(count ==0):
        current_year = year
    else:
        if(current_year != year):
            current_year = year
            countOfRace = 0
        else:
            if(countOfRace >= 11):
                print(str(year)+" "+str(countOfRace))
                last10qualies.append(getLast10quali(driver, year, countOfRace, all_drivers ,all_races, all_results))
                tenthgrid.append(qualifyingRes)
            countOfRace+=1
    count+=1

    
    
    
print(tenthgrid)


# Data Processing(Train-Test Split)
X = last10qualies  
y = tenthgrid      

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#Different Models to experiment with:
#  - Linear Regression
#  - Logistic Regression
#  - Huber Regression
#  - Decision Tree Regression
model = LinearRegression()
model1 = LogisticRegression()
model2 = HuberRegressor()
model3 = DecisionTreeRegressor()



model.fit(X_train, y_train)
model1.fit(X_train, y_train)
model2.fit(X_train, y_train)
model3.fit(X_train, y_train)


y_pred = model.predict(X_test)
y_pred1 = model1.predict(X_test)
y_pred2 = model2.predict(X_test)
y_pred3 = model3.predict(X_test)




mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error of Linear Regression: {mse}")

mse1 = mean_squared_error(y_test, y_pred1)
print(f"Mean Squared Error of Logistic Regression: {mse1}")

mse2 = mean_squared_error(y_test, y_pred2)
print(f"Mean Squared Error of Huber Regression: {mse2}")

mse3 = mean_squared_error(y_test, y_pred3)
print(f"Mean Squared Error of Decision Tree Regression: {mse3}")


 # Replace with actual new data(Just an reshaped numpy array of length 10):
charlesLast10 = np.array([1,2,2,1,2,2,5,8,6,2]).reshape(1, -1) 
albonsLast10 = np.array([14,14,15,5,13,12,12,14,14,14]).reshape(1,-1)

new_data = albonsLast10
prediction = model.predict(new_data)
print(f"Prediction for new data of Linear Regression: {prediction[0]}")

prediction1 = model1.predict(new_data)
print(f"Prediction for new data of Logistic Regression: {prediction1[0]}")

prediction2 = model2.predict(new_data)
print(f"Prediction for new data of Huber Regression: {prediction2[0]}")

prediction3 = model3.predict(new_data)
print(f"Prediction for new data of Decision Tree Regression: {prediction3[0]}")



