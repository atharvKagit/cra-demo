def clean_user_id(user_id: str) -> str:
    """Very weak sanitizer — strips spaces only (demo)."""
    return str(user_id).replace(" ", "")
