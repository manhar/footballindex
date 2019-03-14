#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 21:45:33 2017

@author: ashish
"""
import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path


import numpy as np
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
#from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT
from mysql_populate_table import getAllprediction
from bokeh.models import Legend
import datetime

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown
from bokeh.layouts import column , row
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show

output_file("dropdown.html")

menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]
dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)

#show(widgetbox(dropdown))

f1=widgetbox(dropdown)


player="andrea-belotti"
player="robert-lewandowski"

print("Processing:"+player)

def datetime(x):
    return np.array(x, dtype=np.datetime64)

data=getAllprediction(player,"2017-01-01 00:00:00")

#dtypes = [datetime.datetime,str,str,str,float,float,float,float,float,float,str,str,str,	str,	str,	str,	str,	str,	str,	str,	str,	str,	str,	str]
#data=pd.read_csv('/Users/ashish/Documents/footballindex/data/predictor_backfill.csv')


data["datetime_col"] = datetime(data['datetime_id'])

unique_players=data.player_id.unique()

data= data.loc[data.player_id==player]

event= data.loc[data.what_to_do !='keep' ,["what_to_do", "datetime_id"] ].sort_values(by=["datetime_id"] , ascending=True)

predicted_date=[min(data.cur_bprice),max(data.cur_bprice)]

p1 = figure(x_axis_type="datetime", title="Player Prices",plot_width=900, plot_height=700)
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'
p1.line(data['datetime_col'], data['cur_bprice'], color='green' , legend=player  ,line_width=4,   alpha=1, muted_alpha=0.8)
p1.line(data['datetime_col'], data['last_5min_bprice'], color='black' , legend=player  ,line_width=2,   alpha=1, muted_alpha=0.8)


for index, row in event.iterrows():
    event_type=row[0]
    event_time=row[1]
    label=event_type+"-"+str(event_time)
    if event_type=="sell":
        p1.line(datetime([event_time,event_time]), predicted_date, color='red' , legend=label ,line_width=2,   alpha=0.2, muted_alpha=0.9)
    else:
        p1.line(datetime([event_time,event_time]), predicted_date, color='blue', legend=label  ,line_width=2,   alpha=0.2, muted_alpha=0.9)


p1.legend.location = "top_left"
p1.legend.click_policy="hide"

print("Producing Graph")

layout=column (f1, p1)
show( layout )

