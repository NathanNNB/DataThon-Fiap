import os
from flask import Blueprint
from flask_cors import CORS

questions = Blueprint("questions", __name__)
CORS(questions)

print("Rota")