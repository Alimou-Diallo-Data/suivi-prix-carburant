from __future__ import annotations
import pandas as pd
from sqlalchemy import text
from app.api_clients import fetch_energy_futures, fetch_aaa_state_prices, load_world_prices
from app.transforms import build_latest_kpis
from app.database import engine

def run_etl() -> None:
    energy_df = fetch_energy_futures()
    us_df = fetch_aaa_state_prices()
    world_df = load_world_prices()

    with engine.begin() as conn:
        if not energy_df.empty:
            energy_df.to_sql("oil_prices", conn, if_exists="append", index=False)
        if not us_df.empty:
            us_df.to_sql("fuel_prices_us_states", conn, if_exists="append", index=False)
        if not world_df.empty:
            conn.execute(text("DELETE FROM fuel_prices_world"))
            world_df.to_sql("fuel_prices_world", conn, if_exists="append", index=False)

        kpis = build_latest_kpis(energy_df, us_df, world_df)
        if kpis:
            conn.execute(text("DELETE FROM dashboard_kpis"))
            pd.DataFrame(
                [{"metric_name": k, "metric_value": str(v)} for k, v in kpis.items()]
            ).to_sql("dashboard_kpis", conn, if_exists="append", index=False)
