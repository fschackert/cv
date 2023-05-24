from dash import html
from dash import dcc

from figure import fig

app_components = [
    html.H1(
        children='Dr. Florian K. Schackert'
    ),
    dcc.Graph(
        figure=fig,
        style={'padding': 10, 'flex': 1}
    ),
]
