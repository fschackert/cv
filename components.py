from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


def card_wrapper(component, style=None):
    if style is None:
        style = dict()
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                component
            ], style=style)
        ),
    ])


app_components = [
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    card_wrapper(html.H1(
                        children='Dr. Florian K. Schackert',
                    ))
                ], width=12),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    card_wrapper(dcc.Graph(
                        id='timeline',
                        clear_on_unhover=True,
                        config={
                            'displayModeBar': False
                        }
                    ))
                ], width=8),
                dbc.Col([
                    card_wrapper(dcc.Graph(
                        id='globe',
                    ))
                ], width=4),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    card_wrapper(dcc.Graph(
                        id='skills',
                        clear_on_unhover=True,
                        config={
                            'displayModeBar': False
                        }
                    ))
                ], width=4),
                dbc.Col([
                    " "
                ], width=4),
                dbc.Col([
                    " "
                ], width=4),
            ], align='center'),
        ])
    )
]
