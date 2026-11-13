from __future__ import annotations
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection
from app.config import DATABASE_URL

engine: Engine = create_engine(DATABASE_URL, future=True)

def get_connection() -> Connection:
    return engine.begin()

def query_df(sql: str):
    import pandas as pd
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)
