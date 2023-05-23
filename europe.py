import plotly.graph_objects as go

eu_map = go.Figure(go.Scattergeo())
eu_map.update_geos(
    lataxis_showgrid=True,
    lonaxis_showgrid=True,
    scope='europe'
)
eu_map.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
