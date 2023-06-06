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
                        ], style={"height": "20vh", "width": "75vw"})
                    )
                ], width="auto"),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4(
                                style={"margin-right": "10px"},
                                className="fa-solid fa-star-of-life",
                            ),
                            html.H2(
                                "1996",
                                style={"display": "inline"}
                            ),
                            html.Br(),
                            html.H4(
                                style={"margin-right": "20px"},
                                className="fa-solid fa-location-dot",
                            ),
                            html.H2(
                                "Ulm",
                                style={"display": "inline"}
                            ),
                        ], style={"height": "20vh", "width": "20vw"})
                    )
                ], width="auto"),
            ], justify="left"),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Button(
                                id="selectedCategory",
                                className="w-100",
                            ),
                            html.Br(),
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
                                        "font-size": 20,
                                    },
                                ),
                                dbc.DropdownMenuItem(
                                    "LANGUAGES",
                                    id="buttonLanguages",
                                    style={
                                        "color": CATEGORY_COLORS["LANGUAGES"],
                                        "font-size": 20,
                                    },
                                ),
                                dbc.DropdownMenuItem(
                                    "OTHER SKILLS",
                                    id="buttonOthers",
                                    style={
                                        "color": CATEGORY_COLORS["OTHER SKILLS"],
                                        "font-size": 20,
                                    },
                                )],
                                label="Select category",
                                direction="up",
                                color="light",
                                style={
                                    "font-size": 20,
                                },
                                className="d-grid",
                            ),
                        ], style={"height": "60vh", "width": "20vw"})
                    )
                ], width="auto"),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id="timeline",
                                clear_on_unhover=True,
                                config={"displayModeBar": False},
                                style={"height": "100%", "width": "100%"},
                            )
                        ], style={"height": "60vh", "width": "40vw"})
                    )
                ], width="auto"),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(
                                id="globe",
                                style={"height": "100%", "width": "100%"},
                            )
                        ], style={"height": "60vh", "width": "32vw"})
                    )
                ], width="auto"),
            ], justify="left"),
        ])
    )
]
