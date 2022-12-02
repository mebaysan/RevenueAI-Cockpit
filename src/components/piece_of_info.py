from dash import html


def get_piece_of_info(title_text='2021', sub_title_text='Data Category', icon_src='/assets/logo/logo.png'):
    return html.Div(className='col align-self-center', style={'margin-right': '15px'}, children=[
        html.Div(className='row', children=[
            html.Div(className='col', style={'margin-right': '-65px'}, children=[
                     html.Img(src=icon_src, width=60, height=60)]),
            html.Div(className='col', children=[
                    html.H2(title_text, style={'margin-bottom': '-5px'}),
                    html.Small(sub_title_text, className='text-muted')
                    ])
        ]),

    ])
