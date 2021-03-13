import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask set up
app = Flask(__name__)

##################################
# Flask Routes
##################################

@app.route("/")
def home():
    """List all routes that are available"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    #query precipitation data
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    all_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).order_by(Measurement.date).all()

    session.close()

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation_data = []
    for date, prcp in all_precipitation:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp

    #Return the JSON representation of your dictionary.
    return jsonify(precipitation_data)



@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    #query all station data
    all_stations = session.query(Station.station, Station.name).all()

    session.close()

    #convert to normal list
    station_list = list(all_stations)

    #Return a JSON list of stations from the dataset.
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    last_year_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year).\
        order_by(Measurement.date).all()

    session.close()

    #convert to normal list
    tobs_list = list(last_year_tobs)

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(tobs_list)



@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    session.close()

    #convert to normal list
    start_temp_list = list(start)

    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range.
    return jsonify(start_temp_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()

    session.close()

    #convert to normal list
    start_end_list = list(start_end)

    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)