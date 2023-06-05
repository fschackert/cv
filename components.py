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
                            html.Button(
                                id='selectedCategory',
                                className='w-100',
                            ),
                            html.Br(),
                            html.Br(),
                            dcc.Graph(
                                id='skills',
                                config={'displayModeBar': False},
                                style={'height': '60%'},
                            ),
                            html.Br(),
                            html.Br(),
                            dbc.DropdownMenu([
                                dbc.DropdownMenuItem(
                                    'PROGRAMMING',
                                    id='buttonProgramming',
                                    style={
                                        'color': CATEGORY_COLORS['PROGRAMMING'],
                                        'font-size': 20,
                                    },
                                ),
                                dbc.DropdownMenuItem(
                                    'LANGUAGES',
                                    id='buttonLanguages',
                                    style={
                                        'color': CATEGORY_COLORS['LANGUAGES'],
                                        'font-size': 20,
                                    },
                                ),
                                dbc.DropdownMenuItem(
                                    'OTHER SKILLS',
                                    id='buttonOthers',
                                    style={
                                        'color': CATEGORY_COLORS['OTHER SKILLS'],
                                        'font-size': 20,
                                    },
                                )],
                                label='Select category',
                                direction='up',
                                color='light',
                                style={
                                    'font-size': 20,
                                },
                                className='d-grid',
                            ),
                        ], style={'height': '500px', 'width': '340px'})
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
                        ], style={'height': '500px', 'width': '810px'})
                    )
                ], width='auto'),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id='globe',
                                style={'height': '100%', 'width': '100%'},
                            )
                        ], style={'height': '500px', 'width': '580px'})
                    )
                ], width='auto'),
            ], justify="between"),
        ])
    )
]
