import sys
sys.path.insert(0, '../utilities')
import add_subdir_to_path

# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import random
import api_parser
import my_config

from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend
import datetime
from bokeh.models import DatetimeTickFormatter

BOKEH_PY_LOG_LEVEL=True

#Set the API link
api_link=my_config.ConfigSectionMap("football")['api_link']

TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"

#p = figure(x_axis_type="datetime", plot_width=900, plot_height=700, tools=TOOLS)

#p.xaxis.axis_label = 'Date'
#p.yaxis.axis_label = 'Price'
#r= p.line([], [], color='green' , legend="legend"  ,line_width=4)

players_data=api_parser.parse_api(api_link)
players_list=list(players_data.keys())

n=len(players_list)/50


p = figure(plot_width=900, plot_height=700,x_axis_type="datetime", tools=TOOLS)
#xs = [[] for x in xrange(n)]
#ys = [[] for x in xrange(n)]

r1 = p.line(x=[], y=[], color="red", line_width=2, legend="morata"  )
r2 = p.line(x=[], y=[], color="blue", line_width=2, legend="ronaldo"   )

ds1 = r1.data_source
ds2 = r2.data_source

@linear()
def update(step):
    print("step num :" +str(step))
    df=api_parser.parse_api(api_link)
    player1=df['alvaro-morata']
    player2=df['cristiano-ronaldo']
    #print(player1)
    #print(player2)
    new_data = dict()

    new_data['x'] =  ds1.data['x'] +[player1['datetime']]
    new_data['y'] =  ds1.data['y'] +[player1['score']]
    ds1.data = new_data

    new_data['x'] =  ds2.data['x'] +[player2['datetime']]
    new_data['y'] =  ds2.data['y'] +[player2['score']]
    ds2.data = new_data
curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 6000)

