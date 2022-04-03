"""Streamlit App focused on visualization of Azorean seismic data."""

import streamlit as st
from streamlit_option_menu import option_menu

from streamlit_app.page.app_pages import AppPages
from streamlit_app.utils import (load_app_json, load_custom_components,
                                 load_custom_style)

app_config = load_app_json()

st.set_page_config(
    page_title=app_config["name"],
    layout=app_config["layout"])

load_custom_components(st)
load_custom_style()

with st.sidebar:
    page_selected = option_menu("Menu",
                                options=AppPages.get_titles(),
                                icons=AppPages.get_icons())
    sidebar_container = st.container()
    st.about_footer(app_config["author"], app_config["email"])


st.page_header(app_config["name"], app_config["description"])

content_function = AppPages.get_content(page_selected)
content_function(sidebar_container)
