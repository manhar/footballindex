import sys
#sys.path.insert(0, '../utilities')
import add_subdir_to_path , my_utilities

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import decimal
import logging
from smsapi import send_sms_alert
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
#output_dir=my_config.ConfigSectionMap("logging")['output_dir']

#Set the API link
api_link=my_config.ConfigSectionMap("football")['api_link']


def coalesce(dic, lkp_key, default_value):
    if lkp_key in dic:
        return str((dic[lkp_key]))
    else:
        return default_value



#function to get data in a pipe delimited format
def prepare_dict(datetime_id,df):

    result=""
    result_db=[]
    output_dict=dict();
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

            output_dict[p_id]={'datetime':datetime_id, 'name':p_name , 'rank':p_rank, 'score':p_buy , 'scoreSell':p_sell, 'team':p_team, 'trend':p_trend}



        except Exception as e:
            print(str(e))
    return output_dict

def parse_api(api_link):
    cur_datetime=datetime.today()
    datetime_id=cur_datetime.strftime("%Y-%m-%d %H:%M:%S")
    try:

        #load data in dataframe
        df=pd.read_json(api_link)
        #Set variables
        dic=prepare_dict(cur_datetime, df)
        #print(dic['raphael-varane'])

    except Exception as e:
        print (  datetime_id +"\tError connecting to API:" + str(e) )
    return dic


#main
#parse_api(api_link)
