from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

app_components = [
    html.H1(
        children='Dr. Florian K. Schackert',
        style={'padding': 10, 'flex': 1},
    ),
    dcc.Graph(
        id='timeline',
        style={'padding': 10, 'flex': 1},
        clear_on_unhover=True,
    ),
    dcc.Graph(
        id='globe',
        style={'padding': 10, 'flex': 1},
    ),
    dcc.Store(
        id='selected_items',
    )
]
