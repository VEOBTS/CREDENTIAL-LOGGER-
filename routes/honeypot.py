from flask import Blueprint, render_template, request
import os
from models.db import record_attempt
from config import BASE_DIR

honeypot_bp = Blueprint("honeypot", __name__)
DICT_PATH = os.path.join(BASE_DIR, "dictionary.txt")
USERS_PATH = os.path.join(BASE_DIR, "users.txt")

# load dictionary and users once (on import)
def load_set(path):
    s = set()
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                w = line.strip()
                if w:
                    s.add(w)
    except FileNotFoundError:
        pass
    return s

DICTIONARY = load_set(DICT_PATH)
USERS = load_set(USERS_PATH)

@honeypot_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@honeypot_bp.route("/login", methods=["POST"])
def login():
    form = request.form
    username = form.get("username", "").strip() or "unknown"
    password = form.get("password", "") or ""
    screen = form.get("screen", "")
    tz = form.get("timezone", "")
    ua = request.headers.get("User-Agent", "")
    ip = request.remote_addr or "unknown"

    weak = password in DICTIONARY

    # record attempt (password plain is used only to compute hash inside record_attempt)
    record_attempt(username, password, weak, ip, ua, screen, tz)

    # If username is in users.txt: treat as "successful" for demo (NOT admin)
    is_known_user = username in USERS

    # Show successful or unsuccessful message to the user accordingly (demo)
    return render_template("index.html", submitted=True, username=username, success=is_known_user)
