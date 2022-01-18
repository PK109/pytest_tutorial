from myapitest.src.utilities.genericUtilities import generate_random_email_and_password
from myapitest.src.utilities.requestsUtilities import RequestsUtility

class CustomerHelper(object):

    def __init__(self):
        self.request_utility = RequestsUtility()

    def create_customer(self, email= None, password= None, **kwargs):

        if not email:
            email = generate_random_email_and_password()['email']
        if not password:
            password = 'Password1'

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        create_user_json = self.request_utility.post('customers', payload=payload, expected_status_code=201)
        return create_user_json

