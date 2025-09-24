from flask import Blueprint, request, jsonify

# Cria o Blueprint
questions = Blueprint("questions", __name__)

@questions.route("", methods=["POST"])
def create_question():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nenhum JSON enviado"}), 400

    return jsonify({
        "status": "sucesso",
        "received": data
    }), 201