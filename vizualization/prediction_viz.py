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
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import column
from bokeh.models.widgets import DataTable, TableColumn


player="andrea-belotti"

def datetime(x):
    return np.array(x, dtype=np.datetime64)

#full_data=getAllprediction("2017-01-01 00:00:00")


full_data=pd.read_csv('/Users/ashish/Documents/footballindex/data/predictor.csv')
full_data["datetime_col"] = datetime(full_data['datetime_id'])

source1 = ColumnDataSource(full_data)

#unique_players=full_data.player_id.unique()
unique_players=full_data.loc[full_data.what_to_do!="keep"].player_id.unique()

p1 = figure(x_axis_type="datetime", title="Player Prices",plot_width=900, plot_height=700)
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

for player in unique_players:

    data= full_data.loc[full_data.player_id==player]

    event= data.loc[data.what_to_do !='keep' ,["what_to_do", "datetime_id"] ].sort_values(by=["datetime_id"] , ascending=True)

    predict=[min(data.cur_bprice),max(data.cur_bprice)]

    p1.line(data['datetime_col'], data['cur_bprice'], color='green' , legend=player  ,line_width=2,   alpha=0.2, muted_alpha=0.8)



    for index, row in event.iterrows():
        event_type=row[0]
        event_time=row[1]
        label=event_type+"-"+event_time
        if event_type=="sell":
            p1.line(datetime([event_time,event_time]), predict, color='red' , legend=label ,line_width=2,   alpha=0.2, muted_alpha=0.9)
        else:
            p1.line(datetime([event_time,event_time]), predict, color='blue', legend=label  ,line_width=2,   alpha=0.2, muted_alpha=0.9)


p1.legend.location = "top_left"
p1.legend.click_policy="hide"



show( p1 )
