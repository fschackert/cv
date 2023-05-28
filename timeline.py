import pandas as pd
import plotly.graph_objects as go

from utils import category_to_color

df = pd.read_csv('data.csv', parse_dates=['start', 'end'])

timeline = go.Figure(layout={'xaxis': {'type': 'date'}})

timeline.add_trace(
    go.Bar(
        x=(df['end']-df['start']).astype('timedelta64[ms]'),
        y=df['title'],
        orientation='h',
        base=df['start'],
        marker_color=[category_to_color[category] for category in df['category']],
        opacity=0.5,
    )
)

timeline.update_layout(
    height=360,
    width=640,
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)
