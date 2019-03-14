import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path

import pandas as pd
import matplotlib.pyplot as plt
import glob
from mysql_populate_table import get_pos_news_date , get_neg_news_date, getplayerscore, getAllplayerscore
from dateutil import parser
import sys
from datetime import datetime, timedelta




player_name=  "gareth-bale"#"javier-hernandez"
player_surname="bale"#"hernandez"

last24Hour = (datetime.now() - timedelta(hours = 24)).strftime('%Y-%m-%d %H:%M:%S')
last12Hour = (datetime.now() - timedelta(hours = 12)).strftime('%Y-%m-%d %H:%M:%S')
last1Hour = (datetime.now() - timedelta(hours = 1)).strftime('%Y-%m-%d %H:%M:%S')
last7days =  (datetime.now() - timedelta(days = 7)).strftime('%Y-%m-%d %H:%M:%S')
last1month = (datetime.now() - timedelta(weeks = 1)).strftime('%Y-%m-%d %H:%M:%S')

all_scores=getAllplayerscore(120)


def find_player_score2(df,player, time ):
    score=all_scores.loc[(all_scores.txn_datetime >=time) & (all_scores.player_id ==player)].iloc[0]["bprice"]
    return  score



#get the maximum date
max_dt=all_scores.txn_datetime.max()
latest_score=all_scores.loc[all_scores.txn_datetime == max_dt]

def calculate_pct_change():
    change_24_hrs={}
    for player in latest_score.player_id.unique():
        #get player's latest price
        latest_price= float(str(latest_score.loc[latest_score.player_id==player]["bprice"].values[0]))
        previous_price=all_scores.loc[(all_scores.txn_datetime >=last24Hour) & (all_scores.player_id ==player)].iloc[0]["bprice"]
        pct_change = ( latest_price - previous_price)/previous_price
        change_24_hrs[player]=pct_change
        #print (player , str(latest_price) , str(previous_price) , str(pct_change)  )

    s=pd.Series(change_24_hrs,name= 'val')
    s.index_name="player"
    s.reset_index()
    return s

x=calculate_pct_change()

x.plot(kind="hist")

sys.exit()


 #get scores of player
player=player_all_time_pct_change.loc[player_all_time_pct_change.player_id==player_name, ["bpriceChange", "txn_datetime"]].sort_values(by=["txn_datetime"] , ascending=True)

#print(player.sort(["time_axis"] , ascending=True))

#zlatan_b_price=scores[".as_matrix(columns=zlatan.columns[5:6])
player_b_price=player["bpriceChange"].values
time_axis=player["txn_datetime"].values
fig,ax = plt.subplots()
#plot player buying price over time
ax.plot(time_axis,player_b_price, "b-", label=player_name)

#news=[min(player_b_price),max(player_b_price)]
#
#news_time_pos_df=get_pos_news_date(player_surname)
##for each positive news, get the news time
#for k, v in news_time_pos_df.iterrows():
#    #convert string datetime to datetime
#    t=parser.parse(v[1]).strftime("%Y%m%d%H%M%S")
#    news_id=v[0]
#    news_time=[t,t]
#    ax.plot(news_time,news, "g-", label=news_id)
#
#
#news_time_neg_df=get_neg_news_date(player_surname)
##for each positive news, get the news time
#for k, v in news_time_neg_df.iterrows():
#    #convert string datetime to datetime
#    t=parser.parse(v[1]).strftime("%Y%m%d%H%M%S")
#    news_id=v[0]
#    news_time=[t,t]
#    ax.plot(news_time,news, "r-", label=news_id)

 #get negative news time for player
#news_time_pos_array=get_neg_news_date(player_surname)
#for each positive news, get the news time
#for i in news_time_pos_array:
#    #convert string datetime to datetime
#    t=parser.parse(i[1]).strftime("%Y%m%d%H%M%S")
#    news_id=i[0]
#   news_time=[t,t]
#   ax.plot(news_time,news, "r-", label=news_id)


#ax.plot(news_time,news, "r-", label="news")
plt.ylabel(player_name)
#legend = ax.legend(loc='upper left', shadow=True)
plt.gcf().autofmt_xdate()
plt.show()

