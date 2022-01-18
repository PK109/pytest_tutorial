import pytest

pytestmark =pytest.mark.fe

@pytest.mark.smoke
def test_login_page_valid_user():
    print("Login with valid user")
    print("Function aaaa")

@pytest.mark.regression
def test_login_with_wrong_pass():
    print("Login with wrong password")
    print("Function bbbbbbbbb")
    #assert 1==2