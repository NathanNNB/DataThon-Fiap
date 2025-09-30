import os
from flask_cors import CORS
from flask import request, redirect
from app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix  # 👈 IMPORTANTE

app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # 👈 ESSENCIAL
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def enforce_https():
    if os.getenv("FLASK_ENV") == "production":
        if request.method != "OPTIONS":  # 👈 importante
            if request.headers.get("X-Forwarded-Proto", "http") != "https":
                url = request.url.replace("http://", "https://", 1)
                return redirect(url, code=308)
            
if __name__ == "__main__":
    app.run(debug=True)