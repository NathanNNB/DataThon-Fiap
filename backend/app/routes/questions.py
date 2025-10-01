from flask import Blueprint, request, jsonify
from app.utils.call_model import call_model
import time 
from datetime import datetime
import json 
import uuid
from google.cloud import bigquery

questions = Blueprint("questions", __name__)


client = bigquery.Client()
TABLE_ID = "datathon-473001.datathon.logs"

@questions.route("", methods=["POST"])
def create_question():
    data = request.get_json(silent=True)  # evita lançar erro 400 automático
    


    if not data:
        return jsonify({"error": "Nenhum JSON enviado"}), 400

    start_time = time.time()
    result, status = call_model(data)
    end_time = time.time()
    sec = end_time-start_time
    row = {
        "log_id": str(uuid.uuid4()),
        "json_sent": json.dumps(data),
        "json_received": json.dumps(result),
        "status": status,
        "time_to_run": str(sec)
    }

    client.insert_rows_json(TABLE_ID, [row])

    

    return jsonify(result), 201