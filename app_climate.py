import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#set start date to 8/31/2018.
st_date_str = "2017-08-31" 
#print(type(st_date_str))
st_date = dt.datetime.strptime(st_date_str, '%Y-%m-%d')

#create varialble to store date as start_date - 1 year
##dateprevyr = dt.date.today() - relativedelta(years=1)
dateprevyr = st_date - relativedelta(years=1)
print("Date from 1 year - prev year date", dateprevyr)


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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query dates and tempereature observations for 1 year from
       Date provided. Date = 08/31/2017.
    """ 
    #set start date. 
    st_date_str = "2017-08-31" 
    #print(type(st_date_str))
    st_date = dt.datetime.strptime(st_date_str, '%Y-%m-%d')
    print(st_date)
    
    # Calculate the date 1 year ago from today.
    dateprevyr = st_date - relativedelta(years=1)
    print(dateprevyr)
    
    precip_data = session.query(Measurement.date,Measurement.prcp).\
                       filter(Measurement.date > dateprevyr).all()
    date_lst=list()
    prcp_lst=list()
    cnt=0
    for row in precip_data:
        cnt+=1
        date_lst.append(row.date)
        prcp_lst.append(row.prcp)
        if cnt % 200 == 0 :
            print(row.date, row.prcp)
    
    #type(precip_data)
    #print("Count of rows: ", str(cnt))
    precip_data_dict={"date":date_lst,"Precipitation":prcp_lst}
    
    return jsonify(precip_data_dict)

@app.route("/api/v1.0/stations")
def stations():
    #Retrieve list of unique stations fro the measurement table. 
    station_list = session.query(Measurement.station).distinct().all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the last 12 months of temperature observation data for this station.
    # Filter by the station with the highest number of observation.
    station_temps = session.query(Measurement.tobs).\
                    filter(Measurement.date > dateprevyr).\
                    all()
    return jsonify(station_temps)
    
if __name__ == '__main__':
    app.run(debug=True)
