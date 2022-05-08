from dash import dcc
from dash import html
from config import strings


def make_header() -> html.Header:
    """
    Returns a HTML Header element for the application Header.

    :return: HTML Header
    """
    return html.Header(
        children=[
            # Icon and title container
            html.Div(
                className="dash-title-container",
                children=[
                    html.Img(className="dash-icon", src="assets/img/frisbee_logo_head.png",style={"width":"180px"})
                ],
            ),
            # create navigator with buttons
            html.Nav(
                children=[
                    dcc.Tabs(
                        id="navigation-tabs",
                        value="tab-frisbee-map",
                        children=[
                            dcc.Tab(
                                label=strings.TAB1_NAME,
                                value="tab-frisbee-map",
                                className="dash-tab",
                                selected_className="dash-tab-selected",
                            ),
                            
                            dcc.Tab(
                                label=strings.TAB2_NAME,
                                value="tab-add-info",
                                className="dash-tab",
                                selected_className="dash-tab-selected",
                            ),

                            dcc.Tab(
                                label=strings.TAB3_NAME,
                                value="tab-about-us",
                                className="dash-tab",
                                selected_className="dash-tab-selected",
                            ),
                            
                        ],
                    ),
                ]
            ),
        ]
    )
