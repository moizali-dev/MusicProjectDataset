import os
import logging
from datetime import datetime, timedelta
import pendulum

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

from pythonscripts.music_classification_main import main

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

now = datetime.now().strftime("%Y_%m_%d")
local_tz = pendulum.timezone("Europe/Amsterdam")

default_args = {
    "start_date": pendulum.datetime(2022, 11, 18,2, tz="America/Toronto"),
    "retries": 1,
    'retry_delay': timedelta(minutes=1)
}

def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

with DAG(
    dag_id="MusicalOrchestration",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    SpotifyIngestion = PythonOperator(
        task_id = "IngestSpotify",  
        python_callable=main
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"dataset_{now}",
            "local_file": "Music_Classification_Dataset_test_new.csv",
        },
    )

    load_csv = GCSToBigQueryOperator(
    task_id='gcs_to_bigquery',
    bucket=BUCKET,
    source_objects=f"dataset_{now}",
    destination_project_dataset_table=f"musicprojects.musicprojects_staging.dataset_{now}",
    autodetect=True,
    skip_leading_rows=1,
    source_format="CSV",
    write_disposition='WRITE_TRUNCATE',
    dag=dag,
    )

    dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command="cd /opt/airflow/mc_dbt && dbt test "
    )

    dbt_run_staging = BashOperator(
    task_id="dbt_run_staging",
    bash_command="cd /opt/airflow/mc_dbt && dbt run --model analytics_staging "
    )

    dbt_run_analytics = BashOperator(
    task_id="dbt_run_analytics",
    bash_command="cd /opt/airflow/mc_dbt && dbt run --model analytics "
    )

    dbt_test_again = BashOperator(
    task_id="dbt_test_again",
    bash_command="cd /opt/airflow/mc_dbt && dbt test "
    )

    SpotifyIngestion >> local_to_gcs_task >> load_csv >> dbt_test >> dbt_run_staging >> dbt_run_analytics >> dbt_test_again



