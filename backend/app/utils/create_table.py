from google.cloud import bigquery
import uuid
from datetime import datetime
import json

# Inicializa cliente
client = bigquery.Client()

table_id = "seu_projeto.seu_dataset.model_evaluations"

def insert_evaluation(json_sent, json_received, rating):
    rows_to_insert = [
        {
            "evaluation_id": str(uuid.uuid4()),
            "created_at": datetime.utcnow(),
            "json_sent": json.dumps(json_sent),
            "json_received": json.dumps(json_received),
            "rating": rating,
            "questions_count": len(json_received.get("questions", [])),
            "candidate_summary": json_received.get("candidateSummary", ""),
            "job_summary": json_received.get("jobSummary", "")
        }
    ]
    
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print("Erro ao inserir avaliação:", errors)
    else:
        print("Avaliação inserida com sucesso!")