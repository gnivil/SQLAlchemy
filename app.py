#################################################
# Import Dependencies
#################################################
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
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

#################################################
# Flask Setup
#################################################
# Create an instance of the Flask class
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
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