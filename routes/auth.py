from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
import hashlib
from models.db import get_admin_hash, fetch_attempts
from config import ADMIN_USERNAME
from io import BytesIO
from datetime import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")

@auth_bp.route("/", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        form_user = request.form.get("username","").strip()
        form_pass = request.form.get("password","")
        admin_hash = get_admin_hash()
        if form_user == ADMIN_USERNAME and hashlib.sha256(form_pass.encode('utf-8')).hexdigest() == admin_hash:
            session["is_admin"] = True
            return redirect(url_for("auth.admin"))
        else:
            flash("Invalid admin credentials", "error")
            return redirect(url_for("auth.admin"))

    if not session.get("is_admin"):
        return render_template("admin.html", logged_in=False)

    rows = fetch_attempts()
    attempts = [{
        "id": r[0],
        "time": r[1],
        "username": r[2],
        "password_hash": r[3],
        "weak": bool(r[4]),
        "ip": r[5],
        "user_agent": r[6],
        "screen": r[7],
        "timezone": r[8]
    } for r in rows]
    return render_template("admin.html", logged_in=True, attempts=attempts)

@auth_bp.route("/export")
def export():
    if not session.get("is_admin"):
        return redirect(url_for("auth.admin"))
    rows = fetch_attempts()
    lines = []
    for r in rows:
        lines.append("\n".join([
            f"Time: {r[1]}",
            f"Username: {r[2]}",
            f"Password_hash: {r[3]}",
            f"Weak_password: {bool(r[4])}",
            f"IP: {r[5]}",
            f"UserAgent: {r[6]}",
            f"Screen: {r[7]}",
            f"Timezone: {r[8]}",
            "-"*30
        ]))
    content = "\n\n".join(lines) or "No attempts"
    bio = BytesIO()
    bio.write(content.encode("utf-8"))
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name=f"honeypot_report_{datetime.utcnow().isoformat()}.txt", mimetype="text/plain")

@auth_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("auth.admin"))
