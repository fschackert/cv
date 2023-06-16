import plotly.graph_objects as go

CUSTOM_BLUE = '#2766E8'
CUSTOM_GREY = '#212529'
CUSTOM_RED = '#E83283'
CUSTOM_YELLOW = '#E8B84A'

LINECOLOR = 'rgba(33, 37, 41, 1)'

CATEGORY_COLORS = {
    'MUSIC': CUSTOM_YELLOW,
    'EDUCATION': CUSTOM_BLUE,
    'WORK': CUSTOM_RED,
    'PROGRAMMING': CUSTOM_BLUE,
    'LANGUAGES': CUSTOM_RED,
    'OTHER SKILLS': CUSTOM_GREY,
}


def plot_skills(df, category, max_level=5):
    category_df = df[df['category'] == category].reset_index()

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
            #  'hovermode': False,
        },
    )

    for i, row in category_df.iterrows():
        skills.add_trace(
            go.Scatter(
                x=list(range(max_level)),
                y=[i] * max_level,
                mode='markers',
                opacity=0.3,
                name=row['skill'],
                marker_color=CATEGORY_COLORS[category],
                marker_size=25,
                marker_line_width=0,
            )
        )
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
            )
        )

    return skills
