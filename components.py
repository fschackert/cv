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
                            html.H1("Dr. Florian K. Schackert"),
                        ], style={"height": "20vh", "width": "100%"})
                    )
                ], width=10),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H3(
                                style={"margin-right": "10px"},
                                className="fa-solid fa-star-of-life",
                            ),
                            html.H2(
                                "1996",
                                style={"display": "inline"}
                            ),
                            html.Br(),
                            html.H3(
                                style={"margin-right": "20px"},
                                className="fa-solid fa-location-dot",
                            ),
                            html.H2(
                                "Ulm",
                                style={"display": "inline"}
                            ),
                        ], style={"height": "20vh", "width": "100%"})
                    )
                ], width=2),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Button(
                                id="selectedCategory",
                                className="w-100",
                                style={"font-size": 20},
                            ),
                            html.Br(),
                            dcc.Graph(
                                id="skills",
                                config={"displayModeBar": False},
                                style={"height": "60%"},
                            ),
                            html.Br(),
                            dbc.DropdownMenu([
                                dbc.DropdownMenuItem(
                                    "PROGRAMMING",
                                    id="buttonProgramming",
                                    style={
                                        "color": CATEGORY_COLORS["PROGRAMMING"],
                                    },
                                ),
                                dbc.DropdownMenuItem(
                                    "LANGUAGES",
                                    id="buttonLanguages",
                                    style={
                                        "color": CATEGORY_COLORS["LANGUAGES"],
                                    },
                                ),
                                dbc.DropdownMenuItem(
                                    "OTHER SKILLS",
                                    id="buttonOthers",
                                    style={
                                        "color": CATEGORY_COLORS["OTHER SKILLS"],
                                    },
                                )],
                                label="Select category",
                                color="light",
                                style={"height": "20%"},
                                className="d-grid",
                            ),
                        ], style={"height": "60vh", "width": "100%"})
                    )
                ], width=3),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id="timeline",
                                clear_on_unhover=True,
                                config={"displayModeBar": False},
                                style={"height": "100%", "width": "100%"},
                            )
                        ], style={"height": "60vh", "width": "100%"})
                    )
                ], width=5),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id="globe",
                                style={"height": "100%", "width": "100%"},
                            )
                        ], style={"height": "60vh", "width": "100%"})
                    )
                ], width=4),
            ]),
        ], style={"height": "100vh"}),
    )
]
