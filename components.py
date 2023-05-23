from dash import html
from dash import dcc

from europe import eu_map
app_components = [
    html.H1(
        children='Dr. Florian K. Schackert'),
    dcc.Graph(figure=eu_map)
    ]
