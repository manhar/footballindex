import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path


import pandas as pd
import matplotlib.pyplot as plt
import glob
from mysql_populate_table import get_pos_news_date , get_neg_news_date, getplayerscore,getNewsPubDateByPlayer
from dateutil import parser
import my_config

t=my_config.ConfigSectionMap("logging")['output_dir']


player_id="cristiano-ronaldo"  ## "antoine-griezmann"#"radja-nainggolan"
player_surname="ronaldo"
path =r'/Users/ashish/Documents/footballindex/data/' # use your path
allFiles = glob.glob(path + "*.txt")
team="man utd manchester united"

scores=getplayerscore(player_id)
news_date=getNewsPubDateByPlayer(player_id, team)

player=scores.loc[scores.player_id==player_id, ["bprice",
                                                  "last_1min_pct_change",
                                                  "last_2min_pct_change",
                                                  "last_3min_pct_change",
                                                  "last_4min_pct_change",
                                                  "last_5min_pct_change",
                                                  "last_6min_pct_change",
                                                  "last_7min_pct_change",
                                                  "last_8min_pct_change",
                                                  "last_9min_pct_change",
                                                  "last_10min_pct_change",
                                                  "what_to_do",
                                                  "last_24hr_pct_change","txn_datetime"]].sort_values(by=["txn_datetime"] , ascending=True)


player_b_price=player["bprice"].values

time_axis=player["txn_datetime"].values
what_do_do=player["what_to_do"].values
fig,ax = plt.subplots()
predict=[min(player_b_price),max(player_b_price)]
for k, v in news_date.iterrows():
    #convert string datetime to datetime
    t=v[1]
    news_id=v[0]
    news_time=[t,t]
    ax.plot(news_time,predict, label=news_id)

#plot player buying price over time
ax.plot(time_axis,player_b_price, label="cur_price")



#news=[min(player_b_price),max(player_b_price)]

 #get positive news time for player
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


#ax.plot(news_time,news, "r-", label="news")
plt.ylabel(player_id)
legend = ax.legend(loc='upper left', shadow=True)
plt.gcf().autofmt_xdate()
plt.show()