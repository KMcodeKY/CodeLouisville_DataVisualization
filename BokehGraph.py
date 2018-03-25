import sqlite3
import pandas as pd
from bokeh.io import show, output_file
from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, ColumnDataSource, RangeSlider
from bokeh.plotting import figure
from bokeh.models import HoverTool, NumeralTickFormatter

conn = sqlite3.connect('employment_analysis.db')
cur = conn.cursor()

output_file("test.html")

TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

barChartData = pd.read_sql(""" SELECT * FROM timeAnalysis ORDER BY Total_NetPresentValue DESC""", con=conn)
barChartData = barChartData.reset_index(drop=True)

#source = ColumnDataSource(data=barChartData)
source = ColumnDataSource(data=barChartData.to_dict())
y_max = barChartData['Total_NetPresentValue'].values.max() + 1000000

#x_range=barChartData['Employment_Title'].tolist()

p = figure(plot_height=600, plot_width=600, toolbar_location="right", title="Net Present Value (2017)", tools=TOOLS)
p.y_range=(0, y_max)
p.vbar(x='Employment_Title', top='Total_NetPresentValue', width=1, source=source)

hover = p.select_one(HoverTool)

hover.tooltips = [('Position', '@Employment_Title'),
                  ('Net Present Value', '@Total_NetPresentValue{0,0}'),
                  ('Education Years', '@Education_Years'),
                  ('Residency', '@Residency')
                 ]

p.yaxis.formatter = NumeralTickFormatter(format="0,0")

p.xgrid.grid_line_color = None

callback = CustomJS(args=dict(p=p), code="""
    var a = cb_obj.value;
    p.x_range.start = a[0];
    p.x_range.end = a[1];
""")

range_slider = RangeSlider(start=0, end=barChartData.shape[0], value=(0,barChartData.shape[0]), step=10, title="Test")
range_slider.js_on_change('value', callback)

#def change_data(attrname, old, new):
#    st = start_Slider.value
#    iv = interval_Slider.value
#    print(st)
#    print(iv)
#
#    new_df = barChartData[(st):(st+iv+1)].copy(deep=True)
#    source.data = ColumnDataSource(data=new_df).data
#Sliders
#start_Slider = Slider(start=0, end=barChartData.shape[0], value=0, step=10, title="Position to start display at")
#start_Slider.on_change('value', change_data)
#interval_Slider = Slider(start=10, end=barChartData.shape[0], value=10, step=10, title="# of positions to display")
#interval_Slider.on_change('value', change_data)
#p = row(widgetbox(start_Slider, interval_Slider),p,width=800)

layout = row(p,widgetbox(range_slider))
show(layout)

cur.close()
conn.close()