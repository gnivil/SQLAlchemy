# Surfs Up!

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

-----

# Step 1 - Climate Analysis and Exploration

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Import Dependencies
```python
# Dependencies and Setup
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import scipy.stats as st

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct
```

* Use SQLAlchemy create_engine to connect to your sqlite database.
```python
# create engine to hawaii.sqlite
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
```

* Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.
```python
# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
inspector = inspect(engine)
inspector.get_table_names()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Use Inspector to print the column names and types for Measurement and Station
columns_a = inspector.get_columns('Measurement')
for c in columns_a:
    print(c['name'], c['type'])
print('-'*5)
columns_b = inspector.get_columns('Station')
for c in columns_b:
    print(c['name'], c['type'])
```

* Link Python to the database by creating an SQLAlchemy session.
```python
# Create our session (link) from Python to the DB
session = Session(engine)
```

-----

## Precipitation Analysis
 
* Start by finding the most recent date in the data set.
```python
# Find the most recent date in the data set.
recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
recent_date
```

* Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data.
* Select only the date and prcp values.
```python
# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 
session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date one year from the last date in data set.
one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
prcp_data = session.query(Measurement.date,Measurement.prcp).\
            filter((Measurement.date>=one_year)\
                   &(Measurement.date<=dt.date(2017,8,23))).all()
date = [result[0] for result in prcp_data[:366]]
prcp = [result[1] for result in prcp_data[:366]]
```

* Load the query results into a Pandas DataFrame and set the index to the date column.
* Sort the DataFrame values by date.
```python
# Save the query results as a Pandas DataFrame and set the index to the date column
prcp_df = pd.DataFrame(prcp_data,columns=['date', 'prcp']).sort_values('date').set_index('date')
prcp_df.rename(columns={'prcp':'Precipitation'}, inplace=True)
prcp_df.head()
```
![alt text](https://github.com/gnivil/sqlalchemy-challenge/blob/1e89664cc461889680e45c6ef5adf4ffe0fe1d6a/Images/df.png)

* Plot the results using the DataFrame plot method.
```python
# Use Pandas Plotting with Matplotlib to plot the data
prcp_df.plot(figsize=(10,5), fontsize=10, rot=60)
plt.title(f'Precipitation from {one_year} to {dt.date(2017,8,23)}', fontsize=20)
plt.xlabel('Date')
plt.ylabel('Precipitation')
plt.tight_layout()
plt.savefig('Images/precipitation_data_bargraph.png')
plt.show()
```
![alt text](https://github.com/gnivil/sqlalchemy-challenge/blob/1e89664cc461889680e45c6ef5adf4ffe0fe1d6a/Images/precipitation_data_bargraph.png)


* Use Pandas to print the summary statistics for the precipitation data.
```python
# Use Pandas to calcualte the summary statistics for the precipitation data
precipitation_data = prcp_df['Precipitation'].describe()
summary_statistics = pd.DataFrame(precipitation_data)
summary_statistics
```
![alt text](https://github.com/gnivil/sqlalchemy-challenge/blob/1e89664cc461889680e45c6ef5adf4ffe0fe1d6a/Images/summary_statistics_table.png)

-----

## Station Analysis

* Design a query to calculate the total number of stations in the dataset.
```python
# Design a query to calculate the total number stations in the dataset
station_count = session.query(Station.station).count()
station_count
```

* Design a query to find the most active stations (i.e. which stations have the most rows?).
* List the stations and observation counts in descending order.
* Which station id has the highest number of observations?
```python
# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
                                group_by(Measurement.station).\
                                order_by(func.count(Measurement.station).desc()).all()
active_stations

# Identify the station id with the highest number of observations
most_active_station = active_stations[0][0]
print (f'The most active station id is {most_active_station}.')
print('-'*5)
```

* Using the most active station id, calculate the lowest, highest, and average temperature.
```python
# Calculate lowest temperature
lowest_temp = session.query(func.min(Measurement.tobs)).\
              filter(Measurement.station == most_active_station).scalar()
print(f"Lowest temperature: {lowest_temp} degrees Fahrenheit.")

# Calculate highest temperature
highest_temp = session.query(func.max(Measurement.tobs)).\
              filter(Measurement.station == most_active_station).scalar()
print(f"Highest temperature: {highest_temp} degrees Fahrenheit.")

# Calculate average temperature
avg_temp = session.query(func.avg(Measurement.tobs)).\
              filter(Measurement.station == most_active_station).scalar()
print(f"Average temperature: {round(avg_temp, 2)} degrees Fahrenheit.")
```

* Design a query to retrieve the last 12 months of temperature observation data (TOBS).
* Filter by the station with the highest number of observations.
```python
# Query the last 12 months of temperature observation date for station id USC00519281
most_active_tobs = pd.DataFrame(session.query(Measurement.tobs).\
                                filter((Measurement.station == most_active_station)\
                                        & (Measurement.date >= one_year)\
                                        & (Measurement.date <= dt.date(2017,8,23))).all())
```

* Plot the results as a histogram with bins=12.
```python
# Plot query results as a histogram
most_active_tobs.plot(kind="hist", figsize=(10,5), bins=12, legend=True)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Temperature", fontsize=15)
plt.ylabel("Frequency", fontsize=15)
plt.title(f"Temperature Observations (tobs) at {most_active_station}", fontsize=20)

plt.tight_layout()
plt.savefig("Images/tobs_histogram.png")
plt.show()
```
![alt text](https://github.com/gnivil/sqlalchemy-challenge/blob/1e89664cc461889680e45c6ef5adf4ffe0fe1d6a/Images/tobs_histogram.png)

-----

## Close session

```python
# Close Session
session.close()
```

-----

# Step 2 - Climate App

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.Use Flask to create your routes.
```python
# Import Dependencies
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct
from flask import Flask, jsonify

# Database Setup
# Create engine to hawaii.sqlite
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
inspector = inspect(engine)
inspector.get_table_names()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
# Create an instance of the Flask class
app = Flask(__name__)
```

-----

## /

* Home page.
* List all routes that are available.
```python
@app.route("/")
def home():
    print("Server requested climate app home page...")
    return (
        f"Welcome to the Hawaii Climate App!<br/>"
        f"----------------------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br>"
        f"Note: Replace 'start_date' and 'end_date' with your query dates. Format for querying is 'YYYY-MM-DD'"
    )
```

-----

## /api/v1.0/precipitation

* Convert the query results to a dictionary using date as the key and prcp as the value.
* Return the JSON representation of your dictionary.
```python
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server requested climate app precipitation page...")

    # Create a session from Python to the database
    session = Session(engine)

    # Perform a query to retrieve all the date and precipitation values
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()

    # Close the session
    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp_dict = {} 
    for date, prcp in prcp_data:
        prcp_dict[date] = prcp
    
    # Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)
```

-----

## /api/v1.0/stations

* Return a JSON list of stations from the dataset.
```python
@app.route("/api/v1.0/stations")
def stations():
    print("Server requested climate app station data...")

    # Create a session from Python to the database
    session = Session(engine)
    
    # Perform a query to retrieve all the station data
    results = session.query(Station.id, Station.station, Station.name).all()

    # Close the session
    session.close()

    # Create a list of dictionaries with station info using for loops
    list_stations = []

    for st in results:
        station_dict = {}

        station_dict["id"] = st[0]
        station_dict["station"] = st[1]
        station_dict["name"] = st[2]

        list_stations.append(station_dict)

    # Return a JSON list of stations from the dataset.
    return jsonify(list_stations)
```

-----

## /api/v1.0/tobs

* Query the dates and temperature observations of the most active station for the last year of data.
* Return a JSON list of temperature observations (TOBS) for the previous year.
```python
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server reuested climate app temp observation data ...")

    # Create a session from Python to the database
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data

    # Identify the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
                                        order_by(func.count(Measurement.station).desc()).\
                                        group_by(Measurement.station).\
                                        first()[0]

    # Identify the last date, convert to datetime and calculate the start date (12 months from the last date)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    format_str = '%Y-%m-%d'
    last_dt = dt.datetime.strptime(last_date, format_str)
    date_oneyearago = last_dt - dt.timedelta(days=365)

    # Build query for tobs with above conditions
    most_active_tobs = session.query(Measurement.date, Measurement.tobs).\
                                    filter((Measurement.station == most_active_station)\
                                            & (Measurement.date >= date_oneyearago)\
                                            & (Measurement.date <= last_dt)).all()

    # Close the session
    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year
    return jsonify(most_active_tobs)
```

-----

## /api/v1.0/<start>

* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start 
* When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
```python
@app.route("/api/v1.0/<start>")
def temps_from_start(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date

    print(f"Server requested climate app daily normals from {start}...")

    # Create a function to calculate the daily normals given a certain start date (datetime object in the format "%Y-%m-%d")
    def daily_normals(start_date):

        # Create a session from Python to the database
        session = Session(engine)   

        sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        return session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= func.strftime("%Y-%m-%d", start_date)).group_by(Measurement.date).all()

        # Close the session
        session.close()

    try:
        # Convert the start date to a datetime object for validating and error handling
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")

        # Call the daily_normals function to calculate normals from the start date and save the result
        results = daily_normals(start_date)
        normals=[]

        # Create a for loop to go through row and calculate daily normals
        for temp_date, tmin, tavg, tmax in results:

            # Create an empty dictionary and store results for each row
            temps_dict = {}
            temps_dict["Date"] = temp_date
            temps_dict["T-Min"] = tmin
            temps_dict["T-Avg"] = tavg
            temps_dict["T-Max"] = tmax

            # Append each result's dictionary to the normals list
            normals.append(temps_dict)

        # Return the JSON list of normals
        return jsonify(normals)

    except ValueError:
        return "Please enter a start date in the format 'YYYY-MM-DD'"
```

## /api/v1.0/<start>/<end>
* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range
* When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
```python
@app.route("/api/v1.0/<start>/<end>")
def temps_between(start, end):
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

    print(f"Server requested climate app daily normals from {start} to {end}...")

    # Create a function to calculate the daily normals given certain start and end dates (datetime objects in the format "%Y-%m-%d")
    def daily_normals(start_date, end_date):

        # Create a session from Python to the database
        session = Session(engine)   

        sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        return session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= func.strftime("%Y-%m-%d", start_date)).\
                                   filter(func.strftime("%Y-%m-%d", Measurement.date) <= func.strftime("%Y-%m-%d", end_date)).\
                                    group_by(Measurement.date).all()

        # Close the session
        session.close()

    try:
        # Convert the start date to a datetime object for validating and error handling
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")

        # Call the daily_normals function to calculate normals from the start date and save the result
        results = daily_normals(start_date, end_date)
        normals=[]

        # Create a for loop to go through row and calculate daily normals
        for temp_date, tmin, tavg, tmax in results:

            # Create an empty dictionary and store results for each row
            temps_dict = {}
            temps_dict["Date"] = temp_date
            temps_dict["T-Min"] = tmin
            temps_dict["T-Avg"] = tavg
            temps_dict["T-Max"] = tmax

            # Append each result's dictionary to the normals list
            normals.append(temps_dict)

        # Return the JSON list of normals
        return jsonify(normals)

    except ValueError:
        return "Please enter dates in the following order and format: 'start_date/end_date' i.e. 'YYYY-MM-DD'/'YYYY-MM-DD'"

if __name__ == "__main__":
```

-----