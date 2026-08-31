from app import get_user


def test_get_user_builds_query():
    result = get_user("42")
    assert result == [{"ok": True}]
