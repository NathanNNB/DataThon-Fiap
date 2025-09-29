from flask import Blueprint, request, jsonify

questions = Blueprint("questions", __name__)

@questions.route("", methods=["POST"])

@app.route("/submit_evaluation", methods=["POST"])
def submit_evaluation():
    """
    Espera receber um JSON com:
    {
        "json_sent": {...},
        "json_received": {...},
        "rating": 4
    }
    """
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
        "created_at": datetime.utcnow(),
        "json_sent": json.dumps(json_sent),
        "json_received": json.dumps(json_received),
        "rating": rating,
        "questions_count": len(json_received.get("questions", [])) if json_received else 0,
        "candidate_summary": json_received.get("candidateSummary", "") if json_received else "",
        "job_summary": json_received.get("jobSummary", "") if json_received else ""
    }

    errors = client.insert_rows_json(TABLE_ID, [row])
    if errors:
        return jsonify({"error": errors}), 500

    return jsonify({"message": "Avaliação registrada com sucesso!", "evaluation_id": row["evaluation_id"]})