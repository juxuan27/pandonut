import dash
from dash import dcc
from dash import html
import pandas as pd
from app.ui import (
    header,
    tap_frisbeemap_controls
)
from app import helpers,tab_frisbeemap
from config import strings
from dash.dependencies import Input, Output
from gevent import pywsgi


# FRISBEE DATASET
df_school_frisbee_info=pd.read_csv(strings.SCHOOL_FRISBEE_DATA_PATH)
dpd_options_province=[strings.ALL]+helpers.get_dropdown_items(df=df_school_frisbee_info, attribute="Province")
dpd_options_city_list={}
for province in dpd_options_province:
    dpd_options_city_list[province]=[strings.ALL]+helpers.get_dropdown_items(
        df=df_school_frisbee_info[df_school_frisbee_info["Province"].isin([province])],
        attribute="City")
dpd_options_type_list=[strings.ALL]+helpers.get_dropdown_items(df=df_school_frisbee_info, attribute="Type")

# CURRENT DATA
curr_province=strings.INITIAL_PROVINCE
curr_type=strings.ALL


# EXTERNAL SCRIPTS AND STYLES
external_scripts = ["https://kit.fontawesome.com/0bb0d79500.js"]
external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
]

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "pandonut", "content": "width=device-width, initial-scale=1"}],
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
)
app.title = strings.APP_NAME
app.config["suppress_callback_exceptions"] = True
server = app.server

# GENERAL LAYOUT
app.layout = html.Div(
    [
        header.make_header(),
        html.Div(
            className="wrapper",
            children=[
                html.Div(id="main-area", className="main-area"),
            ],
        ),
    ]
)


# TAB RENDERER
@app.callback(Output("main-area", "children"), [Input("navigation-tabs", "value")])
def render_tab(tab):
    """
    Renders content depending on the tab selected.

    :param tab: tab option selected
    :return: HTML div
    """
    if tab == "tab-frisbee-map":
        return [
            html.Div(
                id="tab-frisbee-map-container",
                className="tab-frisbee-map-container",
                children=[
                    tap_frisbeemap_controls.make_tab_frisbee_map_controls(
                        city_arr = dpd_options_city_list,
                        province_arr = dpd_options_province,
                        province_val = curr_province,
                        type_arr=dpd_options_type_list,
                        type_val=curr_type
                    )
                ],
            )
        ]
    elif tab == "tab-about-us":
        return [
            html.Div(
                className="about-us",
                children=html.Div(
                    className="about-us-inner",
                    children=[
                        html.H3(id="text1",children="盘盘圈"),
                        html.H1(id="text2",children="飞盘地图"),
                        html.P(id="text3",children='''
                        盘盘圈飞盘地图是“盘盘圈”的一个实验项目，我们希望 ta 能帮助对飞盘感兴趣的人用最低的信息成本参与到飞盘运动中来，也希望定居地发生变化的盘友，能快速找到本地组织，重建生活的秩序。'''),
                        html.P(id="text3",children='''
                        如果您发现您的队伍或俱乐部没有出现在这个地图上，抱歉是我们的疏忽，请点击这里联系我们。'''),
                        html.P(id="text3",children='''
                        JuJu, 经林, miao2, and Gray, are proud to present the CN Ultimate's Map
                        ''')
                        
                    ]
                )
                
            )
        ]


# MAP RENDERER (TAB 1)
@app.callback(
    Output("tab-frisbee-map-container", "children"),
    [
        Input("port-map-dropdown-province", "value"),
        Input("port-map-dropdown-city", "value"),
        Input("port-map-dropdown-type", "value"),
    ],
)
def update_port_map_tab(province,city,type):
    """
    Renders content for the Map tab.

    :param port: str, port of interest
    :param vessel_type: str, vessel type of interest
    :param year: int, year of interest
    :param month: int, month of interest
    :return: HTML div
    """
    global curr_province
    global curr_city
    global curr_type
    curr_province=province
    curr_city=city
    curr_type=type

    return html.Div(
        children=[
            tap_frisbeemap_controls.make_tab_frisbee_map_controls(
                city_arr=dpd_options_city_list,
                city_val=curr_city,
                province_arr=dpd_options_province,
                province_val=curr_province,
                type_arr=dpd_options_type_list,
                type_val=curr_type,
            ),
            tab_frisbeemap.make_tab_port_map_map(
                df=df_school_frisbee_info, province=province,city=city,type=type
            ),
            tab_frisbeemap.make_tab_port_map_table(
                df=df_school_frisbee_info, province=province,city=city,type=type
            ),
        ]
    )



if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050) # production
    
