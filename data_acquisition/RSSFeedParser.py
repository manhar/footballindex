#!/usr/bin/python
import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path

import feedparser
import time
from subprocess import check_output
import sys
from dateutil.parser import *
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
import hashlib
from mysql_populate_table import insert_f_daily_news,check_new_hash_key_exists, getLatestNewsKey
from smsapi import send_sms_alert
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import logging
import my_config

feed_name = 'EXPRESS'
url = 'http://www.goal.com/en-gb/feeds/news?fmt=rss'


#declare output directory
output_dir=my_config.ConfigSectionMap("logging")['output_dir']

#create a dictionary of the RSS feeds to collect news from
feed_dict={"DAILY_EXPRESS":'http://feeds.feedburner.com/daily-express-football-news?format=xml'
           ,"METRO":'http://metro.co.uk/sport/football/feed/'
           ,"DAILY_STAR":"http://feeds.feedburner.com/daily-star-football?format=xml"
           ,"DAILY_MAIL_TRANSFER_NEWS":"http://www.dailymail.co.uk/sport/transfernews/index.rss"
           ,"DAILY_MAIL_LATEST_FOOTBALL_STORIES":"http://www.dailymail.co.uk/sport/football/articles.rss"
           ,"TALKSPORT_FOOTBALL":"http://talksport.com/rss/sports-news/football/feed"
           ,"TALKSPORT_FOOTBALL_PREMIER_LEAGUE":"http://talksport.com/rss/football/premier-league/feed"
           ,"TALKSPORT_TRANSFER_NEWS":"http://talksport.com/rss/sports-news/transfer-rumours/feed"
           ,"GOAL":"http://www.goal.com/en-gb/feeds/news?fmt=rss"
           ,"INDEPENDENT":"http://www.independent.co.uk/sport/football/rss"
           ,"GUARDIAN_FOOTBALL":"https://www.theguardian.com/football/rss"
           ,"MIRROR":"http://www.mirror.co.uk/sport/football/rss.xml"

           }

#
# function to get the current time
#
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

#log_news in db
def log_news_in_db(hash_key , feed_name ,title,link,comments,description,pubdate,pos_score, neg_score):

    #curr_time=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print ("inserting news from", feed_name)
    values=[(hash_key , feed_name ,title,link,comments,description,pubdate,pos_score, neg_score)]
    insert_f_daily_news(values)




#function to write news to a file
def populate_db(table_name, row):
    result=False
    try:
        with open(table_name, 'ab') as datafile:
                datafile.write(row)
                result=True
        datafile.close()
    except Exception as e :
        print("Error while populating DB "+str(e))
    return result

# return true if the title is in the database with a timestamp > limit
def post_is_in_db_with_old_timestamp(title):
#    with open(db, 'r') as database:
#        for line in database:
#            if title in line:
#                ts_as_string = line.split('|', 1)[1]
#                ts = long(ts_as_string)
#                if current_timestamp - ts > limit:
#                    return True
    return False



def acquire_feed_data(feed_name, url, hash_key_array):
    ''' This method acquires data from a RSS URL link. News which are new are inserted into the database '''
    # get the feed data from the url
    feed = feedparser.parse(url)

    for post in feed.entries:
        # if post is already in the database, skip it
        #Get post attributes (Tite, pubdate, descriptopn...ect) from the news feed
        title = post.title#.encode('utf-8')
        comment= "COMMENTS ARE SUPRESSED"#post.comments
        link= post.link#.encode('utf-8')
        pubdate=str(parse(post.published).strftime('%Y-%m-%d %H:%M:%S'))
        description = str(post.description.encode("utf=8"))
        hash_key= hashlib.md5(''.join(( title,pubdate)).encode()).hexdigest()

        #if not check_new_hash_key_exists(hash_key):
        if not hash_key in hash_key_array:
            #posts_to_print.append(row)

            #initialize sentimental analysis class
            sia=SIA()
            #apply sentimental anaylysis algorithm on news Title and derive positve/negative score
            sentimental_score=sia.polarity_scores(title)
            pos_score=str(sentimental_score["pos"])
            neg_score=str(sentimental_score["neg"])

            #prepare row to be inserted inserted in DB
            row=(u' '.join((hash_key,"|",feed_name,"|" ,title,"|" ,link,"|" ,comment,"|" ,description,"|" ,pubdate,"|" ,pos_score,"|" ,neg_score,"\n"))).encode('utf-8')
            #insert row into database
            log_news_in_db(hash_key , feed_name ,title.replace("'",""),link.replace("'",""),comment.replace("'",""),description,pubdate , pos_score, neg_score)



def process_feeds():
    ''' This method loops through the list of RSS URL provided in feed dictionary. For each feed, it parses the URL and insert the news on the database
    if not already exist'''

    #Set variables
    cur_datetime=datetime.today()
    txn_date=cur_datetime.strftime('%Y%m%d')
    txn_time=cur_datetime.strftime('%H%M%S')

    logfile=output_dir+"/logs/"+"RSSFeedParser_"+txn_date+".log"
    logging.basicConfig(filename=logfile,format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S',level=logging.DEBUG)


    #get  news keys which are 24 hours old
    hash_key_array=getLatestNewsKey(24);
    for feed, url in feed_dict.items():
        cur_datetime=datetime.today()
        logging.info(" Acquiring news feed from "+feed)
        try:
            acquire_feed_data(feed, url, hash_key_array)
            logging.info(" News aquired for "+feed)
        except Exception as e:
            logging.info(" Error football  news feed"+ feed+ " " + str(e))
            #send_sms_alert("Error football  news feed"+ feed+ " " + str(e))


#main
process_feeds()