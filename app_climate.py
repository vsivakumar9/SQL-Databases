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
        f" Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
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


@app.route("/api/v1.0/<start>/<end>")
def tempst(start,end):
    #Calculate minimun temp, avg temp and max temp for date >= start date. TBD
    #st_date_inp  = input("input a start date in yyyy-mm-dd format")
    #end_date_inp = input("input an end  date in yyyy-mm-dd format")
    st_date_inp  = start
    end_date_inp = end
    #Try except for start date.
    try:
        st_date_conv =  dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
        
    #   print(st_date_conv,end_date_conv)
    except:
        print(" Invalid start date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default date. start = 2017-08-21")
        print("start date input: " + st_date_inp)
        print(" ")
        st_date_inp   = '2017-08-21'
        st_date_conv  = dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
        
    #Try except for end date.
    try:
        end_date_conv = dt.datetime.strptime(end_date_inp, '%Y-%m-%d')
    except: 
        print(" Invalid end date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default  end date = current date")
        print("end date input:" + end_date_inp)
        print(" ")
        end_date_conv = dt.datetime.today().strftime('%Y-%m-%d')

    
    print(st_date_conv, end_date_conv)
    #Calculate minimum temp, avg temp and max temp in between  given 
    #start date and end date. 
    Meas_temp_st = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                     filter(Measurement.date >= st_date_conv).\
                     filter(Measurement.date <= end_date_conv).\
                     all()
    return jsonify(Meas_temp_st)

@app.route("/api/v1.0/<start>")
def tempstartonly(start):
    #Calculate minimun temp, avg temp and max temp for date >= start date. 
    #st_date_inp  = input("input a start date in yyyy-mm-dd format")
    st_date_inp  = start
    #Try except for start date.
    try:
        st_date_conv =  dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
    #   print(st_date_conv,end_date_conv)

    except:
        print(" Invalid start date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default date. start = 2017-08-21")
        print("start date input: " + st_date_inp)
        st_date_inp   = '2017-08-21'
        st_date_conv  = dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
        
    print(st_date_conv)
    #Calculate minimum temp, avg temp and max temp for date >= start date.  
    Meas_temp_st = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                     filter(Measurement.date >= st_date_conv).\
                     all()
    return jsonify(Meas_temp_st)


    
if __name__ == '__main__':
    app.run(debug=True)
