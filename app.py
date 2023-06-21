import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html, Input, Output, ctx
import dash_bootstrap_components as dbc

from components import app_components
from utils import CATEGORY_COLORS, LINECOLOR, plot_skills, wrap_string


def main() -> None:

    # ==================================================================
    # GLOBAL THINGIES
    # ==================================================================

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.PULSE, dbc.icons.FONT_AWESOME],
    )

    app.layout = html.Div(
        children=app_components,
    )

    timeline_df = pd.read_csv(
        delimiter=';',
        filepath_or_buffer='timeline.csv',
        parse_dates=['start', 'end'],
    )

    skill_df = pd.read_csv(
        filepath_or_buffer='skills.csv',
    )

    button_categories = {
        'buttonProgramming': 'PROGRAMMING',
        'buttonLanguages': 'LANGUAGES',
        'buttonOthers': 'OTHER SKILLS',
    }

    hovertemplates = {
        'EDUCATION': "<b>%{text}</b><br>" +
            "%{customdata[0]}<br><br>" +
            "%{customdata[1]}" +
            "<b>Grade</b>: %{customdata[2]}",
        'WORK': "<b>%{text}</b><br>" +
            "%{customdata[0]}<br><br>" +
            "%{customdata[1]}",
        'MUSIC': "<b>%{text}</b><br>" +
            "%{customdata[0]}<br><br>" +
            "%{customdata[1]}" +
            "<b>Grade</b>: %{customdata[2]}",
    }

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
                'bargap': 0.1,
                'xaxis': {
                    'type': 'date',
                    'range': ['2014-05-01', '2023-06-30'],
                    'color': LINECOLOR,
                    'gridcolor': LINECOLOR,
                },
                'yaxis': {
                    'visible': False,
                    'fixedrange': True,
                },
                'legend': {
                    'yanchor': 'bottom',
                    'y': 1.05,
                    'xanchor': 'center',
                    'x': 0.5,
                    'orientation': 'h',
                },
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                'font': {'size': 20},
                'uirevision': 'static',
            },
        )
        for category in timeline_df['category'].unique():
            category_df = timeline_df[timeline_df['category'] == category]
            timeline.add_trace(
                go.Bar(
                    # dash does not seem to like timedelta, maybe related to github.com/plotly/dash/issues/1808
                    x=(category_df['end'] - category_df['start']).dt.days*24*60*60*1000,
                    y=category_df['id'],
                    orientation='h',
                    base=category_df['start'],
                    marker_color=CATEGORY_COLORS[category],
                    marker_line_width=0,
                    name=category,
                    text=category_df['title'],
                    textposition='none',
                    customdata=list(zip(
                        category_df['institution'],
                        [wrap_string(description) for description in category_df['description']],
                        category_df['grade'],
                    )),
                    hovertemplate=hovertemplates[category],
                    hoverlabel={
                        "bgcolor": "white",
                        "font_size": 16,
                    }
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
            # timeline.update_traces(opacity=0.6) also changes the label colors
            for i in range(len(timeline['data'])):
                timeline['data'][i]['marker']['opacity'] = [
                    0.6 for _ in range(len(timeline['data'][i]['x']))
                ]
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
        toggled_on = timeline_df[~timeline_df['category'].isin(toggled_off_categories)]
        if toggled_on.empty:
            toggled_on = timeline_df
            opacity = 0.0
            hovermode = False
        else:
            opacity = 0.6
            hovermode = 'closest'
        globe = px.scatter_geo(
            data_frame=toggled_on,
            lat='lat',
            lon='lon',
            color=[str(i) for i in toggled_on['id']],  # Numerical values trigger continuous colors
            color_discrete_sequence=[CATEGORY_COLORS[category] for category in toggled_on['category']],
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
            countrycolor=LINECOLOR,
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
            hovered_on = toggled_on[toggled_on['id'] == hover_data['points'][0]['label']]['id'].to_string(index=False)
            for i, point in enumerate(globe.data):
                if point['legendgroup'] == hovered_on:
                    point['marker']['opacity'] = 1.0
                    globe.data = globe.data[:i] + globe.data[i+1:] + (point, )  # See plotly feature request #2345
                    break
        return globe

    @app.callback(
        Output('skills', 'figure'),
        Input('buttonProgramming', 'n_clicks'),
        Input('buttonLanguages', 'n_clicks'),
        Input('buttonOthers', 'n_clicks'))
    def update_skills(*_):
        try:
            category = button_categories[ctx.triggered_id]
        except KeyError:
            category = 'PROGRAMMING'
        return plot_skills(skill_df, category)

    @app.callback(
        Output('selectedCategory', 'children'),
        Output('selectedCategory', 'style'),
        Input('buttonProgramming', 'n_clicks'),
        Input('buttonLanguages', 'n_clicks'),
        Input('buttonOthers', 'n_clicks'))
    def update_skill_title(*_):
        try:
            category = button_categories[ctx.triggered_id]
        except KeyError:
            category = 'PROGRAMMING'
        style = {
            'background-color': 'rgba(0, 0, 0, 0)',
            'border-color': 'rgba(0, 0, 0, 0)',
            'color': CATEGORY_COLORS[category],
            'font-size': 20,
            'text-align': 'center',
        }
        return category, style

    # ==================================================================
    # RUN THE SERVER
    # ==================================================================

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
