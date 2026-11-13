from app.transforms import build_latest_kpis
import pandas as pd

def test_build_latest_kpis():
    energy = pd.DataFrame([
        {"price_date":"2026-03-29","benchmark":"Brent","close":110.3},
        {"price_date":"2026-03-29","benchmark":"WTI","close":96.2},
    ])
    us = pd.DataFrame([
        {"state":"California","regular":5.5},
        {"state":"Texas","regular":3.4},
    ])
    world = pd.DataFrame([
        {"country":"Canada","price":1.78},
        {"country":"France","price":1.95},
    ])

    out = build_latest_kpis(energy, us, world)
    assert out["Brent"] == 110.3
    assert out["WTI"] == 96.2
    assert out["WORLD_COUNTRIES"] == 2
