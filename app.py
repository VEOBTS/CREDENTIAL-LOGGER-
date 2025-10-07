from flask import Flask
from routes.honeypot import honeypot_bp
from routes.auth import auth_bp
from models.db import ensure_db
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ensure DB exists and admin hash set
ensure_db()

# register blueprints
app.register_blueprint(honeypot_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
