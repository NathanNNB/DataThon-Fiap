from flask import Blueprint, request, jsonify

questions = Blueprint("questions", __name__)

@questions.route("", methods=["POST"])
def create_question():
    data = request.get_json(silent=True)  # evita lançar erro 400 automático

    if not data:
        return jsonify({"error": "Nenhum JSON enviado"}), 400

    return jsonify({
        "status": "sucesso",
        "received": data,
        "questions": ["Questão 1", "Questão 2", "Questão 3"]
    }), 201