from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow import DAG
from datetime import datetime


with DAG(
    dag_id="example_dag_5",
    start_date=datetime(2022, 6, 20),
    schedule_interval="*/1 * * * *",
    catchup=True
) as dag:

    submit_job = SparkSubmitOperator(
        application="/home/ubuntu/airflow_workspace/spark-apps/simple_app.py", 
        task_id="submit_job",
        conn_id="spark_local"
    )