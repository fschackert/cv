from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from utils import CATEGORY_COLORS

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
                        ], style={'height': '120px'})
                    )
                ], width=12)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button(
                                        'PROGRAMMING',
                                        outline=True,
                                        color='primary',
                                    )
                                ], className='d-grid gap-2'),
                                dbc.Col([
                                    dbc.Button(
                                        'LANGUAGES',
                                        outline=True,
                                        color='primary',
                                    )
                                ], className='d-grid gap-2'),
                                dbc.Col([
                                    dbc.Button(
                                        'OTHER SKILLS',
                                        outline=True,
                                        color='primary',
                                    )
                                ], className='d-grid gap-2')
                            ]),
                            dcc.Graph(
                                id='programmingSkills',
                                config={'displayModeBar': False},
                                style={'height': '70%', 'width': '100%'},
                            ),
                        ], style={'height': '480px', 'width': '280px'})
                    )
                ], width='auto'),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='timeline',
                                clear_on_unhover=True,
                                config={'displayModeBar': False},
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '480px', 'width': '860px'})
                    )
                ], width='auto'),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='globe',
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '480px'})
                    )
                ]),
            ]),
        ])
    )
]
