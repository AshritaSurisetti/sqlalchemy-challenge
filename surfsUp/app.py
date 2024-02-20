# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with = engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the API Homepage<br/><br/><br/>" 
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).all()
    prcp_dict = dict(prcp_scores)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temparaturess():
    #took the value from my previous analysis in Jupyter notebook
    most_active_station = "USC00519281"
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_obs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).filter(Measurement.station == most_active_station).all()
    tobs_dict = dict(temp_obs)
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    temps = []
    for min,avg,max in results:
        temps_dict = {}
        temps_dict["Min"] = min,
        temps_dict["Avg"] = avg,
        temps_dict["Max"] = max,
        temps.append(temps_dict)

    return jsonify(temps_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                                    filter(Measurement.date <= end).all()
    temps = []
    for min,avg,max in results:
        temps_dict = {}
        temps_dict["Min"] = min,
        temps_dict["Avg"] = avg,
        temps_dict["Max"] = max,
        temps.append(temps_dict)

    return jsonify(temps_dict)

if __name__ == "__main__":
    app.run(debug=True)