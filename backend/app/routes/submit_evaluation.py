from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from google.cloud import bigquery
from datetime import datetime
import uuid
import json


# --- Inicializa o cliente BigQuery ---
client = bigquery.Client()
TABLE_ID = "datathon-473001.datathon.evaluations"

# --- Criação do Blueprint ---
submit_evaluation = Blueprint("submit_evaluation", __name__)

@submit_evaluation.route("/", methods=["POST", "OPTIONS"], strict_slashes=False)
@cross_origin() 
def handle_submit_evaluation():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum JSON enviado"}), 400

    json_sent = data.get("json_sent")
    json_received = data.get("json_received")
    rating = data.get("rating")

    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"error": "Rating inválido. Deve ser inteiro de 1 a 5."}), 400

    row = {
        "evaluation_id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat() + "Z",  # ISO 8601 UTC
        "json_sent": json.dumps(json_sent),
        "json_received": json.dumps(json_received),
        "rating": rating,
        "questions_count": len(json_received.get("questions", [])) if json_received else 0,
        "candidate_summary": json_received.get("candidateSummary", "") if json_received else "",
        "job_summary": json_received.get("jobSummary", "") if json_received else ""
    }

    errors = client.insert_rows_json(TABLE_ID, [row])
    if errors:
        return jsonify({"error": "Erro ao inserir no BigQuery", "details": errors}), 500

    return jsonify({"message": "Avaliação registrada com sucesso!", "evaluation_id": row["evaluation_id"]})




