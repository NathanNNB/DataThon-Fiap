import pytest
from flask import Flask
from app.routes.questions import questions 

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(questions, url_prefix="/questions")
    with app.test_client() as client:
        yield client

def test_create_question_success(client):
    payload = {"questions": "alguma coisa"}
    response = client.post("/questions", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "sucesso"
    assert "received" in data
    assert "questions" in data
    assert isinstance(data["questions"], list)

def test_create_question_no_json(client):
    response = client.post(
        "/questions",
        data="",  # envia corpo vazio
        content_type="application/json"  # define o content-type corretamente
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Nenhum JSON enviado"