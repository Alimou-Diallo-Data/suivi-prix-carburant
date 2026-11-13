from __future__ import annotations

import sys
from app.database import engine, get_connection
from app.config import DASH_HOST, DASH_PORT
from app.etl import run_etl
from app.dashboard import app

def init_db() -> None:
    from pathlib import Path
    sql_file = Path("sql/create_tables.sql")
    with get_connection() as conn:
        conn.execute(sql_file.read_text(encoding="utf-8"))

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python run.py [init-db|etl|dashboard]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init-db":
        init_db()
        print("Base initialisée.")
    elif cmd == "etl":
        run_etl()
        print("ETL terminé.")
    elif cmd == "dashboard":
        app.run(host=DASH_HOST, port=DASH_PORT, debug=True)
    else:
        print(f"Commande inconnue: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
