from datetime import datetime

from src.back.to_front.auth import sign_up, delete_user
from src.session import Me

_TEST_PASSWORD = "TestPassword123"


def test_sign_up_success():
    login = f"test_{datetime.now().strftime('%H%M%S%f')}"
    res = sign_up(login, _TEST_PASSWORD)
    assert res.status_code == 200
    assert Me.is_authenticated()
    delete_user()


def test_sign_up_duplicate(auth_user):
    res = sign_up(auth_user["login"], _TEST_PASSWORD)
    assert res.status_code == 400
