import MySQLdb
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import json
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from pytz import timezone


def db_connect(dbname):
    """
    obtain a db cursor obj
    """
    
    db = MySQLdb.connect('localhost',
                        'di_writer',
                        'di_write',
                        dbname)
    return db
    
def res_gen(cursor, size = 1000):
    """
    this is a generator
    such that it doesn't have to read in
    all records at the same time
    while also not reading records 1 by 1 
    at turtle speed
    """
    
    while True:
        results = cursor.fetchmany(size)

        if not results:
            break
        for result in results:

            yield result
    
def get_time_array():
    curr_time = datetime.datetime.now()

    d_hour = datetime.timedelta(hours = 1)

    rounded_time = curr_time.replace(minute = 0, second = 0, microsecond = 0)
    past_hours = [1000* time.mktime(curr_time.timetuple())]

    for i in range(49):
        past_hours.append(1000* time.mktime((rounded_time - d_hour * (i)).timetuple()))
        
    #print "Time Array:"
    #print past_hours
    return past_hours


    
def db_collection(conn):
    # get the starting timestamp for the past 48 hours
    # collapse that into 24 hours
    t_array = get_time_array()
    res_array = []
    
    with conn as cursor:
        query = "SELECT *, COUNT(*) as counts FROM locations GROUP BY place_id ORDER BY counts DESC LIMIT 11"
        cursor.execute(query)
        

        
        # for each location:
        for row in res_gen(cursor):
            place_id = row[0]
            mini_res_array = []
            with conn as loc_cursor:
                for hour_index in range(len(t_array)-1):

                    if place_id == 0:
                        query2 = "SELECT SUM(sentiment) as avg_s, COUNT(sentiment) as sum_s FROM locations WHERE (dt_ms BETWEEN '%d' AND '%d') ORDER BY dt_ms DESC" % (place_id, t_array[hour_index+1], t_array[hour_index])
                    else:
                        query2 = "SELECT SUM(sentiment) as avg_s, COUNT(sentiment) as sum_s FROM locations WHERE (place_id = '%s' AND (dt_ms BETWEEN '%d' AND '%d')) ORDER BY dt_ms DESC" % (place_id, t_array[hour_index+1], t_array[hour_index])
                    print "Processing %s at T-%d hour." % (row[1], hour_index)
                    loc_cursor.execute(query2)
                    loc_res = loc_cursor.fetchone()
                    print loc_res
                    
                    # structure of each row [place_id, place_name, the hour, avg_sentiment, total counts]
                    rt_array = [place_id, row[1], t_array[hour_index], loc_res[0] if loc_res[0] != None else 0, loc_res[1]]
                    mini_res_array.append(rt_array)
                    
                    
            # turn the 48 hour record into 24 unique hour marks
            # for anything more than 24 hours away, add 24 hours
            
            for i in range(24,len(mini_res_array)):
                mini_res_array[i % 24][3] += mini_res_array[i][3]
                mini_res_array[i % 24][4] += mini_res_array[i][4]
            
            for res in mini_res_array[:24]:
                res[3] = res[3]/res[4]
            
            res_array.append(mini_res_array[:24])
            print 'Final result array:'
            print [res[3] for res in mini_res_array[:24]]
    return res_array
                    
                        
def cache_data(results, filename):
    with open(filename, 'w') as fn:
        json.dump(results, fn)
                        
def load_data(filename):
    res = []
    with open(filename, 'r') as fn:
        res = json.load(fn)
                        
    return res

def geo_tz_shift(res):
    """
    transform the hours into real time in local tz
    """
    
    
    geolocator = Nominatim()
    gv = GoogleV3()
    geo = gv.geocode(res[0][1])
    print geo
    
    if (geo == None):
        geo = gv.geocode("Philadelphia, PA")

    tz = gv.timezone((geo.latitude, geo.longitude))
    
    for res_row in res:
        new_dt = tz.localize(datetime.datetime.utcfromtimestamp(res_row[2]/1000))
        res_row.append(new_dt.hour)
        
    
    
if __name__ == "__main__":
    conn = db_connect('dataincubator')
    #results = db_collection(conn)
    #cache_data(results, 'tmpdump')
    
    results2 = load_data('tmpdump')
    plt.figure(1)
    #plt.subplot(2,1, 1)
    
    #for result in results:
    #    res = np.array(result)
    #    plt.plot(res[:,2],res[:,3], 'k')
    
    
    #plt.subplot(2,1,2)
    
    for result in results2:

        geo_tz_shift(result)
        res = np.array(result)
        
        sorted_res = res[np.array([int(x) for x in res[:,5]]).argsort()]
        print sorted_res
        plt.plot(sorted_res[:,5],sorted_res[:,3], '-')
        
        # beautification
        axes = plt.gca()
        axismin =  min(float(x) for x in res[:,3] if x != None)
        axismax =  max(float(x) for x in res[:,3])
        axes.set_ylim([axismin - (axismax - axismin) * 0.1, axismax + (axismax - axismin) * 0.1])
        axes.set_xlim([0,23])
        plt.xlabel("Hour of the Day")
        plt.ylabel("Average Sentiment")
        if res[0,1] != 'untagged':
            plt.title("Average Sentiment in %s" % res[0,1])
        else:
            plt.title("Average Sentiment in the World in EDT")
        
        plt.show()
        
    

    
    