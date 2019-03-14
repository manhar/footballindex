import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path


import pandas as pd
import matplotlib.pyplot as plt
import glob
from mysql_populate_table import get_pos_news_date , get_neg_news_date, getplayerscore
from dateutil import parser
import my_config

t=my_config.ConfigSectionMap("logging")['output_dir']


player_name="alvaro-morata"  ## "antoine-griezmann"#"radja-nainggolan"
player_surname="zaha"
path =r'/Users/ashish/Documents/footballindex/data/' # use your path
allFiles = glob.glob(path + "*.txt")

scores=getplayerscore(player_name)


player=scores.loc[scores.player_id==player_name, ["bprice",
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

sell= player.loc[player.what_to_do=='sell' , ["txn_datetime"]].sort_values(by=["txn_datetime"] , ascending=True)
buy= player.loc[player.what_to_do=='buy', ["txn_datetime"]].sort_values(by=["txn_datetime"] , ascending=True)



player_b_price=player["bprice"].values
player_1_price=player["last_1min_pct_change"].values
player_2_price=player["last_2min_pct_change"].values
player_3_price=player["last_3min_pct_change"].values
player_4_price=player["last_4min_pct_change"].values
player_5_price=player["last_5min_pct_change"].values
player_6_price=player["last_6min_pct_change"].values
player_7_price=player["last_7min_pct_change"].values
player_8_price=player["last_8min_pct_change"].values
player_9_price=player["last_9min_pct_change"].values
player_10_price=player["last_10min_pct_change"].values
player_24_price=player["last_24hr_pct_change"].values
time_axis=player["txn_datetime"].values
what_do_do=player["what_to_do"].values
fig,ax = plt.subplots()
predict=[min(player_b_price),max(player_b_price)]
for sell_time in sell["txn_datetime"].values:
    print(sell_time)
    ax.plot([sell_time,sell_time],predict, label="sell")

for buy_time in buy["txn_datetime"].values:
    print(buy_time)
    ax.plot([buy_time,buy_time],predict, label="buy")



#plot player buying price over time
ax.plot(time_axis,player_b_price, label="cur_price")
#ax.plot(time_axis,player_1_price, label="last 1 min % change")
#ax.plot(time_axis,player_2_price, label="last 2 min % change")
#ax.plot(time_axis,player_3_price,  label="last 3 min % change")
#ax.plot(time_axis,player_4_price,  label="last 4 min % change")
#ax.plot(time_axis,player_5_price,  label="last 5 min % change")
#ax.plot(time_axis,player_6_price,  label="last 6 min % change")
#ax.plot(time_axis,player_7_price,  label="last 7 min % change")
#ax.plot(time_axis,player_8_price,  label="last 8 min % change")
#ax.plot(time_axis,player_9_price,  label="last 9 min % change")
#ax.plot(time_axis,player_10_price, label="last 10 min % change")
#ax.plot(time_axis,player_24_price, label="last 24 hours % change")



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
plt.ylabel(player_name)
legend = ax.legend(loc='upper left', shadow=True)
plt.gcf().autofmt_xdate()
plt.show()