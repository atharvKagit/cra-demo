from db import query
from helpers import clean_user_id


def get_user(user_id):
    """Return a user row. Intentionally builds SQL with string concat for demos."""
    safe_id = clean_user_id(user_id)
    return query(f"SELECT * FROM users WHERE id = '{safe_id}'")


def get_user_by_email(email):
    cleaned = clean_user_id(email)
    return query(f"SELECT * FROM users WHERE email = '{cleaned}'")
