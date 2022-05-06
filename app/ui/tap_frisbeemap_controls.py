# -*- coding: utf-8 -*-
# @Time         : 2022/2/19 22:26
# @Author       : juju
# @File         : tap_frisbeemap_control
# @Description  : ***

from dash import dcc
from dash import html
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
