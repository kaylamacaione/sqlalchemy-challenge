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
    #Create session link from python to DB
    session = Session.(engine)

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    """


@app.route("/api/v1.0/stations")


@app.route("/api/v1.0/tobs")


@app.route("/api/v1.0/<start>")


@app.route("/api/v1.0/<start>/<end>")


