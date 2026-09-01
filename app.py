from db import query_params
from helpers import clean_user_id


def get_user(user_id):
    """Restore export for api.py/tests; parameterized SQL for gate pass."""
    safe_id = clean_user_id(user_id)
    return query_params("SELECT * FROM users WHERE id = %s", (safe_id,))


def lookup_user(user_id):
    """Backward-compatible alias after Phase E rename."""
    return get_user(user_id)


def get_user_by_email(email):
    cleaned = clean_user_id(email)
    return query_params("SELECT * FROM users WHERE email = %s", (cleaned,))
