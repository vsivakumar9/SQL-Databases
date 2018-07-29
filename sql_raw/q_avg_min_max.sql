select min(tobs), max(tobs), avg(tobs) 
      from measurement
where station = 'USC00519281'