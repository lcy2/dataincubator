import datetime, time


#print datetime.datetime.now()

curr_time = datetime.datetime.now()

d_hour = datetime.timedelta(hours = 1)

print time.mktime(datetime.datetime.now().timetuple()) * 1000
rounded_time = curr_time.replace(minute = 0, second = 0, microsecond = 0)
print rounded_time


past_hours = [None] * 24



for i in range(24):
    past_hours[i] = 100* time.mktime((rounded_time - d_hour * (i + 1)).timetuple())

print past_hours