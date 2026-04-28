from google.cloud import bigquery
from google.oauth2 import service_account
from config import PROJECT_ID, DATASET_ID, TABLE_ID, CREDENTIALS_PATH
import pandas as pd

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

def insert_rows(rows: list):
    df = pd.DataFrame(rows)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema=[
            bigquery.SchemaField("timestamp", "TIMESTAMP"),
            bigquery.SchemaField("device_id", "STRING"),
            bigquery.SchemaField("data_type", "STRING"),
            bigquery.SchemaField("temperature", "FLOAT"),
            bigquery.SchemaField("humidity", "FLOAT"),
            bigquery.SchemaField("log_level", "STRING"),
            bigquery.SchemaField("message", "STRING"),
            bigquery.SchemaField("response_time_ms", "INTEGER"),
        ]
    )
    
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # wait for job to complete
    print(f"✅ Inserted {len(rows)} rows via batch load")