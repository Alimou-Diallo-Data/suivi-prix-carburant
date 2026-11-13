from __future__ import annotations

from pathlib import Path
import math
import pandas as pd
import yfinance as yf

USA_STATE_TO_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

US_REGION_MAP = {
    "CT": "Northeast", "ME": "Northeast", "MA": "Northeast", "NH": "Northeast", "RI": "Northeast",
    "VT": "Northeast", "NJ": "Northeast", "NY": "Northeast", "PA": "Northeast", "DE": "Northeast",
    "MD": "Northeast", "DC": "Northeast",
    "IL": "Midwest", "IN": "Midwest", "MI": "Midwest", "OH": "Midwest", "WI": "Midwest",
    "IA": "Midwest", "KS": "Midwest", "MN": "Midwest", "MO": "Midwest", "NE": "Midwest",
    "ND": "Midwest", "SD": "Midwest",
    "FL": "South", "GA": "South", "NC": "South", "SC": "South", "VA": "South", "WV": "South",
    "AL": "South", "KY": "South", "MS": "South", "TN": "South", "AR": "South", "LA": "South",
    "OK": "South", "TX": "South",
    "AZ": "West", "CO": "West", "ID": "West", "MT": "West", "NV": "West", "NM": "West",
    "UT": "West", "WY": "West", "AK": "West", "CA": "West", "HI": "West", "OR": "West", "WA": "West"
}

def safe_float(value: str):
    try:
        return float(str(value).replace("$", "").replace(",", "").strip())
    except Exception:
        return None

def fetch_energy_futures() -> pd.DataFrame:
    tickers = {
        "Brent": "BZ=F",
        "WTI": "CL=F",
        "RBOB Gasoline": "RB=F",
        "Heating Oil": "HO=F",
        "Natural Gas": "NG=F",
    }

    rows = []
    for benchmark, ticker in tickers.items():
        try:
            hist = yf.download(ticker, period="1mo", interval="1d", progress=False, auto_adjust=False)
            if hist is None or hist.empty:
                continue
            hist = hist.reset_index()
            date_col = "Date" if "Date" in hist.columns else hist.columns[0]
            use = hist[[date_col, "Open", "High", "Low", "Close", "Volume"]].copy()
            use.columns = ["price_date", "open", "high", "low", "close", "volume"]
            use["benchmark"] = benchmark
            use["price_date"] = pd.to_datetime(use["price_date"]).dt.date
            rows.append(use)
        except Exception:
            continue

    if not rows:
        return pd.DataFrame(columns=["price_date", "open", "high", "low", "close", "volume", "benchmark"])
    return pd.concat(rows, ignore_index=True)

def fetch_aaa_state_prices() -> pd.DataFrame:
    urls = [
        "https://gasprices.aaa.com/state-gas-price-averages/",
        "https://gasprices.aaa.com/",
    ]
    for url in urls:
        try:
            tables = pd.read_html(url)
            chosen = None
            for tbl in tables:
                cols = [str(c).lower() for c in tbl.columns]
                if any("state" in c for c in cols) and any("regular" in c for c in cols):
                    chosen = tbl
                    break
            if chosen is None:
                continue

            normalized = {str(c).strip().lower(): c for c in chosen.columns}
            state_col = next((normalized[c] for c in normalized if "state" in c), None)
            reg_col = next((normalized[c] for c in normalized if "regular" in c), None)
            if not state_col or not reg_col:
                continue

            df = chosen[[state_col, reg_col]].copy()
            df.columns = ["state", "regular"]
            df["regular"] = df["regular"].map(safe_float)
            df = df.dropna(subset=["regular"])
            df["abbr"] = df["state"].map(USA_STATE_TO_ABBR)
            df = df.dropna(subset=["abbr"])
            df["region"] = df["abbr"].map(US_REGION_MAP).fillna("Other")
            df["price_date"] = pd.Timestamp.utcnow().date()
            return df[["price_date", "state", "abbr", "region", "regular"]]
        except Exception:
            continue

    return pd.DataFrame(columns=["price_date", "state", "abbr", "region", "regular"])

def load_world_prices(csv_path: str = "world_fuel_prices.csv") -> pd.DataFrame:
    path = Path(csv_path)
    cols = ["country", "region", "city", "fuel_type", "price", "unit", "currency", "last_update", "source"]
    if not path.exists():
        return pd.DataFrame(columns=cols)
    df = pd.read_csv(path)
    for col in cols:
        if col not in df.columns:
            df[col] = None
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["country", "price"])
    return df[cols]
