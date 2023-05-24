import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = pd.read_csv('data.csv')

fig = make_subplots(
    rows=1,
    cols=2,
    specs=[[{'type': 'scattergeo'}, {}]],
)

fig.add_trace(
    go.Scattergeo(
        lat=df['lat'],
        lon=df['lon'],
        mode='markers',
        marker={
            'size': 10,
        }
    ),
    row=1,
    col=1,
)

fig.update_geos(
    projection_type="mercator",
    center={'lat': 50, 'lon': 10},
    lataxis_range=[40, 60],
    lonaxis_range=[0, 20],
    showcountries=True,
)

fig.add_trace(
    go.Scatter(
        x=df['start'],
        y=df['category'],
    ),
    row=1,
    col=2,
)
fig.update_layout(
    height=300,
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)
