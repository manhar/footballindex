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
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from collections import OrderedDict
from mysql_populate_table import getAllprediction,getplayerscore,getNewsPubDateByPlayer,getDistinctPlayers
from bokeh.models import Legend , HoverTool, Span,LinearAxis, Range1d
from datetime import datetime
import time
import bokeh.io as bio

import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

#get  data for the last 120 minutes from the database
hours_filter=24
#player_id="neymar"
player_id="harry-kane" #"marcus-rashford"
team="man utd manchester united"
team=""


distinctPlayers=getDistinctPlayers(hours_filter)
TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"


for player_id in distinctPlayers.player_id:
    #player_id=player_id
    print(  player_id)
    #output_file("/Users/ashish/Documents/VS_WORKSPACE/main/vizualization/html_files/"+player_id+".html")


    data=getplayerscore(player_id,hours_filter)
    news_date=getNewsPubDateByPlayer(player_id, team ,hours_filter )

    data= data.loc[data.player_id==player_id]

    #plot y range
    min_data_price=min(data.bprice)-0.01
    max_data_price=max(data.bprice)+0.01

    predicted_date=[min_data_price,max_data_price]

    p1 = figure(x_axis_type="datetime", title=player_id+" Prices",plot_width=500, plot_height=500, tools=TOOLS, toolbar_location="above", y_range=(min_data_price, max_data_price))
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price (£)'
    p1.line(data['datetime_id'], data['bprice'], color='green' , legend=player_id  ,line_width=4,   alpha=1, muted_alpha=0.8)

    if not news_date.empty:
        news_date['dt']= news_date.pubdate.dt.date #convert string to date
        news_date=news_date.sort_values(by='pubdate') #sort df by pubdate
        news_date['news_cnt']=news_date.groupby('dt')['pubdate'].rank(method='first')
        for k, v in news_date.iterrows():
            source = ColumnDataSource(data=dict(
                    news_time=[v[1],v[1]],
                    predicted_date=[min_data_price, max_data_price],
                    pubdate=[str(v[1]),str(v[1])],
                    feed_name=[v[3],v[3]],
                    title=[v[2],v[2]],
                    ))


        p1.extra_y_ranges = {"news_cumsum": Range1d(start=0, end=news_date.news_cnt.max()+1)}
        p1.add_layout(LinearAxis(y_range_name="news_cumsum", axis_label="Total appearance in news "), 'right')


        for index, dt in np.ndenumerate(news_date.dt.unique()):
            line=news_date[news_date.dt==dt]
            source = ColumnDataSource(data=dict(
                    pubdate=line.pubdate,
                    pubdate_str=line.pubdate.dt.strftime('%Y-%m-%d %H:%M:%S'),
                    feed_name=line.feed_name,
                    news_cnt=line.news_cnt,
                    title=line.title,
                    ))
            p1.line(line.pubdate, line.news_cnt, color="red", y_range_name="news_cumsum" , line_width=4,   alpha=0.2, muted_alpha=0.9)
            p1.circle('pubdate', 'news_cnt',source=source, color="blue", y_range_name="news_cumsum" , line_width=10,   alpha=0.2, muted_alpha=0.9)


    p1.legend.location = "top_left"
    p1.legend.click_policy="hide"

    hover =p1.select(dict(type=HoverTool))
    hover.tooltips=([
        ("Date", "@pubdate_str"),
        ("Feed", "@feed_name"),
        ("Title", "@title"),
    ])

    output_file("/Users/ashish/Documents/VS_WORKSPACE/main/vizualization/html_files/"+player_id+".html")
    bio.save(p1,filename="/Users/ashish/Documents/VS_WORKSPACE/main/vizualization/html_files/"+player_id+".html")
    show( p1 )
