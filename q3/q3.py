import tweepy
import geocoder
from textblob import TextBlob
import math
import json
import sys
from http.client import IncompleteRead
from requests.packages.urllib3.exceptions import ProtocolError
import requests
import MySQLdb
import time

def db_connect(dbname):
    """
    obtain a db cursor obj
    """
    
    db = MySQLdb.connect('localhost',
                        'di_writer',
                        'di_write',
                        dbname,
                        charset='utf8',
                        use_unicode=True,)
    return db



class listener(tweepy.streaming.StreamListener):
    #geo_bb = []
    ctr = 0
    conn = None
    def __init__(self, c):
        #self.geo_bb = bb
        self.conn = c
    
    def on_data(self, data):
        parsed_data = json.loads(data)
        self.ctr += 1

        try:
            print "\rProcessing tweet #%d" % self.ctr,
            
            # only deal with English tweets
            if (parsed_data["lang"] == "en"):
                
                blob = TextBlob(parsed_data['text'])
                print parsed_data['text'].encode('utf-8')
                print blob.sentiment.polarity

                
                
                
                
                
                if parsed_data['place'] != None:
                    print parsed_data['place']['full_name'].encode('utf-8')
                    with self.conn as cursor:
                        twp = parsed_data['place']
                        query = u"""
                        INSERT INTO locations VALUES
                        ('%s', '%s', '%s', '%f', '%s')
                        """ % (twp['id'], self.conn.escape_string(twp['full_name']).encode('utf-8'), twp['country_code'], blob.sentiment.polarity, parsed_data['timestamp_ms'])
                        #print query
                        cursor.execute(query)
                        
                        #print "\n\t Inserted entry for %s." % twp['id']
                        #print '\n'
                else:
                    with self.conn as cursor:
                        query = """INSERT INTO locations (sentiment, dt_ms) VALUES
                            ('%f', '%s')""" % (blob.sentiment.polarity, parsed_data['timestamp_ms'])
                        #print query
                        cursor.execute(query)
                        #print "\n\t Inserted an untagged entry."
                                
        except KeyError: # can't find the 'lang' key
            pass

            
        return True
        
    def on_error(self, status):
        print "Error: %s" % status
        time.sleep(30)
        return True
        
    def on_stall_warning(self, status):
        print "Got Stall Warning message",str(status)
        return True # Don't kill the stream



def getauth():
    consumer_key = 'ky27Yj5H4e2BFo7ivxZ8Y0JU3'
    consumer_secret = 'WWV1R4vgvpUL6L3x1slXG45j40XhjsBYMDpQkwtja4moSqAxTS'

    access_token = 	'792247102243995648-8OL14uhxm34Fmy2q8Wl8kL4Arwg5VZN'
    access_token_secret = 'JlWwWTwEmESbX8rg4XzwWNinK1N7DntzpGdYE4hiZeiqu'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    return auth
    
def get_bounding_box(location, dist):
    """
    given a location and a distance (in km),
    return the southwest corner
    and the northeast corner in a tuple
    """
    
    
    geo = geocoder.google(location)

    
    lat = geo.latlng[0]
    lon = geo.latlng[1]
    
    print lat, lon
    
    # use a simple estimation
    delta_y = dist / 111.111
    delta_x = dist / (111.111 * math.cos(math.radians(lat)))
    
    return lat-delta_y, lon-delta_x, lat+delta_y, lon+delta_x

def in_bounding_box(geolist, bb):
    #print bb
    if geolist == None:
        return False
    elif (bb[0] <= geolist['coordinates'][0] <= bb[2] and
          bb[1] <= geolist['coordinates'][1] <= bb[3]) :
        return True
        
        # still need to implement edge case of lat ~ 0
    return False
    


if __name__ == "__main__":

    #geobb = get_bounding_box('New York City, NY', 50)
    #print geobb
    reload(sys)
    sys.setdefaultencoding('utf8')
    conn = db_connect('dataincubator')
    while True:

        try:
            twstream = tweepy.streaming.Stream(getauth(), listener(conn))
            twstream.filter(track=["a", "the", "i", "to", "and", "is", "in", "it", "can", "you", "u"], stall_warnings=True)
        except (ProtocolError, IncompleteRead):
            print "\nEncountering Incomplete Read. Move on."
            time.sleep(30)
            continue
        except UnicodeEncodeError:
            print "\nUnicode problem. Move on."
            time.sleep(30)
            continue





