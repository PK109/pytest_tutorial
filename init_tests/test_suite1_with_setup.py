import pytest

pytestmark =pytest.mark.fe

@pytest.fixture(scope='module')
def my_setup():
    print("")
    print(">>>>> MYSETUP <<<<<")

    return {'id':20, 'name':"Admin"}

@pytest.mark.smoke
def test_login_page_valid_user(my_setup):
    print("Login with valid user")
    print("Function aaaa")
    print("Name: {}".format(my_setup.get('name')))

@pytest.mark.regression
def test_login_with_wrong_pass(my_setup):
    print("Login with wrong password")
    print("Function bbbbbbbbb")
    assert 1==2