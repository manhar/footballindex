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

def datetime(x):
    return np.array(x, dtype=np.datetime64)

p = figure(plot_width=900, plot_height=700,x_axis_type="datetime")
r = p.multi_line(xs=[[],[]], ys=[[],[]], color="firebrick", line_width=2, legend="ONly 1 legend is possible with multiline"  )

ds = r.data_source


@linear()
def update(step):
    print("step num :" +str(step))
    df=api_parser.parse_api(api_link)
    player1=df['alvaro-morata']
    player2=df['cristiano-ronaldo']
    #print(player1)
    #print(player2)
    new_data = dict()

    new_data['xs'] = [ ds.data['xs'][0] +[player1['datetime']],  ds.data['xs'][1] +[player2['datetime']] ]
    new_data['ys'] = [ ds.data['ys'][0] +[player1['score']],     ds.data['ys'][1] +[player2['score']] ]

    ds.data = new_data


curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 6000)