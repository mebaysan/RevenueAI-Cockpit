from dash import html, dcc


def get_header(navbar_text, buttons=[]):
    navbar_end = [
        html.Li(
            className="nav-item mt-2",
            children=[
                html.A(
                    navbar_text,
                    className="navbar-brand text-center",
                    style={"color": "white"},
                ),
            ],
        )
    ]
    for btn in buttons:
        navbar_end.append(
            html.Li(
                className="nav-item",
                children=[
                    html.Button(
                        className=btn["className"],
                        id=btn["id"],
                        n_clicks=1,
                        style={
                            "font-size": "2rem",
                            "color": "white",
                            "background": "transparent",
                            "border-color": "transparent",
                        },
                    ),
                ],
            )
        )
        navbar_end.append(
            dcc.Store(id=btn["memory-id"], data="CLOSE"),
        )
    return html.Nav(
        className="navbar navbar-light",
        style={"background-color": "#0081A7"},
        children=[
            html.Div(
                className="container-fluid",
                children=[
                    html.A(
                        className="navbar-brand",
                        href="#",
                        children=[
                            html.Img(
                                className="d-inline-block align-text-top",
                                src="/assets/logo/logo.png",
                                width=30,
                                height=30,
                            )
                        ],
                    ),
                    html.Ul(className="nav justify-content-end", children=navbar_end),
                ],
            )
        ],
    )
