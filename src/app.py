from dash import Dash, html, dcc, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

#############
from components.header import get_header
from components.piece_of_info import get_piece_of_info
from components.figure_col import get_figure_col, get_card_col
from components.sidebar import get_sidebar, get_sidebar_list, bind_sidebar_callbacks
from components.filters import get_dropdown
from helpers.format import format_big_number


def get_data():
    df = pd.read_csv("commodity_trade_statistics_data.csv", low_memory=False)
    df.sort_values("year", ascending=True, inplace=True)
    return df


# load the data and cache (simulating) it to filter out by using the inputs
DF = get_data()


app = Dash(__name__)


########################## Sidebar Menu ##########################
menu_content_children = get_sidebar_list(
    "Menu Item 1", [("Sub Menu Item 1.1", "/"), ("Sub Menu Item 1.2", "/")]
)


menu_content = html.Div(children=[menu_content_children])
########################## ++++++ ##########################

########################## Filter Menu ##########################
# generate filter options list
dd_year_options = [
    {"label": year, "value": year} for year in sorted(DF["year"].unique().tolist())
]

dd_area_options = [
    {"label": year, "value": year}
    for year in sorted(DF["country_or_area"].unique().tolist())
]

dd_area_options.insert(0, {"label": "All", "value": "All"})

dd_measurement_options = [
    {"label": "Trade (USD)", "value": "trade_usd"},
    {"label": "Weight (kg)", "value": "weight_kg"},
    {"label": "Quantity", "value": "quantity"},
]


filter_content = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col",
                    children=[
                        get_dropdown(
                            "dd-start",
                            dd_year_options,
                            "Start Year",
                            DF["year"].min(),
                        ),
                    ],
                ),
                html.Div(
                    className="col",
                    children=[
                        get_dropdown(
                            "dd-end",
                            dd_year_options,
                            "End Year",
                            DF["year"].max(),
                        ),
                    ],
                ),
            ],
        ),
        get_dropdown(
            "dd-area",
            dd_area_options,
            "Country (Area)",
            "All",
        ),
        get_dropdown(
            "dd-measurement-unit",
            dd_measurement_options,
            "Measurement Unit",
            dd_measurement_options[0]["value"],
        ),
    ]
)
########################## ++++++ ##########################

########################## APP Layout ##########################
app.layout = html.Div(
    style={"background": "#f3f3f3"},
    children=[
        get_header(
            "Revenue.AI Cockpit",
            [
                {
                    "className": "bi bi-funnel",
                    "id": "filter-icon",
                    "memory-id": "filter-memory",
                },
                {
                    "className": "bi bi-list",
                    "id": "menu-icon",
                    "memory-id": "menu-memory",
                },
            ],
        ),
        get_sidebar("menu-div", "Menu", menu_content),
        get_sidebar("filter-div", "FILTERS", filter_content),
        html.Div(
            className="container",
            style={"height": "1000px"},
            children=[
                # Summary statistics
                html.Div(
                    className="row mt-4",
                    id="summary-statistics-div",
                    children=[],
                ),
                # Figures
                html.Div(
                    className="row mt-4",
                    children=[
                        get_figure_col("fig-flow", "Flow Ratio"),
                        get_figure_col("fig-export-map", "Export Totals by Year", 7),
                    ],
                ),
                html.Div(
                    className="row mt-4",
                    children=[
                        get_card_col("raw-data-table-div", "Raw Data"),
                    ],
                ),
            ],
        ),
    ],
)
########################## ++++++ ##########################

# Binding sidebar callbacks to main app
app = bind_sidebar_callbacks(app, "menu-div", "menu-icon", "menu-memory")
app = bind_sidebar_callbacks(app, "filter-div", "filter-icon", "filter-memory")

# defining global inputs
GLOBAL_FIGURE_INPUTS = [
    Input("dd-start", "value"),
    Input("dd-end", "value"),
    Input("dd-area", "value"),
    Input("dd-measurement-unit", "value"),
]

# filter df by using input parameters
def filter_df(df, dd_start, dd_end, dd_area):
    filtered_df = df[(df["year"] >= dd_start) & (df["year"] <= dd_end)]
    if dd_area != "All":
        filtered_df = filtered_df[filtered_df["country_or_area"] == dd_area]
    return filtered_df


@app.callback(Output("summary-statistics-div", "children"), [*GLOBAL_FIGURE_INPUTS])
def get_summary_statistics_cards(dd_start, dd_end, dd_area, dd_m_unit):
    filtered_df = filter_df(DF, dd_start, dd_end, dd_area)
    cards = [
        get_piece_of_info(
            filtered_df["country_or_area"].unique().shape[0],
            "Total Countries",
            "/assets/icons/countries.png",
        ),
        get_piece_of_info(
            filtered_df["commodity"].unique().shape[0],
            "Commodities",
            "/assets/icons/commodity.png",
        ),
        get_piece_of_info(
            format_big_number(filtered_df.shape[0]),
            "Unique Flows",
            "/assets/icons/flow.png",
        ),
        get_piece_of_info(
            format_big_number(filtered_df["trade_usd"].sum()),
            "Total Trade (USD)",
            "/assets/icons/trade.png",
        ),
        get_piece_of_info(
            format_big_number(filtered_df["weight_kg"].sum()),
            "Total Weight (KG)",
            "/assets/icons/weight.png",
        ),
        get_piece_of_info(
            format_big_number(filtered_df["quantity"].sum()),
            "Total Quantity",
            "/assets/icons/quantity.png",
        ),
    ]
    return cards


@app.callback(Output("fig-flow", "figure"), [*GLOBAL_FIGURE_INPUTS])
def get_flow_fig(dd_start, dd_end, dd_area, dd_m_unit):
    filtered_df = filter_df(DF, dd_start, dd_end, dd_area)
    filtered_df = filtered_df.groupby(["flow"], as_index=False).agg({dd_m_unit: "sum"})
    fig = px.pie(
        filtered_df,
        names="flow",
        labels="flow",
        values=dd_m_unit,
        color_discrete_sequence=["#00AFB9", "#FDFCDC", "#FED9B7", "#F07167"],
    )

    fig = fig.update_layout(
        margin={"t": 20, "r": 0, "b": 45},
        width=350,
        height=350,
        template="simple_white",
        showlegend=True,
    )
    fig = fig.update_traces(
        textposition="none",
        hovertemplate="Flow: <b> %{label} </b><br>"
        + f"Total {dd_m_unit}:"
        + "<b> %{value:.2f}</b>",
    )
    return fig


@app.callback(Output("fig-export-map", "figure"), [*GLOBAL_FIGURE_INPUTS])
def get_export_map_div(dd_start, dd_end, dd_area, dd_m_unit):
    filtered_df = filter_df(DF, dd_start, dd_end, dd_area)
    filtered_df = filtered_df[filtered_df["flow"] == "Export"]
    filtered_df = (
        filtered_df.groupby(["country_or_area", "year", "flow"], as_index=False)
        .agg({dd_m_unit: "sum"})
        .sort_values("year", ascending=True)
    )
    fig = px.scatter_geo(
        filtered_df,
        locations="country_or_area",
        hover_name="country_or_area",
        size=dd_m_unit,
        locationmode="country names",
        projection="natural earth",
        animation_frame="year",
        color_discrete_sequence=["#00AFB9", "#FDFCDC", "#FED9B7", "#F07167"],
    )
    fig = fig.update_layout(
        margin={"t": 20, "r": 0, "b": 0},
        height=350,
        template="simple_white",
        showlegend=True,
    )
    return fig


@app.callback(Output("raw-data-table-div", "children"), [*GLOBAL_FIGURE_INPUTS])
def fig_demo_draw(dd_start, dd_end, dd_area, dd_m_unit):
    filtered_df = filter_df(DF, dd_start, dd_end, dd_area)
    filtered_df = filtered_df.groupby(
        ["country_or_area", "flow", "category"], as_index=False
    ).agg({dd_m_unit: "sum"})

    print(filtered_df)

    dt = dash_table.DataTable(
        filtered_df.to_dict("records"),
        [{"name": " ".join(i.split("_")), "id": i} for i in filtered_df.columns],
        id="raw-data-table",
        page_size=8,
    )
    return dt


if __name__ == "__main__":
    app.run_server(debug=False)
