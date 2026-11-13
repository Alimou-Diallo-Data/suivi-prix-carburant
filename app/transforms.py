from __future__ import annotations
import pandas as pd

def build_latest_kpis(energy_df: pd.DataFrame, us_df: pd.DataFrame, world_df: pd.DataFrame) -> dict:
    out = {}
    if not energy_df.empty:
        last = energy_df.sort_values("price_date").groupby("benchmark").tail(1)
        for _, row in last.iterrows():
            out[row["benchmark"]] = float(row["close"])

    if not us_df.empty:
        out["AAA_US_AVG"] = float(us_df["regular"].mean())
        out["AAA_US_MAX_STATE"] = str(us_df.sort_values("regular", ascending=False).iloc[0]["state"])

    if not world_df.empty:
        out["WORLD_ROWS"] = int(len(world_df))
        out["WORLD_COUNTRIES"] = int(world_df["country"].nunique())

    return out
