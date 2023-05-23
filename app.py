from dash import html
from dash import Dash

from components import app_components

def main() -> None:
    """..."""

    # ==================================================================
    # GLOBAL THINGIES
    # ==================================================================

    app = Dash(__name__)
    app.layout = html.Div(children=app_components)

    # ==================================================================
    # RUN THE SERVER
    # ==================================================================

    app.run_server(debug=True)


if __name__ == '__main__':
    main()