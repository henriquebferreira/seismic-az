import datetime as dt

import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
from crawlers.ipma import IpmaCrawler
from crawlers.ivar import IvarCrawler
from streamlit_app.component.pdk_layer import (LAYERS_MAPPING,
                                               LAYERS_VARIABLES_MAPPING,
                                               pdk_layer, pdk_tooltip)
from streamlit_app.utils import split_into_groups


@st.experimental_memo(ttl=1800)
def load_data(source):
    if source == "IPMA":
        ipma_crawler = IpmaCrawler("azores")
        ipma_crawler.crawl()
        df = ipma_crawler.pandify_data()
    elif source == "IVAR":
        ivar_crawler = IvarCrawler()
        ivar_crawler.crawl()
        df = ivar_crawler.pandify_data()
    else:
        raise Exception(
            f"Invalid {source} as a data source. Select 'IPMA' or 'IVAR'.")

    return df


@st.experimental_memo(ttl=3600)
def filter_df_by(df, column, min_value, max_value):
    return df[(df[column] >= min_value) & (df[column] <= max_value)]


@st.cache
def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(encoding="utf-8")


def visualization_content(sidebar_container):
    # Data Selection Section
    st.header("Select Data")

    DATA_SOURCES = {
        "IVAR": "IVAR (Instituto de Vulcanologia da Universidade dos Açores)",
        "IPMA": "IPMA (Instituto Português do Mar e da Atmosfera)"
    }
    data_source = st.radio("Select Data Source",
                           DATA_SOURCES.keys(),
                           format_func=lambda x: DATA_SOURCES.get(x))

    data = load_data(source=data_source)

    # auxiliary date columns
    data["date_string"] = data["date"].dt.strftime('%Y-%m-%d %H:%M')
    now = dt.datetime.now()
    data["hours_since"] = (now - data.date) / np.timedelta64(1, 'h')

    min_time = data["date"].min().to_pydatetime()
    max_time = data["date"].max().to_pydatetime()

    min_mag, max_mag = data["magnitude"].min(), data["magnitude"].max()
    min_mag, max_mag = float(min_mag), float(max_mag)

    min_lat, max_lat = data["lat"].min(), data["lat"].max()
    min_lat, max_lat = float(min_lat), float(max_lat)

    min_lon, max_lon = data["lon"].min(), data["lon"].max()
    min_lon, max_lon = float(min_lon), float(max_lon)
    with sidebar_container:
        st.header("Select Data Config")

        st.caption("Data Sources")
        st.markdown(
            """
            <div class="data-source-container">
                <a href="https://www.ipma.pt/pt/index.html" target="_blank" rel="noopener noreferrer" >
                    <img src="https://www.antenasul.pt/wp-content/uploads/2019/07/IPMA.png" alt="IPMA" class="data-source-img" >
                </a>
                <a href="http://www.cvarg.azores.gov.pt/civisa/Paginas/homeCIVISA.aspx" target="_blank" rel="noopener noreferrer" >
                    <img src="http://www.cvarg.azores.gov.pt/Style%20Library/css/images/cvarg-master-logo.png" alt="CIVISA" class="data-source-img" style="background-color:black">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        presets = {
            "Sao Jorge Crisis": {
                "lower_time": dt.datetime(2022, 3, 19),
                "upper_time": max_time,
                "lower_lat": 38.519,
                "upper_lat": 38.798,
                "lower_lon": -28.330,
                "upper_lon": -27.750,
                "lower_mag": 1.0,
                "upper_mag": 10.0
            },
            "Custom": {
                "lower_time": min_time,
                "upper_time": max_time,
                "lower_lat": min_lat,
                "upper_lat": max_lat,
                "lower_lon": min_lon,
                "upper_lon": max_lon,
                "lower_mag": min_mag,
                "upper_mag": max_mag
            },
        }
        selected_preset = st.selectbox("Select a preset config",
                                       (presets.keys()))

        lower_time_value = presets[selected_preset]["lower_time"]
        upper_time_value = presets[selected_preset]["upper_time"]
        lower_lat_value = presets[selected_preset]["lower_lat"]
        upper_lat_value = presets[selected_preset]["upper_lat"]
        lower_lon_value = presets[selected_preset]["lower_lon"]
        upper_lon_value = presets[selected_preset]["upper_lon"]
        lower_mag_value = presets[selected_preset]["lower_mag"]
        upper_mag_value = presets[selected_preset]["upper_mag"]

        lower_time, upper_time = st.slider(
            "Date interval",
            min_value=min_time,
            max_value=max_time,
            value=(lower_time_value, upper_time_value),
            step=dt.timedelta(hours=3),
            format="Do MMM hh:mm")

        lower_lat, upper_lat = st.slider(
            "Latitude interval",
            min_value=min_lat,
            max_value=max_lat,
            value=(lower_lat_value, upper_lat_value),
            format="%.3f",
            step=0.001)

        lower_lon, upper_lon = st.slider(
            "Longitude interval",
            min_value=min_lon,
            max_value=max_lon,
            value=(lower_lon_value, upper_lon_value),
            format="%.3f",
            step=0.001)

        lower_mag, upper_mag = st.slider(
            "Magnitude interval",
            min_value=min_mag,
            max_value=max_mag,
            value=(lower_mag_value, upper_mag_value),
            format="%.1f",
            step=0.1)
        st.caption("---")

    data = filter_df_by(data, "date", lower_time, upper_time)
    data = filter_df_by(data, "lat", lower_lat, upper_lat)
    data = filter_df_by(data, "lon", lower_lon, upper_lon)
    data = filter_df_by(data, "magnitude", lower_mag, upper_mag)

    grid = st.aggrid(data)

    selected_data = pd.DataFrame(grid['selected_rows'])
    data_to_draw = data if selected_data.empty else selected_data

    st.download_button(
        label="Download data as CSV",
        data=convert_df_to_csv(data_to_draw),
        file_name='az_seismic_data.csv',
        mime='text/csv')
    st.caption("---")

    # Data Visualization Section
    st.header("Data Visualization")

    with sidebar_container:
        st.header("Data Visualization Config")
        num_maps = st.number_input(
            'Number of maps', min_value=1, value=1, max_value=6)

    if data_to_draw.empty:
        st.error("No data for the selected inputs.")
        return

    map_center = ((upper_lat+lower_lat)/2, (upper_lon+lower_lon)/2)
    zoom = 8

    # Set viewport for the deckgl map
    view = pdk.ViewState(latitude=map_center[0],
                         longitude=map_center[1],
                         zoom=zoom,
                         pitch=15)

    num_maps = int(num_maps)
    maps_controllers = {k: {} for k in range(num_maps)}
    grouped_maps = split_into_groups(list(maps_controllers.keys()))

    layers, tooltips = [], []

    LAND_COVER = [[[upper_lon, lower_lat], [upper_lon, upper_lat],
                   [lower_lon, upper_lat], [lower_lon, lower_lat]]]

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        LAND_COVER,
        stroked=False,
        get_polygon="-",
        get_fill_color=[200, 200, 200, 20],
    )

    for group_idx, g in enumerate(grouped_maps):
        select_box_cols = st.columns(len(g)*2)
        map_cols = st.columns(len(g))

        for idx, c in enumerate(select_box_cols):
            if idx % 2 == 0:
                layer_name = c.selectbox(
                    'Select Layer Type',
                    (LAYERS_MAPPING.keys()),
                    index=0,
                    key=f'col_layer_{group_idx*4+idx}')
            else:
                available_variables = LAYERS_VARIABLES_MAPPING.get(layer_name)

                plot_variable = c.selectbox(
                    'Select Variable',
                    available_variables,
                    index=0,
                    key=f'col_variable_{group_idx*4+idx}')
            if idx % 2 == 1:
                layers.append(
                    pdk_layer(layer_name, plot_variable, data_to_draw))
                tooltips.append(pdk_tooltip(layer_name, data_to_draw.columns))

        for idx, c in enumerate(map_cols):
            # variable types should depend on layer type
            # tooltip should depend on the layer type
            map_deck = pdk.Deck(
                layers=[layers[group_idx*2+idx], polygon_layer],
                initial_view_state=view,
                tooltip=tooltips[idx],
                map_style="mapbox://styles/mapbox/dark-v10",
            )

            # Render the deck.gl map in the Streamlit app as a Pydeck chart
            map = c.pydeck_chart(map_deck)
