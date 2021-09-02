# Surfs Up!

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

-----

# Step 1 

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

-----

## Climate Analysis and Exploration

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

* Important: Don't forget to close out your session at the end of your notebook.

-----

## Precipitation Analysis
 
*Start by finding the most recent date in the data set.
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

* Use Pandas to print the summary statistics for the precipitation data.
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




```python

```
-----