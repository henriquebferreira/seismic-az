import pydeck as pdk
import streamlit as st

from streamlit_app.utils import build_color_gradient, hex_to_rgb


def heatmap_layer(data, *args, **kwargs):
    variable = kwargs["variable"]
    if variable == 'Density':
        weight = "1"
    elif variable == 'Magnitude':
        weight = "magnitude*20"
    elif variable == 'Depth':
        weight = "1/(depth+5)"
    elif variable == 'Recentness':
        weight = "1/(hours_since+10)"

    return pdk.Layer(
        "HeatmapLayer",
        data=data,
        opacity=0.9,
        radius=100,
        get_position=["lon", "lat"],
        aggregation=pdk.types.String("MEAN"),
        get_weight=weight
    )


def hexagon_layer(data, *args, **kwargs):
    return pdk.Layer(
        "HexagonLayer",
        data=data,
        get_position=["lon", "lat"],
        radius=100,
        elevation_scale=10,
        pickable=True,
        extruded=True,
        auto_highlight=True,
    )


def column_layer(data, *args, **kwargs):
    variable = kwargs["variable"]

    bg_color = hex_to_rgb(st.get_option('theme.primaryColor'))
    white = [255, 255, 255]

    s_color, e_color = white, bg_color

    if variable == 'Density':
        elevation = "50"
        variable_name = "20"
        start_value = 0
        end_value = 100
    elif variable == 'Magnitude':
        elevation = "magnitude*20"
        variable_name = "magnitude"
        start_value = 1.5
        end_value = 4.5
    elif variable == 'Depth':
        elevation = "depth!=0 ? 100/(depth) : 101"
        variable_name = "1/(depth+5)"
        start_value = 1/30
        end_value = 1/5
    elif variable == 'Recentness':
        elevation = '200/hours_since'
        variable_name = "1/(hours_since+10)"
        start_value = 1/500
        end_value = 1/10

    color = []
    for i in range(len(white)):
        color_component = build_color_gradient(
            name=variable_name,
            start_value=start_value,
            end_value=end_value,
            start_color=s_color[i],
            end_color=e_color[i])
        color.append(color_component)

    return pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation=elevation,
        elevation_scale=50,
        elevation_range=[0, 1000],
        radius=100,
        get_fill_color=color,
        pickable=True,
        auto_highlight=True,
    )


def scatterplot_layer(data, *args, **kwargs):
    variable = kwargs["variable"]

    bg_color = hex_to_rgb(st.get_option('theme.primaryColor'))
    white = [255, 255, 255]

    s_color, e_color = white, bg_color

    if variable == 'Density':
        radius = "15"
        variable_name = "20"
        start_value = 0
        end_value = 100
    elif variable == 'Magnitude':
        radius = "magnitude*20"
        variable_name = "magnitude"
        start_value = 1.5
        end_value = 4.5
    elif variable == 'Depth':
        radius = "depth!=0 ? 100/(depth) : 101"
        variable_name = "1/(depth+5)"
        start_value = 1/30
        end_value = 1/5
    elif variable == 'Recentness':
        radius = '200/hours_since'
        variable_name = "1/(hours_since+10)"
        start_value = 1/500
        end_value = 1/10

    color = []
    for i in range(len(white)):
        color_component = build_color_gradient(
            name=variable_name,
            start_value=start_value,
            end_value=end_value,
            start_color=s_color[i],
            end_color=e_color[i])
        color.append(color_component)

    return pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["lon", "lat"],
        opacity=0.8,
        stroked=True,
        pickable=True,
        filled=True,
        radius_scale=3,
        radius_min_pixels=3,
        # radius_max_pixels=50,
        line_width_min_pixels=1,
        get_radius=radius,
        get_fill_color=color,
        get_line_color=[0, 0, 0],
    )


def grid_layer(data, *args, **kwargs):
    return pdk.Layer(
        "GridLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="magnitude*20",
        elevation_scale=4,
        cell_size=200,
        extruded=True
    )


def screen_grid_layer(data, *args, **kwargs):
    return pdk.Layer(
        "ScreenGridLayer",
        data=data,
        get_position=["lon", "lat"],
        get_elevation="magnitude*20",
        elevation_scale=4,
        elevation_range=[0, 1000],
        cell_size_pixels=20,
        color_range=[
            [25, 0, 0, 25],
            [85, 0, 0, 85],
            [127, 0, 0, 127],
            [170, 0, 0, 170],
            [190, 0, 0, 190],
            [255, 0, 0, 255]],
        pickable=False,
        opacity=0.8,
        auto_highlight=True,
        get_weight="magnitude"
    )


LAYERS_MAPPING = {
    # "Hexagon": hexagon_layer,
    "Heatmap": heatmap_layer,
    "Column": column_layer,
    "Scatter": scatterplot_layer,
    # "Grid": grid_layer,
    # "ScreenGrid": screen_grid_layer,
}

LAYERS_VARIABLES_MAPPING = {
    "Hexagon": ('Density',),
    "Heatmap": ('Density', 'Magnitude', 'Depth', 'Recentness'),
    "Column": ('Density', 'Magnitude', 'Depth', 'Recentness'),
    "Scatter": ('Density', 'Magnitude', 'Depth', 'Recentness'),
    "Grid": ('Density', 'Magnitude', 'Depth', 'Recentness'),
    "ScreenGrid": ('Density', 'Magnitude', 'Depth', 'Recentness'),
}


def pdk_layer(layer, variable, data):
    layer_function = LAYERS_MAPPING.get(layer)
    if not layer_function:
        raise Exception("Invalid layer type")

    return layer_function(data, variable=variable)


def pdk_tooltip(layer, data_cols):
    tooltip_lines = {
        "lat": "<b>Latitude: </b>{lat}<br />",
        "lon": "<b>Longitude: </b>{lon}<br />",
        "magnitude": "<b>Magnitude: </b>{magnitude}<br />",
        "depth": "<b>Depth: </b>{depth}<br />",
        "date": "<b>Date: </b>{date_string}<br />"
    }

    if layer == 'Column':
        lines = [t for c, t in tooltip_lines.items() if c in data_cols]
        html_string = ''.join(lines)
        return {'html': html_string}
    if layer == 'Scatter':
        lines = [t for c, t in tooltip_lines.items() if c in data_cols]
        html_string = ''.join(lines)
        return {'html': html_string}
