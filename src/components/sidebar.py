from dash import html, Input, Output, State
from components.config import SIDEBAR_STYLE


def get_sidebar(sidebar_id, sidebar_title, sidebar_content):
    return html.Div(id=sidebar_id, className='d-flex flex-column flex-shrink-0 p-3', children=[
        # html.Button(className='bi bi-arrow-left', id='menu-close-icon', style={
        #     'font-size': '2rem', 'color': 'white', 'margin-right': '10px', 'background': 'transparent', 'border-color': 'transparent', 'left': '0px', 'position': 'absolute'}),
        html.H5(
            sidebar_title, className='d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none', style={'color': 'white'}),
        sidebar_content
    ])


def get_sidebar_list(section_title, section_links):
    li_list = [html.Li(className='nav-item',
                       children=[html.H6(section_title, style={'color': 'white'},)])]
    for i in section_links:
        li_list.append(html.Li(className='nav-item',
                       children=[html.A(i[0], href=i[1], style={'color': 'white', 'text-decoration': 'none'})]))
    return html.Ul(className='nav nav-pills flex-column mb-auto', children=li_list, style={'margin-top': '20px'})


def bind_sidebar_callbacks(app, sidebar_id, sidebar_btn_id, sidebar_btn_memory_id):
    @app.callback(
        [Output(sidebar_id, 'style'),
         Output(sidebar_btn_memory_id, 'data')
         ],
        Input(sidebar_btn_id, 'n_clicks'),
        State(sidebar_btn_memory_id, 'data')
    )
    def open_close_sidebar(n_clicks, data):
        if n_clicks:
            if data == 'CLOSE':
                SIDEBAR_STYLE['right'] = '-280px'
                return (SIDEBAR_STYLE, 'OPEN')
            elif data == 'OPEN':
                SIDEBAR_STYLE['right'] = '0px'
                return (SIDEBAR_STYLE, 'CLOSE')
        return (SIDEBAR_STYLE, 'OPEN')
    return app
