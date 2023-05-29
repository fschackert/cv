import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash
from dash import html
from dash.dependencies import Input, Output, State

from components import app_components
from utils import category_to_color


def main() -> None:
    """..."""

    # ==================================================================
    # GLOBAL THINGIES
    # ==================================================================

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.QUARTZ]
    )
    app.layout = html.Div(
        children=app_components,
        #style={'display': 'flex', 'flex-direction': 'row'},
    )

    df = pd.read_csv(
        filepath_or_buffer='data.csv',
        parse_dates=['start', 'end'],
    )

    def _get_highlighted_locations(
            hover_data,
            selected_data):
        selected_items = []
        if hover_data:
            selected_items += [hover_data['points'][0]['pointNumber']]
        if selected_data:
            selected_items += [point['pointNumber'] for point in selected_data['points']]
        return selected_items

    # ==================================================================
    # FIGURE CALLBACKS
    # ==================================================================

    @app.callback(
        Output('timeline', 'figure'),
        Input('timeline', 'hoverData'))
    def update_timeline(hover_data):
        timeline = go.Figure(
            layout={
                'margin': {'r': 0, 't': 0, 'l': 0, 'b': 0},
                'bargap': 0,
                'xaxis': {
                    'type': 'date',
                    'range': ['2014-05-01', '2023-06-01'],
                },
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {'size': 18},
                'modebar': {'orientation': 'v'},
            },
        )
        timeline.add_trace(
            go.Bar(
                # dash does not seem to like timedelta, maybe related to github.com/plotly/dash/issues/1808
                x=(df['end'] - df['start']).dt.days*24*60*60*1000,
                y=df['title'],
                orientation='h',
                base=df['start'],
                marker_color=[category_to_color[category] for category in df['category']],
                marker_line_width=0,
            )
        )
        if hover_data:
            hover_number = hover_data['points'][0]['pointNumber']
            timeline['data'][0]['marker']['opacity'] = [1.0 if i == hover_number else 0.6 for i in df.index]
        else:
            timeline['data'][0]['marker']['opacity'] = [0.6 for _ in df.index]
        return timeline

    @app.callback(
        Output('globe', 'figure'),
        Input('timeline', 'hoverData'),
        Input('timeline', 'selectedData'))
    def update_globe(
            hover_data,
            selected_data):
        scope = df.iloc[_get_highlighted_locations(hover_data, selected_data)]
        globe = px.scatter_geo(
            data_frame=df,
            lat='lat',
            lon='lon',
            color='title',
            color_discrete_sequence=[category_to_color[category] for category in df['category']],
            hover_name='location',
            opacity=0.6,
            size=(df['end'] - df['start']).astype(int),
        )
        globe.update_geos(
            projection_type='mercator',
            center={'lat': 50.9413, 'lon': 6.9583},
            lataxis_range=[40, 65],
            lonaxis_range=[-10, 40],
            # fitbounds='locations',
            showcoastlines=False,
            resolution=50,
            scope='europe',
            showcountries=True,
            showframe=False,
            countrycolor='rgba(33, 37, 41, 1)',
            landcolor='rgba(0, 0, 0, 0.05)',
            lakecolor='rgba(0, 0, 0, 0)',
            bgcolor='rgba(0, 0, 0, 0)',
        )
        globe.update_layout(
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            showlegend=False,
            uirevision=1,
        )
        globe.update_traces(
            marker={
                'line': {'width': 0},
            }
        )
        for i, point in enumerate(globe['data']):
            if i in scope.index:
                point['marker']['opacity'] = 1.0
        return globe

    # ==================================================================
    # RUN THE SERVER
    # ==================================================================

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
