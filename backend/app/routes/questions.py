from flask import Blueprint, request, jsonify
from utils.call_model import call_model
questions = Blueprint("questions", __name__)

@questions.route("", methods=["POST"])
def create_question():
    data = request.get_json(silent=True)  # evita lançar erro 400 automático
    


    if not data:
        return jsonify({"error": "Nenhum JSON enviado"}), 400

    result, mensagem = call_model(data)
    
    return jsonify({
        
        "questions": [
            "Explique sua experiência com controle de budget e KPIs.",
            "Como você lida com fechamento contábil e fiscal?",
            "Quais sistemas ERP você já utilizou?",
            "Descreva um desafio que você enfrentou na área financeira e como resolveu.",
            "Como você automatiza processos usando Excel ou outros softwares?"
        ],
        "candidateSummary": "Carolina Aparecida é uma profissional com experiência nos departamentos financeiro, contábil, fiscal e de controladoria jurídica. Possui formação em Ciências Contábeis e Gestão Financeira, e habilidades em contas a pagar/receber, indicadores KPI, fechamento contábil, emissão de boletos, impostos e budget.",
        "jobSummary": "A vaga é para assistente financeiro/contábil em empresa de médio porte, com foco em controladoria, fechamento contábil e análise de indicadores financeiros. É necessário conhecimento em sistemas ERP e Excel avançado."
        
    }), 201