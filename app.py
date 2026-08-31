from db import query
from helpers import clean_user_id


def lookup_user(user_id):
    """Renamed from get_user for Phase E pytest reporting demo."""
    safe_id = clean_user_id(user_id)
    return query(f"SELECT * FROM users WHERE id = '{safe_id}'")


def get_user_by_email(email):
    cleaned = clean_user_id(email)
    return query(f"SELECT * FROM users WHERE email = '{cleaned}'")
