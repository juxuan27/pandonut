import feffery_antd_components as fac
import dash
from dash import dcc
from dash import html
import pandas as pd
from app.ui import (
    header,
    tab_frisbeemap,
    add_information
)
from app import helpers
from config import strings
from dash.dependencies import Input, Output, State
import csv


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
                    tab_frisbeemap.make_tab_frisbee_map_controls(
                        city_arr = dpd_options_city_list,
                        province_arr = dpd_options_province,
                        province_val = curr_province,
                        type_arr=dpd_options_type_list,
                        type_val=curr_type
                    )
                ],
            )
        ]
    elif tab == "tab-add-info":
        return [
            html.Div(
                id="add-info-container",
                className="add-info-container",
                children=[
                    add_information.make_add_info_table()

                ]
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
            tab_frisbeemap.make_tab_frisbee_map_controls(
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



@app.callback(
    [
     Output('show-info', 'children'),  
     Output('form-item-usr-name', 'validateStatus'),  
     Output('form-item-usr-contact', 'validateStatus'),  
     Output('form-item-name', 'validateStatus'),  
     Output('form-item-type', 'validateStatus'),  
    #  Output('form-item-time', 'validateStatus'),  
     Output('form-item-contact', 'validateStatus'),  
     Output('form-item-address', 'validateStatus'),  
     Output('form-item-compete', 'validateStatus'),  
    #  Output('form-item-coach', 'validateStatus'),  
    #  Output('form-item-scale', 'validateStatus'),  
    #  Output('form-item-fee', 'validateStatus'),  
     Output('form-item-usr-name', 'help'),  
     Output('form-item-usr-contact', 'help'),  
     Output('form-item-name', 'help'),  
     Output('form-item-type', 'help'),  
    #  Output('form-item-time', 'help'),  
     Output('form-item-contact', 'help'),  
     Output('form-item-address', 'help'),  
     Output('form-item-compete', 'help'),  
    #  Output('form-item-coach', 'help'),  
    #  Output('form-item-scale', 'help'),  
    #  Output('form-item-fee', 'help')
     ],  
    Input('form-submit', 'nClicks'),
    [State('form-usr-name', 'value'),
     State('form-usr-contact', 'value'),
     State('form-name','value'),
     State('form-type','value'),
     State('form-time','value'),
     State('form-contact','value'),
     State('form-address','value'),
     State('form-compete','value'),
     State('form-coach','value'),
     State('form-scale','value'),
     State('form-fee','value'),
     State('form-other','value'),
     ], 
    prevent_initial_call=True
)
def form_demo_2_callback(nClicks, username, usrcontact,name,type,time,contact,address,compete,coach,scale,fee,other):
    if username and usrcontact and name and type and contact and address and compete:
        with open(strings.SCHOOL_FRISBEE_ADD_DATA_PATH,"a",newline="") as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow([username, usrcontact,name,type,time,contact,address,compete,coach,scale,fee,other])
        return [
            fac.AntdAlert( 
                message='信息成功提交！我们会尽快将其更新在地图上，感谢您的填写！',
                type='success',
                showIcon=True,
                messageRenderMode='marquee',
                style={
                    'marginBottom': '10px'
                },
                closable=True,
            ),     
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
            None ,
        ]

    return [
        fac.AntdAlert(  # 警告提示
            message='信息填写有误！请检查后进行提交！',
            type='error',
            showIcon=True,
            messageRenderMode='marquee',
            style={
                'marginBottom': '10px'
            }
        ),
        None if username else 'error',
        None if usrcontact else 'error',
        None if name else 'error',
        None if type else 'error',
        None if contact else 'error',
        None if address else 'error',
        None if compete else 'error',
        None if username else '不能为空！',
        None if usrcontact else '不能为空！',
        None if name else '不能为空！',
        None if type else '不能为空！',
        None if contact else '不能为空！',
        None if address else '不能为空！',
        None if compete else '不能为空！'
    ]




if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050) # production
    
