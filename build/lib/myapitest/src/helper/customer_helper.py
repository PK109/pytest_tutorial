from myapitest.src.utilities.genericUtilities import generate_random_email_and_password

class CustomerHelper(object):

    def __init__(self):
        pass

    def create_customer(self, email= None, password= None, **kwargs):

        if not email:
            email = generate_random_email_and_password()['email']
        if not password:
            password = 'Password1'

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        return True

