from airflow import DAG 
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import os



def extract_users():
    """
    Fetches user data from randomuser api.
    """
    url = "https://randomuser.me/api/?results=10"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch users: {response.status_code}")


def load_users():
    users = extract_users()
    print(f"Used host: {os.getenv('POSTGRES_HOST')}")
    print(f"Used port: {os.getenv('POSTGRES_PORT')}")
    
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT', 5433)
    )
    print(f"Connected to PostgreSQL database:{conn}")
    cur = conn.cursor()

    for user in users['results']:
        cur.execute("""
            INSERT INTO users_userprofile (username, email, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
        """, (
            user["login"]["username"],
            user["email"],
            user["name"]["first"],
            user["name"]["last"]
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("Users loaded successfully.")



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'user_etl_dag',
    default_args=default_args,
    description='A simple user ETL DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:
    
    start_task = EmptyOperator(task_id='start')

    extract_task = PythonOperator(
        task_id='extract_users',
        python_callable=extract_users,
    )

    load_task = PythonOperator(
        task_id='load_users_to_postgres_db',
        python_callable=load_users,
    )

    end_task = EmptyOperator(task_id='end')

    start_task >> extract_task >> load_task >> end_task
