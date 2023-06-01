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

    # ==================================================================
    # GLOBAL THINGIES
    # ==================================================================

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.QUARTZ]
    )
    app.layout = html.Div(
        children=app_components,
    )

    df = pd.read_csv(
        filepath_or_buffer='data.csv',
        parse_dates=['start', 'end'],
    )
    skill_df = pd.read_csv(
        filepath_or_buffer='skills.csv',
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
                'margin': {'r': 60, 't': 0, 'l': 0, 'b': 0},
                'bargap': 0.1,
                'xaxis': {
                    'type': 'date',
                    'range': ['2014-05-01', '2023-06-01'],
                    'color': 'rgba(33, 37, 41, 1)',
                    'gridcolor': 'rgba(33, 37, 41, 1)',
                    'anchor': 'free',
                    'position': 0.0,
                },
                'yaxis': {
                    'visible': False,
                },
                'legend': {
                    'yanchor': 'bottom',
                    'y': 1.05,
                    'xanchor': 'left',
                    'x': 0.0,
                    'orientation': 'h',
                },
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {
                    'size': 20,
                },
                'uirevision': 'static',
            },
        )
        for category in df['category'].unique():
            category_df = df[df['category'] == category]
            timeline.add_trace(
                go.Bar(
                    # dash does not seem to like timedelta, maybe related to github.com/plotly/dash/issues/1808
                    x=(category_df['end'] - category_df['start']).dt.days*24*60*60*1000,
                    y=category_df['title'],
                    orientation='h',
                    base=category_df['start'],
                    marker_color=category_to_color[category],
                    marker_line_width=0,
                    name=category,
                )
            )
        if hover_data:
            curve_number = hover_data['points'][0]['curveNumber']
            point_number = hover_data['points'][0]['pointNumber']
            for i in range(len(timeline['data'])):
                timeline['data'][i]['marker']['opacity'] = [
                    1.0 if i == curve_number and j == point_number else 0.6
                    for j in range(len(timeline['data'][i]['x']))
                ]
        else:
            timeline.update_traces(opacity=0.6)
        return timeline

    @app.callback(
        Output('globe', 'figure'),
        Input('timeline', 'hoverData'),
        Input('timeline', 'figure'),
        Input('timeline', 'restyleData'))
    def update_globe(hover_data, figure, _):
        toggled_off_categories = []
        for figure_data in figure['data']:
            try:
                if figure_data['visible'] == 'legendonly':
                    toggled_off_categories.append(figure_data['name'])
            except KeyError:
                pass
        toggled_on = df[~df['category'].isin(toggled_off_categories)]
        if toggled_on.empty:
            toggled_on = df
            opacity = 0.0
            hovermode = False
        else:
            opacity = 0.6
            hovermode = 'closest'
        globe = px.scatter_geo(
            data_frame=toggled_on,
            lat='lat',
            lon='lon',
            color='title',
            color_discrete_sequence=[category_to_color[category] for category in toggled_on['category']],
            hover_name='location',
            opacity=opacity,
            size=(toggled_on['end'] - toggled_on['start']).astype(int),
        )
        globe.update_geos(
            projection_type='mercator',
            center={'lat': 50.9413, 'lon': 6.9583},
            lataxis_range=[40, 65],
            lonaxis_range=[-10, 40],
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
            uirevision='static',
            hovermode=hovermode,
        )
        globe.update_traces(
            marker={
                'line': {'width': 0},
            },
        )
        if hover_data is not None:
            scope = df[df['title'] == hover_data['points'][0]['label']]
            for i, point in enumerate(globe['data']):
                if i == scope.index:
                    point['marker']['opacity'] = 1.0
        return globe

    @app.callback(
        Output('skills', 'figure'),
        Input('skills', 'figure'))
    def update_skills(_):
        max_level = 5
        skills = go.Figure(
            layout={
                'margin': {'r': 0, 't': 0, 'l': 0, 'b': 0},
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {
                    'size': 20,
                },
                'uirevision': 'static',
            },
        )
        skills.add_trace(
            go.Scatterpolar(
                r=skill_df['level'],
                theta=skill_df['skill'],
                fill='toself',
                fillcolor='rgba(0, 0, 0, 0.05)',
                )
            )
        skills.update_layout(
            polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5],
                        showticklabels=False
                )),
                showlegend=False
        )
        return skills

    # ==================================================================
    # RUN THE SERVER
    # ==================================================================

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
