from flask import Flask
from flask_cors import CORS
from .routes.questions import questions

def create_app():
    app = Flask(__name__)

    app.register_blueprint(questions, url_prefix="/questions")

    return app