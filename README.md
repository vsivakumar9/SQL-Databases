

```python
#%matplotlib notebook
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import seaborn as sns
#Import Dependencies. 
import numpy as np
import pandas as pd
from collections import defaultdict
import datetime as dt
#import datetime
from dateutil.relativedelta import relativedelta
```

# Reflect Tables into SQLAlchemy ORM


```python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.inspection import inspect
from sqlalchemy import desc
```


```python
#create engine to connect to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found.
Base.classes.keys()
```




    ['measurement', 'station']




```python
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#start date = 05/26/2017
#end date = 6/3/2018
st_date_str = "2017-08-23" 
print(type(st_date_str))
st_date = dt.datetime.strptime(st_date_str, '%Y-%m-%d')
print(st_date)
```

    <class 'str'>
    2017-08-23 00:00:00
    

# Exploratory Climate Analysis


```python
# Calculate the date 1 year ago from today.
#create varialble to store date as start_date - 1 year
##dateprevyr = dt.date.today() - relativedelta(years=1)
dateprevyr = st_date - relativedelta(years=1)
print(dateprevyr)
##select date, prcp from measurement where date > dateprevyr( current date - 1 yr)
# Design a query to retrieve the last 12 months of precipitation data and plot the results.
#sel=["date","prcp"]
precip_data = session.query(Measurement.date,Measurement.prcp).\
                   filter(Measurement.date > dateprevyr).all()
date_lst=list()
prcp_lst=list()
cnt=0
for row in precip_data:
    cnt+=1
    date_lst.append(row.date)
    prcp_lst.append(row.prcp)
    if cnt % 500 == 0 :
        print(row.date, row.prcp)

type(precip_data)
print("Count of rows: ", str(cnt))
precip_data_dict={"date":date_lst,"Precipitation":prcp_lst}

```

    2016-08-23 00:00:00
    2017-01-10 0.0
    2017-08-16 0.0
    2017-07-26 0.0
    2016-12-30 2.37
    Count of rows:  2223
    


```python
#convert dictionary to a dataframe. 
precip_data_df = pd.DataFrame(precip_data_dict)
precip_data_df = precip_data_df.rename(columns={"prcp":"Precipitation"})
precip_data_df.head(1)
#print(precip_data_df.count())
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Precipitation</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.08</td>
      <td>2016-08-24</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Review data and info for nulls etc.
precip_data_null= precip_data_df[precip_data_df.isnull().any(axis=1)]
precip_data_null.tail(3)
# Drop null values for precipitation values.
precip_data_df = precip_data_df.dropna(how="any")
# Sort the dataframe by date
precip_data_df = precip_data_df.sort_values("date")
#precip_data_df.info()

```


```python
#Review data in dataframe.
#precip_data_df.head(1)
# set index as the date. 
#precip_data_df.reset_index(inplace=True,drop=True)
precip_data_df.set_index("date",drop=True,inplace=True)
precip_data_df.columns
precip_data_df.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Precipitation</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-08-19</th>
      <td>0.09</td>
    </tr>
    <tr>
      <th>2017-08-20</th>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-08-21</th>
      <td>0.56</td>
    </tr>
    <tr>
      <th>2017-08-22</th>
      <td>0.50</td>
    </tr>
    <tr>
      <th>2017-08-23</th>
      <td>0.45</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Display a few beginning rows.
precip_data_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Precipitation</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-24</th>
      <td>0.08</td>
    </tr>
  </tbody>
</table>
</div>




```python
#reset index to create date as a column 
precip_data_df1=precip_data_df.copy()
precip_data_df1.reset_index(inplace=True,drop=False)
precip_data_df1.head(1)
precip_data_df1.tail(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>Precipitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2222</th>
      <td>2017-08-23</td>
      <td>0.45</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Plot data from the dataframe using the pandas line plot.
##plt.savefig("/Images/datevsprecip_vsk.png").# Rotate the xticks for the dates.
precip_data_df1.plot(x="date",y="Precipitation",kind="line",ax=None,legend=True,
                     title="Hawaii - Date vs precipitation ")

plt.savefig("Images\datevsprecip_vsk.png")
plt.show()
```


![png](output_12_0.png)



```python
# Use Pandas to calcualte the summary statistics for the precipitation data
precip_data_df2=precip_data_df1[["date","Precipitation"]]
precip_data_df2.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Precipitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2015.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.176462</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.460288</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.020000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.130000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>6.700000</td>
    </tr>
  </tbody>
</table>
</div>




```python
# How many stations are available in this dataset? Calculation number of stations in the station table. 
#precip_data_stations = precip_data_df1["station"].unique()
#precip_data_stations
station_data = session.query(Station.station).distinct().all()
#station_list = session.query(Measurement.station).distinct().all()
#station_list
#print a few rows form the query results. 
cnt=0
for row in station_data:
    #print(row.station)
    cnt+=1
    if cnt > 10:
        break
# How many stations are available in this dataset?. Calculating # of stations in the full measurement table.
station_cnt = session.query(Measurement.station).distinct().count()
station_cnt
        

```




    9




```python
## Query to determine what are the most active stations..
# List the stations and the counts in descending order.
station_cnts_desc = session.query(Measurement.station,func.count(Measurement.station).label("scount")).\
                    group_by(Measurement.station).\
                    order_by(desc("scount")).\
                    all()
station_cnts_desc          
```




    [('USC00519281', 2772),
     ('USC00519397', 2724),
     ('USC00513117', 2709),
     ('USC00519523', 2669),
     ('USC00516128', 2612),
     ('USC00514830', 2202),
     ('USC00511918', 1979),
     ('USC00517948', 1372),
     ('USC00518838', 511)]




```python
#Determine station with highest observations and assign values for highest count to variables for use. 
(station_max , count_max) = station_cnts_desc[0]
print(station_max,count_max)
```

    USC00519281 2772
    


```python
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature for the most active station?

station_temp_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                     filter(Measurement.station == station_max).\
                     all()
station_temp_stats
```




    [(54.0, 85.0, 71.66378066378067)]




```python
#Review value of dateprevyr.
print(dateprevyr)
# Design a query to retrieve the last 12 months of temperature observation data (tobs). Note this counts only the tobs count 
# and does not include the prcp values. 
from sqlalchemy import desc
station_temp_cnts = session.query(Measurement.station,func.count(Measurement.tobs).label("count_tobs")).\
                     filter(Measurement.date > dateprevyr).\
                     group_by(Measurement.station).\
                     order_by(desc("count_tobs")).\
                     all()
station_temp_cnts[0:2]
# Choose the station with the highest number of temperature observations.
#(station_maxobs, station_maxcnt) = station_temp_cnts[0]
#print(station_maxobs,station_maxcnt)
```

    2016-08-23 00:00:00
    




    [('USC00519397', 360), ('USC00519281', 351)]




```python
# Query the last 12 months of temperature observation data for this station.
# Filter by the station with the highest number of observation and plot the results as a histogram.
# NOTE: Based on discussion with TA(Aiyana), station with max count of  observations(USC00519281) was used here instead of the 
# counts for tobs field only from the database. 

station_temps = session.query(Measurement.tobs).\
                     filter(Measurement.date > dateprevyr).\
                     filter(Measurement.station ==  station_max).\
                     all()
station_temps[0:3]
#Create a  lists for the temperatures. Will be used later to convert to dataframe and plot. 
temp_list=list()
frequency=list()
cntrows=0
for row in station_temps:
    cntrows+=1
    temp, = row
    temp_list.append(temp)

print(str(len(temp_list)))

```

    351
    


```python
##Create temperature bins.
#bins=[]
#binstemp = [60.0,62.5,65.0,67.5,70.0,72.5,75.0,77.5,80.0,82.5,85.0,87.5,90.0]
#labelstemp= [60.0,62.5,65.0,67.5,70.0,72.5,75.0,77.5,80.0,82.5,85.0,87.5,90.0]
temp_freq_dict={"Temperature":temp_list }
temp_freq_df=pd.DataFrame(temp_freq_dict)
temp_freq_df.tail(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Temperature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>349</th>
      <td>76.0</td>
    </tr>
    <tr>
      <th>350</th>
      <td>79.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Plot results as a higtogram with bins=12.
temp_freq_df.plot.hist(by="Temperature", bins=12,title="Hawaii - Temperature  vs Frequency" )
plt.savefig("Images\Temperature-vs-Frequency.png")
plt.show()   
```


![png](output_21_0.png)



```python
#print(temp_freq_df.min())
#print(temp_freq_df.max())
#temp_freq_df.head()
#Calculate minimun temp, avg temp and max temp for date >= start date. TBD
st_date_inp  = input("input a start date in yyyy-mm-dd format")
end_date_inp = input("input an end  date in yyyy-mm-dd format")
try:
    st_date_conv =  dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
    end_date_conv = dt.datetime.strptime(end_date_inp, '%Y-%m-%d')
    print(st_date_conv,end_date_conv)
  
except:
    print("invalid date or date format. Please input valid date in yyyy-mm-dd format. Using default dates. ")
    print(st_date_inp)
    st_date_inp   = '2017-08-21'
    st_date_conv  = dt.datetime.strptime(st_date_inp, '%Y-%m-%d')
    end_date_conv = dt.datetime.today().strftime('%Y-%m-%d')
    print(st_date_conv, end_date_conv)
```

    input a start date in yyyy-mm-dd formatsadf
    input an end  date in yyyy-mm-dd formatsadf
    invalid date or date format. Please input valid date in yyyy-mm-dd format. Using default dates. 
    sadf
    2017-08-21 00:00:00 2018-08-04
    


```python
#Test -  Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
# for a given start or start-end range.
#Calculate minimun temp, avg temp and max temp in between  given start date and end date. 

Meas_temp_st = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                     filter(Measurement.date >= st_date_conv).\
                     filter(Measurement.date <= end_date_conv).\
                     all()
                             
print(Meas_temp_st)
                    
```

    [(76.0, 80.14285714285714, 82.0)]
    


```python
# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
# def calc_temps(start_date, end_date):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
    
#     return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
# print(calc_temps('2012-02-28', '2012-03-05'))
```


```python
# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.

```


```python
# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

```


```python
# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation


```

## Optional Challenge Assignment


```python
# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

# def daily_normals(date):
#     """Daily Normals.
    
#     Args:
#         date (str): A date string in the format '%m-%d'
        
#     Returns:
#         A list of tuples containing the daily normals, tmin, tavg, and tmax
    
#     """
    
#     sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
#     return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
# daily_normals("01-01")
```


```python
# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date

```


```python
# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index

```


```python
# Plot the daily normals as an area plot with `stacked=False`

```
