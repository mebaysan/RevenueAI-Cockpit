from dash import html, dcc
from components.typography import get_filter_title


def get_dropdown(
    dd_id,
    dd_options,
    dd_title,
    default_value="All",
    is_multi=False,
    dd_grid_class="row",
):
    dd = dcc.Dropdown(id=dd_id, options=dd_options, value=default_value, multi=is_multi)

    return html.Div(className=dd_grid_class, children=[get_filter_title(dd_title), dd])


def get_date_picker_single(dp_id, dp_title, dp_date, dp_grid_class="row"):
    dp = dcc.DatePickerSingle(id=dp_id, date=dp_date)
    return html.Div(className=dp_grid_class, children=[get_filter_title(dp_title), dp])
