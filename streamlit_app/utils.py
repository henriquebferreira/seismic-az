import json
import os

import streamlit as st

from streamlit_app.component.about_footer import about_footer
from streamlit_app.component.aggrid_table import aggrid
from streamlit_app.component.tweet import tweet
from streamlit_app.section import PageHeader


def load_app_json():
    APP_JSON_FILENAME = 'app.json'

    # Look in all directories and subdirectories for "app.json" file
    file_path = None
    for root, _, files in os.walk(os.getcwd()):
        if APP_JSON_FILENAME in files:
            if file_path:
                raise Exception("Multiple 'app.json' files.")
            file_path = os.path.join(root, APP_JSON_FILENAME)

    if not file_path:
        raise Exception(
            "Could not find a 'app.json' file in all subdirectories.")

    # Load json contents into a python dictionary and return it
    with open(file_path, 'r') as fp:
        return json.load(fp)


def load_custom_components(st):
    """Adds custom components to a specified streamlit instance."""
    setattr(st, "aggrid", aggrid)
    setattr(st, "tweet", tweet)
    setattr(st, "page_header", PageHeader)
    setattr(st, "about_footer", about_footer)


def load_custom_style():
    with open('streamlit_app/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def set_session_variable(name, value):
    if name not in st.session_state:
        st.session_state[name] = value
    else:
        st.session_state[name] = value


def get_session_variable(name):
    if name not in st.session_state:
        return None
        # raise Exception(f"Variable {name} is not present in st.session_state")
    else:
        return st.session_state[name]


def split_into_groups(lst, group_size=2):
    """ 
    num_maps = 0 => [[]]
    num_maps = 1 => [[0]]
    num_maps = 2 => [[0,1]]
    num_maps = 3 => [[0,1], [2]]
    num_maps = 4 => [[0,1], [2,3]]
    num_maps = 5 => [[0,1], [2,3], [4]]
    num_maps = 5 => [[0,1], [2,3], [4, 5]]
    """
    return [lst[i:i+group_size] for i in range(0, len(lst), group_size)]


def hex_to_rgb(hex_string):
    hex_string = hex_string.lstrip('#')
    return tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))



def build_color_gradient(name, start_value, end_value, start_color, end_color):
    value_range = end_value-start_value
    return f'{name}*({end_color}-{start_color})/{value_range} + {start_color} - {start_value} *({end_color}-{start_color})/{value_range}'
    
def get_color_from_gradient(start_color,
                            end_color,
                            min_value,
                            max_value,
                            value):
    color = []

    delta_value = max_value-min_value
    for i in range(len(start_color)):
        s_color_comp = start_color[i]
        e_color_comp = end_color[i]
        slope = (e_color_comp-s_color_comp)/delta_value
        b = s_color_comp - slope * min_value
        color_comp = slope * value + b
        color.append(color_comp)

    return tuple(color)
