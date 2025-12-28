from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "ops_automation",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ops_workflow_automation",
    start_date=datetime(2024, 6, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    description="End-to-end ops workflow automation",
) as dag:

    ingest = BashOperator(
        task_id="ingest_external_data",
        bash_command="python ingest.py",
    )

    transform = BashOperator(
        task_id="validate_transform_data",
        bash_command="python transformation.py",
    )

    load = BashOperator(
        task_id="load_analytics_db",
        bash_command="python load_to_postgres.py",
    )

    ingest >> transform >> load
