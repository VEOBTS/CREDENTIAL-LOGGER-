## A local, consent-gated honeypot for educational / authorized testing built with Flask + SQLite + vanilla JS/CSS.
This repo logs hashed credential attempts and basic client metadata (IP, user‑agent, screen size, timezone) for learning and testing only. Do not deploy to public internet or collect real users’ credentials without explicit informed consent.

Demo / Project goals
Provide a realistic-looking login page that explicitly requires consent before use.

Record only safe data: timestamp, username (as typed), SHA‑256 hash of attempted password, boolean if password equals a dictionary word, client metadata (IP, UA, screen, timezone).

Allow a list of demo users (users.txt) — if username is in that list the site shows a successful login (demo behavior).

Admin panel (/admin) protected by secure hashed password, to view and export logs as .txt.

Keep everything local and auditable. No plaintext password storage.
<><><><><><><><><><>

Attempts stored in SQLite (honeypot.db) — schema: timestamp, username, password_hash (SHA‑256), weak flag, ip, user_agent, screen, timezone.

Admin authentication uses Werkzeug password hashing (PBKDF2 by default). set_admin.py helper to set/change admin password.

Admin can export logs (/admin/export) as a .txt report.

Frontend collects screen size & timezone via JS and posts them as hidden fields.

Repo structure (what each file/folder is for)
safe-honeypot/
├── app.py                # Flask app entrypoint — registers blueprints & starts server
├── config.py             # Config values (DB path, secret key, admin defaults)
├── requirements.txt      # pip dependencies (Flask)
├── dictionary.txt        # Weak password list (one per line)
├── users.txt             # Demo usernames (one per line)
├── README.md             # (this file)
├── set_admin.py          # CLI helper to securely set admin password (recommended)
├── honeypot.db           # SQLite DB (created automatically)
│
├── models/
│   └── db.py             # DB helpers: init, insert attempt, fetch attempts, admin hash helpers
│
├── routes/
│   ├── honeypot.py       # Landing page (/) and /login route
│   └── auth.py           # /admin routes: login, view attempts, export, logout
│
├── static/
│   ├── styles.css        # Dark black/white/ash UI styling
│   └── main.js           # Client JS: consent handling & metadata collection
│
└── templates/
    ├── index.html        # Landing/login page (uses JS)
    └── admin.html        # Admin UI (login + attempts table + export)

How data flows (high-level)

User opens GET / → templates/index.html served. JS shows consent box.

User clicks I understand — continue → JS collects metadata (screen size, timezone) and reveals the login form.

User submits form (POST /login) → server-side route routes/honeypot.login receives:

username, password, screen, timezone, plus HTTP User-Agent and request.remote_addr (IP).

Backend routes/honeypot:

Checks dictionary.txt to set weak flag (True if password string equals any word in dictionary).

Calls models.db.record_attempt(...) to store:

timestamp (UTC), username (as typed), SHA‑256(password) (one-way), weak integer (0/1), ip, user_agent, screen, timezone.

Checks users.txt to decide if this username is a demo-success user. Returns index.html with submitted and success context to show success/fail message to the user. (User still has no real access.)

Admin visits /admin:

GET shows admin login if not authenticated.

POST verifies the admin password using werkzeug.security.check_password_hash.

If authenticated, routes/auth calls models.db.fetch_attempts() and renders templates/admin.html with attempts.

Admin can click Export → /admin/export builds a textual report from DB rows and returns it as a downloadable .txt.

Why certain design choices

No plaintext password storage: only SHA‑256 hashes for recorded attempts. Admin password uses werkzeug salted hash (PBKDF2) which is better suited for authentication than raw SHA‑256.

Local-only defaults & consent banner: prevents accidental misuse — user must confirm permission to test.

users.txt allows demo behavior: shows a "successful login" to certain usernames to simulate real UX.

dictionary.txt flags weak passwords to illustrate password hygiene in logs.

SQLite simple and portable for local labs; DB auto-created on first run.

Setup & run (copy/paste)

clone/copy this folder and cd safe-honeypot/.

create & activate venv (recommended):

python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1


install dependencies:

pip install -r requirements.txt


(recommended) set admin password interactively:

python set_admin.py


This securely stores a hashed admin password in the DB. If you skip, default admin hash is created from config.ADMIN_PASSWORD_DEFAULT on first DB init (but using set_admin.py is safer).

run the app (local only):

python app.py


open browser at http://127.0.0.1:5000:

Accept consent, test logins.

Visit /admin to log in as the admin user and view/export logs.

File / module relationships (how code pieces talk)

app.py — orchestrator: imports blueprints and ensure_db() (from models/db.py) then registers routes.honeypot and routes.auth. This is the single entrypoint.

models/db.py — direct DB layer. Provides functions:

ensure_db() (creates DB & admin hash on first run)

record_attempt() (insert attempt row)

fetch_attempts() (read attempts for admin)

get_admin_hash() / set_admin_hash() / verify_admin_password() (admin hash helpers)

routes/honeypot.py — UI routes for users:

renders index.html, reads dictionary.txt & users.txt at module import to simple in-memory sets, handles /login POST and calls models.db.record_attempt.

routes/auth.py — admin routes:

uses models.db.get_admin_hash() (or verify_admin_password) to authenticate.

calls fetch_attempts() to assemble data for admin.html, and /admin/export to build the report.

templates/*.html — server-side templates rendered with Jinja for both user and admin views.

static/main.js — small client logic: shows consent, fills hidden form fields (screen, timezone) before POST.

static/styles.css — centralized styling used by templates.

Data storage (schema & where to look)

SQLite DB: honeypot.db (auto-created).

attempts table columns:

id, time (UTC ISO), username, password_hash (SHA‑256 hex), weak_integer (0/1), ip, user_agent, screen, timezone.

You can inspect DB manually with sqlite3 honeypot.db or use the admin UI /admin to view/export.

Admin: change password / reset

Use python set_admin.py to set or change the admin password (stores a secure hash in DB).

To reset everything (only for dev): delete honeypot.db and restart — DB will be recreated (admin hash will reset to default unless you run set_admin.py first).

Security & legal reminders (must read)

This tool is for authorized testing, education, or research only.

Do not use it to collect actual credentials from unaware users. Doing so is unethical and likely illegal.

Keep this local or inside a closed lab network. If you plan experiments involving real users, get explicit written consent and follow applicable laws and policies.

For production or real pentesting, use hardened storage (no plaintext), stronger password hashing for attempts if needed, HTTPS, proper logging and retention policies, and legal approvals.

Extending & next steps (ideas)

Add rate-limiting / alerting when many attempts occur in short time (useful to simulate brute-force detection).

Add visualization in admin panel (charts for IPs, weak-password counts).

Replace SHA‑256 attempt hashing with a keyed HMAC if you want to confirm same-password detection without allowing brute-force offline attacks.

Add CSRF protection for forms (Flask-WTF). For local test apps CSRF is low-priority but important for production.

Add option to operate fully offline (remove IP-related external calls if any).

Troubleshooting

sqlite3.OperationalError: no such table — delete honeypot.db and restart; DB will be created.

If admin login fails after set_admin.py, double-check you typed the same password when running the helper. You can re-run set_admin.py to set a new admin password.

License & attribution

Use freely for learning. If you share, note that the project is educational and must not be used to capture people’s credentials without consen