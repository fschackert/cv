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
                    dbc.Card(
                        dbc.CardBody([
                            html.H1(
                                children='Florian Schackert',
                            )
                        ], style={'height': '110px'})
                    )
                ], width=12)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='timeline',
                                clear_on_unhover=True,
                                config={'displayModeBar': False},
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '480px'})
                    )
                ], width=8),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='globe',
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '480px'})
                    )
                ], width=4),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='programmingSkills',
                                config={'displayModeBar': False},
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '280px'})
                    )
                ], width=4),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='languageSkills',
                                config={'displayModeBar': False},
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '280px'})
                    )
                ], width=4),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='otherSkills',
                                config={'displayModeBar': False},
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '280px'})
                    )
                ], width=4),
            ], align='center'),
        ])
    )
]
