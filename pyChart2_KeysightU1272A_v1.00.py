# --------------------------------------------------------------------------------
# Tobias Haueter                                                        2022-09-26
# Chart plotting software for ".csv" files on localhost web browser.
#
# sudo apt install python3-plotly
#
# https://plotly.com/python/subplots/
# --------------------------------------------------------------------------------
# import mplcursors
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# read csv file and choose the delimiter.
csvFile_data = 'keysightU1272A-log.csv'
df = pd.read_csv(csvFile_data, delimiter=',')  # <TAB>: delimiter='\t' | comma: ','

# create figure
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=False)

# create names
y_1 = str(df._get_value(1, 'RangeSetting'))
y_2 = str(df._get_value(1, 'SecondaryRange'))
start_date = str(df._get_value(1, 'Timestamp'))

config = dict({'scrollZoom': True})

# add first chart on figure - x = time / y = data grep it with the first line 'name'
fig.add_trace(go.Scatter(
    x=df['Timestamp'],
    y=df['Reading'],
    mode='lines',
    name=y_1,
    line=dict(color="red")
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df['Timestamp'],
    y=df['SecondaryReading'],
    mode='lines',
    name=y_2,
    line=dict(color="blue")
), row=2, col=1)

# Update xaxis properties
fig.update_xaxes(title_text="", row=1, col=1)
fig.update_xaxes(title_text="Timestamp", row=2, col=1)
# fig.update_xaxes(title_text="x_10s", row=3, col=1)

# Update yaxis properties
fig.update_yaxes(title_text=y_1, row=1, col=1)
fig.update_yaxes(title_text=y_2, row=2, col=1)
# fig.update_yaxes(title_text="y_3", row=3, col=1)

# site properties
fig.update_layout(
    dragmode='zoom',
    title_text=f'pyCHARTs - {csvFile_data} [{start_date}]',  # xaxis_title="X Axis Title",
    plot_bgcolor='#e3ebff',
    showlegend=True,
    modebar_add=['drawline',
                 'v1hovermode',
                 'togglespikelines',
                 'togglehover',
                 'hovercompare',
                 'drawopenpath',
                 'drawcircle',
                 'drawrect',
                 'eraseshape'
                 ]
)

fig.show(config=config)
