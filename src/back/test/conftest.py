import pytest
from datetime import datetime

from src.back.db.auth import Auth
from src.back.to_front.auth import sign_up, sign_out
from src.session import Me

_TEST_PASSWORD = "TestPassword123"


@pytest.fixture
def auth_user():
    login = f"test_{datetime.now().strftime('%H%M%S%f')}"
    res = sign_up(login, _TEST_PASSWORD)
    assert res.status_code == 200, f"Setup failed: {res.message}"
    user_id = Me.user.id
    yield {"id": user_id, "login": login, "password": _TEST_PASSWORD}
    sign_out()
    Auth._delete_user(user_id)
