## A local, consent-gated honeypot for educational / authorized testing 
## built with Flask + SQLite + vanilla JS/CSS.
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

