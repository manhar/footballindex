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
from bokeh.models import ColumnDataSource, DataRange1d, Select, Legend , MultiSelect
from bokeh.layouts import row, column
from bokeh.palettes import Viridis3
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

players=api_parser.parse_api(api_link)
players_list=list(sorted(players.keys()))

n=len(players_list)/50



p = figure(plot_width=900, plot_height=700,x_axis_type="datetime", tools=TOOLS)
#xs = [[] for x in xrange(n)]
#ys = [[] for x in xrange(n)]

#r1 = p.line(x=[], y=[], color="red", line_width=2, legend="morata"  )
#r2 = p.line(x=[], y=[], color="blue", line_width=2, legend="ronaldo"   )
lines=dict()
datasource=dict()


for player in players_list:
    i=0
    lines[player]= p.line(x=[], y=[], color=Viridis3[i], line_width=2 )
    datasource[player] = lines[player].data_source
    i+=1

hover =p.select(dict(type=HoverTool))
hover.tooltips=([
    ("player", "@pubdate")
])

#print(datasource['cristiano-ronaldo'].data['x'])
#ds1 = lines["alvaro-morata"].data_source
#ds2 = lines["cristiano-ronaldo"].data_source

@linear()
def update_data(step):
    #print("step num :" +str(step))
    df=api_parser.parse_api(api_link)

    for player in players:
        new_data = dict()
        new_data['x']=datasource[player].data['x'] + [ df[player]['datetime'] ]
        new_data['y']=datasource[player].data['y'] + [ df[player]['score'] ]
        datasource[player].data=new_data

def hide_all_lines():
    for player in players:
        lines[player].visible=False


def update_plot(attrname, old, new):
    #print("old: "  + str(old))
    #print("new: "+ str(new))
    #print ("attrname: " + str(attrname ))

    players = player_select.value
    hide_all_lines()
    #p.title.text = "Data analysis for " + players[player]['name']
    for player in players:
        lines[player].visible=True




player = players_list[0:2]   #'alvaro-morata'



#players = {
#    'cristiano-ronaldo': {
#        'position': 'Forward',
#        'title': 'Cristiano Ronaldo',
#    },
#    'alvaro-morata': {
#        'position': 'forward',
#        'title': 'Alvaro Morata',
#    }
#}

#player_select = Select(value=player, title='Player', options=sorted(players.keys()))
player_select = MultiSelect(value=player, title='Player', options=sorted(players.keys()) , size=30)
#distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])

player_select.on_change('value', update_plot)
print ("PlayerSelect: "+ str(player_select.value))

#source=d1.data

controls = column(player_select)

curdoc().add_root(row(p, controls))
curdoc().title="Player Analysis"

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update_data, 6000)

