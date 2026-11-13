from __future__ import annotations
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, Input, Output
from app.database import query_df

app = Dash(__name__)
app.title = "Global Oil & Fuel Monitoring Platform"

def safe_query(sql: str) -> pd.DataFrame:
    try:
        return query_df(sql)
    except Exception:
        return pd.DataFrame()

def kpi_card(title: str, value: str):
    return html.Div(
        [html.Div(title, style={"fontSize": "12px", "color": "#666"}),
         html.Div(value, style={"fontSize": "24px", "fontWeight": "700", "marginTop": "4px"})],
        style={"background":"white","padding":"14px","borderRadius":"12px","border":"1px solid #e5e7eb"}
    )

app.layout = html.Div([
    dcc.Interval(id="refresh", interval=300000, n_intervals=0),
    html.H1("Global Oil & Fuel Monitoring Platform"),
    html.Div("Dashboard branché à PostgreSQL + ETL Airflow-ready", style={"color":"#666","marginBottom":"12px"}),
    html.Div(id="kpis", style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)","gap":"12px","marginBottom":"16px"}),
    dcc.Tabs([
        dcc.Tab(label="Benchmarks", children=[
            dcc.Graph(id="fig-oil")
        ]),
        dcc.Tab(label="USA", children=[
            dcc.Graph(id="fig-us-map"),
            dcc.Graph(id="fig-us-region")
        ]),
        dcc.Tab(label="Monde", children=[
            dcc.Graph(id="fig-world"),
            dash_table.DataTable(id="world-table", page_size=10, style_table={"overflowX":"auto"})
        ])
    ])
], style={"maxWidth":"1400px","margin":"0 auto","padding":"20px","background":"#f3f4f6","minHeight":"100vh"})

@app.callback(
    Output("kpis", "children"),
    Output("fig-oil", "figure"),
    Output("fig-us-map", "figure"),
    Output("fig-us-region", "figure"),
    Output("fig-world", "figure"),
    Output("world-table", "data"),
    Output("world-table", "columns"),
    Input("refresh", "n_intervals"),
)
def refresh(_):
    oil = safe_query("SELECT * FROM oil_prices ORDER BY price_date")
    us = safe_query("SELECT * FROM fuel_prices_us_states ORDER BY price_date")
    world = safe_query("SELECT * FROM fuel_prices_world")
    kpis = safe_query("SELECT * FROM dashboard_kpis")

    metric_map = {row["metric_name"]: row["metric_value"] for _, row in kpis.iterrows()} if not kpis.empty else {}
    cards = [
        kpi_card("Brent", metric_map.get("Brent", "N/A")),
        kpi_card("WTI", metric_map.get("WTI", "N/A")),
        kpi_card("AAA US AVG", metric_map.get("AAA_US_AVG", "N/A")),
        kpi_card("World Rows", metric_map.get("WORLD_ROWS", "N/A")),
    ]

    if oil.empty:
        fig_oil = px.line(title="Aucune donnée pétrole")
    else:
        fig_oil = px.line(oil, x="price_date", y="close", color="benchmark", title="Benchmarks énergie")

    if us.empty:
        fig_us_map = px.scatter(title="Aucune donnée AAA")
        fig_us_region = px.bar(title="Aucune donnée AAA")
    else:
        latest_date = us["price_date"].max()
        us_latest = us[us["price_date"] == latest_date].copy()
        fig_us_map = px.choropleth(us_latest, locations="abbr", locationmode="USA-states", color="regular",
                                   scope="usa", hover_name="state", title="Prix essence US par État")
        region_df = us_latest.groupby("region", as_index=False)["regular"].mean().sort_values("regular", ascending=False)
        fig_us_region = px.bar(region_df, x="region", y="regular", title="Moyenne par région US")

    if world.empty:
        fig_world = px.scatter(title="Aucune donnée monde")
        world_data = []
        world_cols = []
    else:
        fig_world = px.choropleth(world, locations="country", locationmode="country names", color="price",
                                  hover_name="country", title="Prix carburant monde")
        world_data = world.to_dict("records")
        world_cols = [{"name": c, "id": c} for c in world.columns]

    return cards, fig_oil, fig_us_map, fig_us_region, fig_world, world_data, world_cols
