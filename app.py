import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html
from dash import Dash
from dash.dependencies import Input, Output, State

from components import app_components
from utils import category_to_color


def main() -> None:
    """..."""

    # ==================================================================
    # GLOBAL THINGIES
    # ==================================================================

    app = Dash(__name__)
    app.layout = html.Div(
        children=app_components,
        style={'display': 'flex', 'flex-direction': 'row'},
    )

    df = pd.read_csv(
        filepath_or_buffer='data.csv',
        parse_dates=['start', 'end'],
    )

    # ==================================================================
    # FIGURE CALLBACKS
    # ==================================================================

    @app.callback(
        Output('timeline', 'figure'),
        Input('selected_items', 'data'))
    def update_timeline(selected_items):
        timeline = go.Figure(
            layout={
                'height': 360,
                'width': 640,
                'margin': {"r": 0, "t": 36, "l": 0, "b": 0},
                'xaxis': {'type': 'date'},
            },
        )
        timeline.add_trace(
            go.Bar(
                x=(df['end'] - df['start']).astype('timedelta64[ms]'),
                y=df['title'],
                orientation='h',
                base=df['start'],
                marker_color=[category_to_color[category] for category in df['category']],
                opacity=0.6,
            )
        )
        timeline['data'][0]['marker']['opacity'] = [1.0 if i in selected_items else 0.5 for i in df.index]
        return timeline

    @app.callback(
        Output('globe', 'figure'),
        Input('selected_items', 'data'))
    def update_globe(selected_items):
        scope = df.iloc[selected_items]
        globe = px.scatter_geo(
            data_frame=scope,
            lat='lat',
            lon='lon',
            color='category',
            color_discrete_map=category_to_color,
            hover_name='location',
            opacity=0.5,
            size=(scope['end'] - scope['start']).astype(int),
        )
        globe.update_geos(
            projection_type='orthographic',
            fitbounds='locations',
            showcountries=True,
        )
        globe.update_layout(
            height=360,
            width=360,
            margin={"r": 0, "t": 36, "l": 0, "b": 0},
        )

        return globe

    # ==================================================================
    # SELECTION CALLBACKS
    # ==================================================================

    @app.callback(
        Output('selected_items', 'data'),
        Input('timeline', 'clickData'),
        Input('timeline', 'selectedData'))
    def update_selected_items(
            click_data,
            selected_data):
        selected_items = []
        if selected_data:
            selected_items += [point['pointNumber'] for point in selected_data['points']]
            return selected_items
        if click_data:
            selected_items += [click_data['points'][0]['pointNumber']]
            return selected_items
        return df.index

    # ==================================================================
    # RUN THE SERVER
    # ==================================================================

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
