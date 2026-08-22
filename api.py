from app import get_user


def handle_user(user_id):
    # Unchanged caller for impact analysis: lives on main while PRs edit app.py
    return get_user(user_id)
