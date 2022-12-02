from dash import html, dcc


def get_figure_col(fig_id, col_title, additional_col_size=None):
    return html.Div(
        className="col"
        if additional_col_size == None
        else f"col-{additional_col_size}",
        style={
            "box-shadow": "0 3px 10px rgb(0 0 0 / 0.2)",
            "margin-right": "10px",
            "background": "white",
            "height": "400px",
        },
        children=[
            html.Div(
                className="row",
                style={"background": "#e4e4e4"},
                children=[
                    html.H6(
                        col_title,
                        className="mb-0",
                        style={
                            "color": "#0c213d",
                            "background-color": "#fefdfe",
                            "width": "auto",
                            "border-bottom-right-radius": "90px",
                            "border-top-right-radius": "90px",
                        },
                    ),
                ],
            ),
            html.Hr(
                style={
                    "border-left": "10px solid #F07167",
                    "height": "3px",
                    "background-color": "#fefdfe",
                    "margin-top": "0px",
                }
            ),
            html.Div(className="container", children=[dcc.Graph(id=fig_id)]),
        ],
    )


def get_card_col(child_id, col_title, additional_col_size=None):
    return html.Div(
        className="col"
        if additional_col_size == None
        else f"col-{additional_col_size}",
        style={
            "box-shadow": "0 3px 10px rgb(0 0 0 / 0.2)",
            "margin-right": "10px",
            "background": "white",
            "height": "400px",
        },
        children=[
            html.Div(
                className="row",
                style={"background": "#e4e4e4"},
                children=[
                    html.H6(
                        col_title,
                        className="mb-0",
                        style={
                            "color": "#0c213d",
                            "background-color": "#fefdfe",
                            "width": "auto",
                            "border-bottom-right-radius": "90px",
                            "border-top-right-radius": "90px",
                        },
                    ),
                ],
            ),
            html.Hr(
                style={
                    "border-left": "10px solid #F07167",
                    "height": "3px",
                    "background-color": "#fefdfe",
                    "margin-top": "0px",
                }
            ),
            html.Div(className="container", children=[], id=child_id),
        ],
    )
