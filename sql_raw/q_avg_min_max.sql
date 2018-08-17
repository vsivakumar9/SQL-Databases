select count(*)
      from measurement
where station = 'USC00519397'
  and date    > '2016-08-31';