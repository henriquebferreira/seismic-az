# Seismic AZ

A Streamlit web-app that provides visualization of Azorean Seismic data.

## Streamlit App

In order to launch the app locally, run the following command:

```
>>> streamlit run streamlit_app\app.py
```

## TODOS

* Crawler
  - [x] Standardize crawlers output for all data sources (currently: IPMA and IVAR)

* Streamlit
  - [x] Split news and visualization in separate "pages"
  - [x] Move secondary inputs to the sidebar
  - [ ] Map showing the location and depth of each earthquake (3D)
  - [ ] Map Animation (Daily data evolution?)
  - [x] Prettify dataframe table
    - [x] Create "Color range" element (from green to red according to magnitude)
    - [ ] Filter, reorder and format column names
  - [ ] News & Tweets from IPMA/IVAR (filter tweets by hashtag?)
    - [ ] Get twitter API key -> get Sao Jorge tweets -> select top X and render them
  - [ ] Present complementary data 
    * Tectonic plates map ?
    * Volcanoes map ?
  - [ ] Click on table row and show on map
    - [x] Data selectable through checkboxes on table rows
    - [x] Center maps according to the filtered data and set appropriate zoom
  - [ ] Drag&Create area on map and show earthquakes only in that area (on table and map)
  - [ ] [BUG]: Row selection in aggrid should not trigger the streamlit app to rerender