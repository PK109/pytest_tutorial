import pytest

pytestmark = pytest.mark.fe

class TestCheckout(object):

    def test_checkout_as_guest(self):
        print ("checkout as guest")
        print("Classs 1111111111")

    def test_checkout_with_existing_user(self):
        print("Checkout with existing user")
        print("Class: 2222222")