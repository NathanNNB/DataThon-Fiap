import os
from flask_cors import CORS
from app import create_app

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    env = os.environ.get('ENV', 'local')  # default é local
    app.run(host='0.0.0.0', port=port, debug=True)