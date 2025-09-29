from flask import Flask
from flask_cors import CORS
from .routes.questions import questions
from .routes.submit_evaluation import submit_evaluation

def create_app():
    app = Flask(__name__)

    # Habilita CORS em toda a aplicação
    CORS(app)

    # Registra o blueprint de questions
    app.register_blueprint(questions, url_prefix="/questions")
    app.register_blueprint(submit_evaluation, url_prefix="/submit_evaluation")
    return app