from dash import html
from dash import dcc

app_components = [
    html.H1(
        children='Dr. Florian K. Schackert',
        style={'padding': 10, 'flex': 1},
    ),
    dcc.Graph(
        id='timeline',
        style={'padding': 10, 'flex': 1},
    ),
    dcc.Graph(
        id='globe',
        style={'padding': 10, 'flex': 1},
    ),
]
