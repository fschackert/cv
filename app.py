import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc

from components import app_components
from customcolors import CATEGORY_COLORS, LINECOLOR
from hovertemplates import *


# ==================================================================
# GLOBAL THINGIES
# ==================================================================

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE, dbc.icons.FONT_AWESOME])
server = app.server
app.layout = html.Div(children=app_components)

# Load and format CV data
timeline_df = pd.read_csv(
    delimiter=';',
    filepath_or_buffer='timeline.csv',
    parse_dates=['start', 'end'],
)
timeline_df.replace('n.a.', '', inplace=True)  # No empty string in this markdown
timeline_df['start_yyyy-mm-dd'] = timeline_df['start'].dt.date
timeline_df['end_yyyy-mm-dd'] = timeline_df['end'].dt.date

# Skill plot related objects
skill_df = pd.read_csv(
    delimiter=';',
    filepath_or_buffer='skills.csv',
)
button_categories = {
    'buttonProgramming': 'PROGRAMMING',
    'buttonLanguages': 'LANGUAGES',
    'buttonOthers': 'OTHER SKILLS',
}
max_skill_level = 5


# ==================================================================
# FIGURE CALLBACKS
# ==================================================================

@app.callback(
    Output("modal-dismiss", "is_open"),
    Input("close-dismiss", "n_clicks"),
    State("modal-dismiss", "is_open"))
def dismiss_modal(n_close, is_open):
    if n_close:
        return not is_open
    return is_open


@app.callback(
    Output('timeline', 'figure'),
    Input('timeline', 'hoverData'))
def update_timeline(hover_data):
    # Initialize figure with matching layout
    timeline = go.Figure(
        layout={
            'margin': {'r': 0, 't': 0, 'l': 0, 'b': 0},
            'bargap': 0.1,
            'xaxis': {
                'type': 'date',
                'range': ['2014-05-01', '2024-04-30'],
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

    # Each category gets its own trace
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
                    category_df['description'],
                    category_df['grade'],
                )),
                hovertemplate=TIMELINE_HOVER[category],
                hoverlabel={
                    "bgcolor": "white",
                    "font_size": 16,
                }
            )
        )

    # Highlight bar on hover
    if hover_data:
        curve_number = hover_data['points'][0]['curveNumber']
        point_number = hover_data['points'][0]['pointNumber']
        for i in range(len(timeline['data'])):
            timeline['data'][i]['marker']['opacity'] = [
                1.0 if i == curve_number and j == point_number else 0.6
                for j in range(len(timeline['data'][i]['x']))
            ]
    else:
        # timeline.update_traces(opacity=0.6) would also change the label colors
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
    # Update visibility of marker groups on the map based on timeline traces
    toggled_off_categories = []
    for figure_data in figure['data']:
        try:
            if figure_data['visible'] == 'legendonly':
                toggled_off_categories.append(figure_data['name'])
        except KeyError:
            pass
    toggled_on = timeline_df[~timeline_df['category'].isin(toggled_off_categories)]

    # Still show the map even when all categories are toggled off
    if toggled_on.empty:
        toggled_on = timeline_df
        opacity = 0.0
        hovermode = False
    else:
        opacity = 0.6
        hovermode = 'closest'

    # Plot the map
    globe = px.scatter_geo(
        data_frame=toggled_on,
        lat='lat',
        lon='lon',
        color=[str(i) for i in toggled_on['id']],  # Numerical values trigger continuous colors
        color_discrete_sequence=[CATEGORY_COLORS[category] for category in toggled_on['category']],
        hover_name='title',
        opacity=opacity,
        size=(toggled_on['end'] - toggled_on['start']).astype(int),
        custom_data=['institution', 'start_yyyy-mm-dd', 'end_yyyy-mm-dd', 'category'],
    )

    # Make map look nice
    globe.update_geos(
        projection_type='mercator',
        center={'lat': 50.9413, 'lon': 6.9583},
        lataxis_range=[40, 65],
        lonaxis_range=[-10, 40],
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
        hoverlabel={
            "bgcolor": "white",
            "font_size": 16,
        }
    )

    # Set format for hover data
    for point in globe['data']:
        point.hovertemplate = GLOBE_HOVER

    # Highlight map marker on timeline hover and bring to front
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
    # Set default category
    try:
        category = button_categories[ctx.triggered_id]
    except KeyError:
        category = 'PROGRAMMING'

    # Filter for selected category
    category_df = skill_df[skill_df['category'] == category].reset_index()

    # Initialize figure with matching layout
    skills = go.Figure(
        layout={
            'margin': {'r': 0, 't': 10, 'l': 0, 'b': 40},
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font': {'size': 20},
            'xaxis': {
                'visible': False,
                'fixedrange': True,
            },
            'yaxis': {
                'showgrid': False,
                'zeroline': False,
                'tickmode': 'array',
                'ticktext': category_df['skill'],
                'tickvals': category_df.index.tolist(),
                'fixedrange': True,
            },
            'showlegend': False,
            'legend': {
                'yanchor': 'bottom',
                'y': 1.05,
                'xanchor': 'center',
                'x': 0.0,
                'orientation': 'h',
                'itemclick': False,
            },
        },
    )

    # Build plot row by row
    for i, row in category_df.iterrows():
        # Plot muted markers in the background
        skills.add_trace(
            go.Scatter(
                x=list(range(max_skill_level)),
                y=[i] * max_skill_level,
                mode='markers',
                opacity=0.3,
                name=row['skill'],
                marker_color=CATEGORY_COLORS[category],
                marker_size=25,
                marker_line_width=0,
                hoverinfo='skip',
            )
        )
        # Plot actual skill level
        skills.add_trace(
            go.Scatter(
                x=list(range(row['level'])),
                y=[i] * row['level'],
                mode='markers+lines',
                name=row['skill'],
                marker_color=CATEGORY_COLORS[category],
                marker_size=25,
                marker_line_width=0,
                line_width=5,
                hoverlabel={
                    "bgcolor": "white",
                    "font_size": 16,
                },
                hoverinfo='text',
                hovertext=row['description'],
            )
        )

    return skills


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
        category = 'PROGRAMMING'  # Set default
    style = {
        'background-color': 'rgba(0, 0, 0, 0)',
        'border-color': 'rgba(0, 0, 0, 0)',
        'color': CATEGORY_COLORS[category],
        'font-size': 20,
        'text-align': 'center',
    }
    return category, style
