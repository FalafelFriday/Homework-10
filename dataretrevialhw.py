import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


Measurements = Base.classes.measurement
Station = Base.classes.station

session=Session(engine)




app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"

    )


@app.route("/api/v1.0/precipitation")
def prcpa():

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date > last_year).\
        order_by(Measurements.date).all()

    rain_totals = []
    for rain in Measurements:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

@app.route("/api/v1.0/stations")
def stt():
    stationq=session.query(Station.name,Station.station)
    name = []
    for stationq in Station:
        row = {}
        row["name"] = stationq[0]
        row["station"] = stationq[1]
        name.append(row)
    return jsonify(name)

@app.route("/api/v1.0/tobs")
def tbs():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    temp = session.query(Measurements.date,Measurements.tobs).\
        filter(Measurements.date > last_year).\
            order_by(Measurements.date).all()
    temperature_total=[]
    for temp in Measurements:
        row={}
        row["date"]=temp[0]
        row["tobs"]=temp[1]
        temperature_total.append(row)
    return jsonify(temperature_total)

@app.route("/api/v1.0/<start>")
def tr1p():
    start = dt.date(2017,7,4)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).all()
    trip=np.ravel(trip_data)
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def tr2p():
    start=dt.date(2017,7,4)
    end=dt.date(2017,8,4)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip2=np.ravel(trip_data)
    return jsonify(trip2)


if __name__ == "__main__":
    app.run(debug=True)