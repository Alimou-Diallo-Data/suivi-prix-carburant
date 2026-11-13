from __future__ import annotations
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="petrol_pipeline",
    start_date=datetime(2026, 3, 1),
    schedule="0 */6 * * *",
    catchup=False,
    tags=["petrol", "etl", "portfolio"],
) as dag:
    init_db = BashOperator(
        task_id="init_db",
        bash_command="cd /opt/airflow/project && python run.py init-db"
    )

    run_etl = BashOperator(
        task_id="run_etl",
        bash_command="cd /opt/airflow/project && python run.py etl"
    )

    init_db >> run_etl
