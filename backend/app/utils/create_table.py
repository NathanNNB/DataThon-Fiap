from google.cloud import bigquery

client = bigquery.Client()

project_id = "datathon-473001"
dataset_id = "datathon"   # troque para o nome do seu dataset
table_name = "evaluations"

# Garante que o dataset existe
dataset_ref = bigquery.Dataset(f"{project_id}.{dataset_id}")
try:
    client.get_dataset(dataset_ref)
    print(f"✅ Dataset {dataset_id} já existe.")
except Exception:
    dataset = client.create_dataset(dataset_ref)
    print(f"📦 Dataset criado: {dataset.dataset_id}")

# Schema da tabela
schema = [
    bigquery.SchemaField("evaluation_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("json_sent", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("json_received", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("rating", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("questions_count", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("candidate_summary", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("job_summary", "STRING", mode="NULLABLE"),
]

table_id = f"{project_id}.{dataset_id}.{table_name}"
table = bigquery.Table(table_id, schema=schema)

try:
    client.create_table(table)
    print(f"✅ Tabela criada: {table_id}")
except Exception as e:
    print(f"⚠️ Erro ao criar tabela: {e}")

