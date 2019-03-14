import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path , my_utilities

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import decimal
import logging
from smsapi import send_sms_alert
from mysql_populate_table import insert_d_player_list
import my_config
import ssl

## Disable SSL certificate check
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

#Set Logging directories
output_dir=my_config.ConfigSectionMap("logging")['output_dir']

#Set the API link
api_link=my_config.ConfigSectionMap("football")['api_link']


def coalesce(dic, lkp_key, default_value):
    if lkp_key in dic:
        return str((dic[lkp_key]))
    else:
        return default_value



#function to get data in a pipe delimited format
def get_data(datetime_id,df,txn_date,txn_time,data_file):

    result=""
    result_db=[]
    for i in df["items"]:
        trend_date=datetime.today()
        days_to_subtract=0
        while trend_date.strftime('%Y%m%d') not in i["history"]:
            trend_date=datetime.today() - timedelta(days=days_to_subtract)
            days_to_subtract+=1

        trend_date=trend_date.strftime('%Y%m%d')
        try:

            #x=1/0
            p_id  =coalesce(i,"id","-999")
            p_name=coalesce(i,"name", "ZZZZ")
            p_rank=coalesce(i,"rank", "-999")
            p_buy =coalesce(i,"score", "-999")
            p_sell=coalesce(i,"scoreSell", "-999")
            p_team=coalesce(i,"team","ZZZ")#.decode('utf-8')
            p_trend=coalesce(i["history"][trend_date],"trending","-999")

            result+=(
                  p_name +"|"+
                  p_rank +"|"+
                  p_team +"\n"
                  )

            result_db.append((
                  p_id ,
                  p_name ,
                  p_team
                  ))


        except Exception as e:
            logging.debug("error occured while parsing json file. : " + str(e))
            print(str(e))
    insert_d_player_list(result_db)

def acquire_player_data():
    cur_datetime=datetime.today()
    datetime_id=cur_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print(datetime_id +"\tAcquiring playerdata feed")
    try:

        #load data in dataframe
        df=pd.read_json(api_link)
        #Set variables
        txn_date=cur_datetime.strftime('%Y%m%d')
        txn_time=cur_datetime.strftime('%H%M%S')

        data_file=output_dir+"/data/"+"playerdata"+txn_date+".txt"
        playerdata_acquisition_date=output_dir+"/data/playerdata_acquisition_date.dat"
        dump_file=output_dir+"/dump/"+"playerdata_api_dump"+txn_date+"_"+txn_time+".txt"
        logfile=output_dir+"/logs/"+"playerdata_"+txn_date+".log"
        logging.basicConfig(filename=logfile,format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S',level=logging.DEBUG)
        try:
            logging.info("Starting Data Aquisition")
            get_data(datetime_id, df, txn_date, txn_time,data_file)
            my_utilities.write_to_file( playerdata_acquisition_date, datetime_id)
            logging.info("Data Aquisition completed successfully, going to sleep...")
        except Exception as e:
            logging.debug("Error encoutered during data aquisition:" + str(e))
            df.to_csv(dump_file)
    except Exception as e:
        logging.debug("Error connecting to API:" +str(e))
        #send_sms_alert("Error football feed" + str(e))
        print (  datetime_id +"\tError connecting to API:" + str(e) )



#main
acquire_player_data()