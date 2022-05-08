# -*- coding: utf-8 -*-
# @Time         : 2022/2/19 23:08
# @Author       : juju
# @File         : tab_frisbeemap
# @Description  : ***

import folium
from dash import dash_table
import numpy as np
import pandas as pd
from dash import html
from config import strings
from folium.plugins import MarkerCluster


from dash import dcc
from config import strings


def make_tab_frisbee_map_controls(
    city_arr,
    province_arr,
    province_val,
    type_arr,
    type_val,
    city_val=None,
) -> html.Div:

    def get_city(dictionary:dict,province:str):
        return list(dictionary[province])

    if city_val == None:
        city=get_city(city_arr, province_val)[0]
    else:
        city=city_val

    return html.Div(
        className="tab-frisbee-map-controls",
        children=[
            html.Div(
                className="tab-frisbee-map-single-control-container area-a",
                children=[
                    html.Label(
                        className="control-label", children=[strings.LABEL_PROVINCE]
                    ),
                    dcc.Dropdown(
                        id="port-map-dropdown-province",
                        clearable=False,
                        options=[
                            {"label": province, "value": province}
                            for province in province_arr
                        ],
                        value=province_val,
                    ),
                ],
            ),
            html.Div(className="tab-frisbee-map-single-control-separator area-a"),
            html.Div(
                className="tab-frisbee-map-single-control-container area-b",
                children=[
                    html.Label(
                        className="control-label", children=[strings.LABEL_CITY]
                    ),
                    dcc.Dropdown(
                        id="port-map-dropdown-city",
                        clearable=False,
                        options=[{"label": city, "value": city} for city in get_city(city_arr,province_val)],
                        value=city,
                    ),
                ],
            ),

            html.Div(className="tab-frisbee-map-single-control-separator area-b"),
            html.Div(
                className="tab-frisbee-map-single-control-container area-c",
                children=[
                    html.Label(
                        className="control-label", children=[strings.LABEL_TYPE]
                    ),
                    dcc.Dropdown(
                        id="port-map-dropdown-type",
                        clearable=False,
                        options=[{"label": type, "value": type} for type in type_arr],
                        value=type_val,
                    ),
                ],
            ),
        ],
    )


def make_tab_port_map_map(
    df: pd.DataFrame, city: str, province: str,type:str
) -> html.Div:

    def generate_popup(row) -> folium.Popup:
        html = f"""<div class="map-popup">
                        <b>{strings.MAP_POPUP_NAME}</b> {row.Name}<br>
                        <b>{strings.MAP_POPUP_TYPE}</b> {row.Type}<br>
                        <b>{strings.MAP_POPUP_TIME}</b> {row.Time}<br>
                        <b>{strings.MAP_POPUP_CONTACT}</b>{row.Contact}<br>
                        <b>{strings.MAP_POPUP_PROVINCE}</b>{row.Province}<br>
                        <b>{strings.MAP_POPUP_CITY}</b>{row.City}<br>
                        <b>{strings.MAP_POPUP_ADDRESS}</b> {row.Address}<br>
                        <b>{strings.MAP_POPUP_COMPETIVE}</b> {row.Competive}<br>
                        <b>{strings.MAP_POPUP_COACH}</b> {row.Coach}<br>
                        <b>{strings.MAP_POPUP_SCALE}</b>{row.Scale}<br>
                        <b>{strings.MAP_POPUP_FEE}</b>{row.Fee}<br>
                        <b>{strings.MAP_POPUP_OTHERS}</b>{row.Others}<br>
                    </div>"""
        iframe = folium.IFrame(html, width=300, height=100)
        return folium.Popup(iframe)

    def generate_center_coordinates(df: pd.DataFrame) -> list:
        if len(df) > 0:
            return [df["Lat"].median(), df["Lon"].median()]
        return [-1, -1]

    def generate_zoom_coordinates(df: pd.DataFrame) -> int:
        if len(df) > 1:
            if max(df["Lat"].max()-df["Lat"].min(), df["Lon"].max()-df["Lon"].min())>35:
                return 4
            else:
                return 6
        return 6

    if province == strings.ALL:
        data=df.copy()
    elif city ==  strings.ALL:
        data=df[(df["Province"] == province)].copy()
    else:
        data = df[
            (df["City"] == city)
            & (df["Province"] == province)
        ].copy()
    if type==strings.ALL:
        data=data.copy()
    else:
        data=data[(data["Type"] == type)].copy()

    geolocation = generate_center_coordinates(df=data)
    zoom_start = generate_zoom_coordinates(df=data)

    port_map = folium.Map(
        location=geolocation,
        zoom_start=zoom_start,
        tiles='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}',
        attr='default'
    )
    
    marker_cluster = MarkerCluster().add_to(port_map)
    for row in data.itertuples(index=False):
        folium.Marker(
            location=(row.Lat, row.Lon),
            popup=generate_popup(row),
            icon=folium.Icon(icon='map-signs',prefix='fa',color="green")
        ).add_to(marker_cluster)

        # folium.Circle(
        #     location=(row.Lat, row.Lon),
        #     popup=generate_popup(row),
        #     color="#30DFAF",
        #     weight=15,
        #     opacity=0.5,
        # ).add_to(port_map)

    port_map.save("data/index.html")
    return html.Div(
        className="map-container",
        children=[html.Iframe(srcDoc=open("data/index.html", "r").read())],
    )


def make_tab_port_map_table(
    df: pd.DataFrame, city: str, province: str,type:str
) -> html.Div:
    """
    Makes a table shown below the map on the Map tab.

    :param df: Pandas DataFrame, input data
    :param port: str, port of interest
    :param vessel_type: str, vessel type of interest
    :param year: int, year of interest
    :param month: int, month of interest
    :return: HTML div with embedded table
    """
    if province == strings.ALL:
        data = df.copy()
    elif city == strings.ALL:
        data = df[(df["Province"] == province)].copy()
    else:
        data = df[
            (df["City"] == city)
            & (df["Province"] == province)
            ].copy()

    if type==strings.ALL:
        data=data.copy()
    else:
        data=data[(data["Type"] == type)].copy()

    columns = [
        "Name",
        "Type",
        "Time",
        "Contact",
        "Province",
        "City",
        "Address",
        "Competive",
        "Coach",
        "Scale",
        "Fee",
        "Others"
    ]
    data = data[columns]
    data.columns = [
        strings.MAP_POPUP_NAME,
        strings.MAP_POPUP_TYPE,
        strings.MAP_POPUP_TIME,
        strings.MAP_POPUP_CONTACT,
        strings.MAP_POPUP_PROVINCE,
        strings.MAP_POPUP_CITY,
        strings.MAP_POPUP_ADDRESS,
        strings.MAP_POPUP_COMPETIVE,
        strings.MAP_POPUP_COACH,
        strings.MAP_POPUP_SCALE,
        strings.MAP_POPUP_FEE,
        strings.MAP_POPUP_OTHERS
    ]
    #data["Lat"] = data["Lat"].apply(lambda x: np.round(x, 5))
   # data["Lon"] = data["Lon"].apply(lambda x: np.round(x, 5))

    return html.Div(
        className="map-table-container",
        children=[
            dash_table.DataTable(
                id="table",
                columns=[{"name": i, "id": i} for i in data.columns],
                data=data.to_dict("records"),
                page_size=20,
                sort_action="native",
                filter_action="native",
                style_cell={"padding": "15px 5px", "boxShadow": "0 0",},
                style_data={"border": "0px", "textAlign": "center"},
                style_header={
                    "padding": "2px 5px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "border": "none",
                    "backgroundColor": "transparent",
                },
                style_table={"overflowX": "auto", "width": "calc(100% - 26px)",},
                style_data_conditional=[
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "transparent",
                        "border": "0px solid transparent",
                    }
                ],
            )
        ],
    )
