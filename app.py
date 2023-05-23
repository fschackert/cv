from dash import html
from dash import Dash

def main() -> None:
    """..."""

    # ==================================================================
    # GLOBAL THINGIES
    # ==================================================================

    app = Dash(__name__)
    app.layout = html.Div()

    # ==================================================================
    # RUN THE SERVER
    # ==================================================================

    app.run_server(debug=True)


if __name__ == '__main__':
    main()