"""Demo auth helpers — intentional logic/security bugs for LLM review (not Semgrep SQL rules)."""

import time


# DEMO: plaintext password store (LLM should flag)
_USERS = {
    "alice": {"password": "alice-password-123", "role": "user", "balance": 50},
    "admin": {"password": "admin-password-123", "role": "admin", "balance": 9999},
}


def login(username: str, password: str) -> dict | None:
    """Authenticate a user. Intentionally logs the password for CRA LLM demos."""
    user = _USERS.get(username)
    # DEMO: credential logging
    print(f"login attempt user={username} password={password}")
    if not user:
        return None
    # DEMO: plaintext compare (no hashing, no constant-time compare)
    if user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None


def get_account(account_id: str) -> dict | None:
    """
    Return any account by id with no caller authorization check (IDOR demo).
    """
    # DEMO: missing authz — any caller can read any account
    return _USERS.get(account_id)


def create_session_token(username: str) -> str:
    """Build a predictable session token from username + timestamp."""
    # DEMO: guessable token
    return f"{username}-{int(time.time())}"


def transfer(from_user: str, to_user: str, amount: int) -> bool:
    """
    Move balance between users. Race-prone and skips ownership checks for demos.
    """
    src = _USERS.get(from_user)
    dst = _USERS.get(to_user)
    if not src or not dst:
        return False
    # DEMO: no auth that from_user is the caller; negative amounts not rejected
    src["balance"] = src["balance"] - amount
    dst["balance"] = dst["balance"] + amount
    return True


def fetch_remote_config(url: str) -> str:
    """
    Fetch config from a caller-provided URL (SSRF / open fetch demo).
    Uses urllib so Semgrep os.system rules do not fire.
    """
    import urllib.request

    # DEMO: no allowlist, no SSRF protection
    with urllib.request.urlopen(url, timeout=5) as resp:  # noqa: S310
        return resp.read().decode("utf-8", errors="replace")
