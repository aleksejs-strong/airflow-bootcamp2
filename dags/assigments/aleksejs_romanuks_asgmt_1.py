from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator
import random

default_args = {
    'retries': 0,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
        dag_id="aleksejs_romanuks_asgmt_1",
        start_date=datetime(2022, 6, 20),
        schedule_interval="*/10 * * * *",
        default_args=default_args,
        catchup=False
) as dag:

    number_1_generator_operator = PythonOperator(
        task_id="number_1_generator",
        python_callable=lambda: random.randint(0, 10)
    )

    number_2_generator_operator = PythonOperator(
        task_id="number_2_generator",
        python_callable=lambda: random.randint(0, 10)
    )

    def compare_numbers(**kwargs):
        task_instance = kwargs['ti']
        number1 = task_instance.xcom_pull(task_ids='number_1_generator')
        number2 = task_instance.xcom_pull(task_ids='number_2_generator')

        if number1 == number2:
            return "equal"
        elif number1 > number2:
            return "number_1_greater"
        else:
            return "number_2_greater"


    branch_operator = BranchPythonOperator(
        task_id='branch',
        python_callable=compare_numbers,
        provide_context=True,
        trigger_rule='all_done'
    )

    number_1_generator_operator.set_downstream(branch_operator)
    number_2_generator_operator.set_downstream(branch_operator)

    for case in ["equal", "number_1_greater", "number_2_greater"]:
        branch_operator >> DummyOperator(task_id=case)




