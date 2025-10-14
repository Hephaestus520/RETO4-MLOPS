from google.cloud import bigquery

def load_to_bigquery(event, context):
    file = event['name']
    if not file.endswith(".csv"):
        return
    client = bigquery.Client()
    uri = f"gs://donostia-parking-data/{file}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_APPEND"
    )

    table_id = f"{client.project}.donostia_dataset.parking_data"
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
    print(f"✅ {file} cargado correctamente en {table_id}")
