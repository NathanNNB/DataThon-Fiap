import pytest
from app.utils.model_rag import RAGRecrutamento

def test_rag_output():
    curriculo = "João, experiência em Python, endereço SP, objetivo Desenvolvedor, tempo de experiência 5 anos, formação superior, inglês avançado, hard-skills: Python, soft-skills: comunicação."
    vaga = "Desenvolvedor, requisitos: Python, soft-skills: trabalho em equipe, extras: remoto."
    rag_model = RAGRecrutamento()
    result = rag_model.rag(curriculo, vaga, max_tokens=300)
    assert isinstance(result, dict)
    assert "candidateSummary" in result
    assert "jobSummary" in result
    assert "questions" in result
    assert isinstance(result["questions"], list)
    assert len(result["questions"]) == 5
