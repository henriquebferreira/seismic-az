import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, JsCode


def aggrid(data):
    gb = GridOptionsBuilder.from_dataframe(data)

    cellsytle_jscode = JsCode("""
    function(params) {
        const start_color = [55,217,37];
        const end_color = [255,35,35];
        const min_mag = 2;
        const max_mag = 6;
        const delta_mag = max_mag-min_mag;
        var colors = [0,0,0];
        console.log("X");
        for (let i = 0; i < 3; i++) {
            let start_color_part = start_color[i];
            let end_color_part = end_color[i];
            let m = (end_color_part-start_color_part)/delta_mag;
            let b = start_color_part-m*min_mag;
            let color_part = m*params.data.magnitude +b;
            colors[i] = parseInt(color_part);
        }
        const alpha = 0.8;
        const color = `rgba(${colors[0]}, ${colors[1]}, ${colors[2]}, ${alpha})`;
        return {'backgroundColor': color};
    };
    """)

    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    for col in data.columns:
        gb.configure_column(col, filter=False)

    gb.configure_grid_options(
        domLayout='normal',
        getRowStyle=cellsytle_jscode)
    gridOptions = gb.build()

    st.markdown("""<div style="display: flex;justify-content: space-between;font-weight: 700;">
                        <span>2</span>
                        <span>Magnitude Range</span>
                        <span>6</span>
                    </div>
                    <div style="height:18px; background: linear-gradient(90deg, rgba(55,217,37,1) 0%, rgba(255,35,35,1) 100%); margin-bottom: 8px; border: 1px solid #5f6a96;">
                    </div>""", unsafe_allow_html=True)

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        update_mode="selection_changed",
        allow_unsafe_jscode=True,
        theme="material",
        custom_css={
            ".ag-header-row": {"background-color": "#1e2337", "color": "white !important"},
            ".ag-header-cell:first-of-type:not(.ag-header-cell-moving):hover": {"background-color": "#5f6a96 !important", "color": "white !important"},
            ".ag-header-cell:not(.ag-column-resizing)+.ag-header-cell:not(.ag-header-cell-moving):hover": {"background-color": "#5f6a96 !important", "color": "white !important"},
            ".ag-theme-material .ag-checkbox-input-wrapper.ag-checked:after": {"color": "white !important"},
            ".ag-theme-material .ag-row-selected": {"font-weight": "700 !important"}
        }
    )
    return grid_response
