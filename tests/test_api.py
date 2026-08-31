from api import handle_user


def test_handle_user_delegates_to_app():
    result = handle_user("99")
    assert result == [{"ok": True}]
