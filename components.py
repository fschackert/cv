from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from customcolors import CATEGORY_COLORS

modal = dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle("Hi, welcome!"),
                close_button=False
            ),
            dbc.ModalBody(
                "Thanks for checking out my CV. "
                "Hover over the plots below for more information."
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Explore",
                    id="close-dismiss"
                ),
            ),
        ],
        id="modal-dismiss",
        is_open=True,
        keyboard=False,
        backdrop="static",
)

app_components = [
    modal,
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.CardImg(
                                                src="static/abstract.png",
                                                style={
                                                    "height": "100%",
                                                },
                                            ),
                                        ],
                                        className="col-12 col-sm-4 col-md-3 col-lg-2",
                                        style={
                                            "height": "100%",
                                            "minHeight": "120px",
                                            "minWidth": "120px",
                                        },
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.H5(
                                                        "Dr. rer. nat.",
                                                        className="text-muted",
                                                        style={
                                                            "white-space": "nowrap",
                                                        },
                                                    ),
                                                    html.H2(
                                                        "Florian Schackert",
                                                        style={
                                                            "white-space": "nowrap",
                                                        },
                                                    ),
                                                    # html.Br(),  # Adds more space after name, optional
                                                    html.P(
                                                        [
                                                            html.H4(
                                                                className="fa-solid fa-star-of-life",
                                                                style={
                                                                    "margin-right": "10px",
                                                                },
                                                            ),
                                                            html.H3(
                                                                "1996",
                                                                style={
                                                                    "display": "inline",
                                                                    "margin-right": "30px",
                                                                    "white-space": "nowrap",
                                                                },
                                                            ),
                                                        ],
                                                        style={
                                                            "display": "inline-block",
                                                            "white-space": "nowrap",
                                                        },
                                                    ),
                                                    html.P(
                                                        [
                                                            html.H4(
                                                                className="fa-solid fa-location-dot",
                                                                style={
                                                                    "margin-right": "10px",
                                                                },
                                                            ),
                                                            html.H3(
                                                                "Berlin",
                                                                style={
                                                                    "display": "inline",
                                                                    "white-space": "nowrap",
                                                                },
                                                            ),
                                                        ],
                                                        style={
                                                            "display": "inline-block",
                                                            "white-space": "nowrap",
                                                        },
                                                    ),
                                                ],
                                            ),
                                        ],
                                        style={
                                            "minHeight": "120px",
                                        },
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.A(
                                                        [
                                                            dbc.CardImg(
                                                                src="static/orcid.svg",
                                                                style={
                                                                    "height": "5vh",
                                                                    "width": "5vh",
                                                                    "minHeight": "40px",
                                                                    "minWidth": "40px",
                                                                    "padding": "5px",
                                                                },
                                                            ),
                                                        ],
                                                        href="https://orcid.org/0000-0001-6028-3717",
                                                    ),
                                                    html.A(
                                                        [
                                                            dbc.CardImg(
                                                                src="static/github-mark.svg",
                                                                style={
                                                                    "height": "5vh",
                                                                    "width": "5vh",
                                                                    "minHeight": "40px",
                                                                    "minWidth": "40px",
                                                                    "padding": "5px",
                                                                },
                                                            ),
                                                        ],
                                                        href="https://github.com/fschackert",
                                                    ),
                                                    html.A(
                                                        [
                                                            dbc.CardImg(
                                                                src="static/linkedin.png",
                                                                style={
                                                                    "height": "5vh",
                                                                    "width": "5vh",
                                                                    "minHeight": "40px",
                                                                    "minWidth": "40px",
                                                                    "padding": "5px",
                                                                },
                                                            ),
                                                        ],
                                                        href="https://www.linkedin.com/in/florianschackert",
                                                    ),
                                                ],
                                            ),
                                        ],
                                        align="end",
                                        style={
                                            "text-align": "right",
                                        },
                                    ),
                                ],
                                className="g-0",
                                style={
                                    "height": "100%",
                                    "width": "100%",
                                    "minHeight": "120px",
                                },
                            ),
                        ],
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.Button(
                                                        id="selectedCategory",
                                                        style={
                                                            "font-size": 20,
                                                            "height": "20%",
                                                            "white-space": "nowrap",
                                                        },
                                                    ),
                                                    dcc.Graph(
                                                        id="skills",
                                                        config={
                                                            "displayModeBar": False,
                                                        },
                                                        style={
                                                            "height": "80%",
                                                        },
                                                    ),
                                                    dbc.DropdownMenu(
                                                        [
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
                                                            ),
                                                        ],
                                                        className="d-grid",
                                                        color="dark",
                                                        direction="up",
                                                        label="Select category",
                                                        style={
                                                            "height": "10%",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "height": "60vh",
                                                    "width": "100%",
                                                    "minHeight": "400px",
                                                    "text-align": "center",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                                className="col-12 col-lg-4",
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    dcc.Graph(
                                                        id="timeline",
                                                        clear_on_unhover=True,
                                                        config={
                                                            "displayModeBar": False,
                                                        },
                                                        style={
                                                            "height": "100%",
                                                            "width": "100%",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "height": "60vh",
                                                    "width": "100%",
                                                    "minHeight": "400px",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                                className="col-12 col-md-8 col-lg-4",
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    dcc.Graph(
                                                        id="globe",
                                                        style={
                                                            "height": "100%",
                                                            "width": "100%",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "height": "60vh",
                                                    "width": "100%",
                                                    "minHeight": "400px",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                                className="col-12 col-md-4 col-md-4",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    ),
]
