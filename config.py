import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "honeypot.db")
SECRET_KEY = "change_this_secret_for_local_testing"   # change for your local testing
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_DEFAULT = "admin"  # default; stored as hash on first run
