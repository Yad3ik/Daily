from datetime import datetime

from src.back.to_front.auth import sign_in, sign_out
from src.session import Me

_TEST_PASSWORD = "TestPassword123"


def test_sign_in_success(auth_user):
    sign_out()
    res = sign_in(auth_user["login"], auth_user["password"])
    assert res.status_code == 200
    assert Me.is_authenticated()


def test_sign_in_wrong_password(auth_user):
    sign_out()
    res = sign_in(auth_user["login"], "wrong_password")
    assert res.status_code == 400
    assert not Me.is_authenticated()


def test_sign_in_unknown_login():
    login = f"ghost_{datetime.now().strftime('%H%M%S%f')}"
    res = sign_in(login, _TEST_PASSWORD)
    assert res.status_code == 400
