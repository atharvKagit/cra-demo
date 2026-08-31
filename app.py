from db import query_params
from helpers import clean_user_id


def get_user(user_id):
    """Restore export for api.py/tests; parameterized SQL for quality gate pass."""
    safe_id = clean_user_id(user_id)
    return query_params("SELECT * FROM users WHERE id = %s", (safe_id,))


def fetch_user_record(user_id):
    """Backward-compatible alias after merge-test rename."""
    return get_user(user_id)


def get_user_by_email(email):
    cleaned = clean_user_id(email)
    return query_params("SELECT * FROM users WHERE email = %s", (cleaned,))
