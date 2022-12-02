from dash import html

def get_filter_title(title_text):
    return html.H6(title_text, style={'color': 'white', 'margin-top': '10px'})