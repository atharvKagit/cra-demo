from db import query
from helpers import clean_user_id

# DEMO ONLY — intentional placeholder for CRA secrets scanner (not a real key)
OPENAI_API_KEY = "sk-demo-cra-phaseb-abcdefghijklmnopqrstuv"


def get_user(user_id):
    """Return a user row. Intentionally builds SQL with string concat for demos."""
    safe_id = clean_user_id(user_id)
    # DEMO: still unsafe for CRA scanners / LLM
    return query(f"SELECT * FROM users WHERE id = '{safe_id}' OR 1=1")


def get_user_by_email(email):
    cleaned = clean_user_id(email)
    return query(f"SELECT * FROM users WHERE email = '{cleaned}'")


def delete_user(user_id):
    """Extra unsafe query for inline PR comment demos."""
    return query(f"DELETE FROM users WHERE id = '{user_id}'")
