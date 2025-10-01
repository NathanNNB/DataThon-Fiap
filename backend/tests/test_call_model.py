import pytest
from app.utils.call_model import call_model

def test_call_model_valid_payload():
    payload = {
        "curriculo": "João, experiência em Python, endereço SP, objetivo Desenvolvedor, tempo de experiência 5 anos, formação superior, inglês avançado, hard-skills: Python, soft-skills: comunicação.",
        "job_description": "Desenvolvedor, requisitos: Python, soft-skills: trabalho em equipe, extras: remoto."
    }
    result, status = call_model(payload)
    assert status == 200
    assert isinstance(result, dict)
    assert "candidateSummary" in result
    assert "jobSummary" in result
    assert "questions" in result
    assert "compatibility_rate" in result

def test_call_model_missing_fields():
    payload = {"curriculo": "", "job_description": ""}
    result = call_model(payload)
    assert "Both 'curriculo' and 'job_description' must be provided and non-empty." in result

def test_call_model_invalid_json():
    payload = "not a json string"
    result, status = call_model(payload)
    assert status == 400
