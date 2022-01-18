import pytest
import pdb
import os
import logging as logger

from myapitest.src.utilities.genericUtilities import generate_random_email_and_password
from myapitest.src.helper.customer_helper import CustomerHelper
from myapitest.src.dao.customers_dao import CustomersDAO
from myapitest.src.utilities.requestsUtilities import RequestsUtility

os.environ['ENV'] = 'test'
os.environ['WC_KEY'] = 'ck_5d2f5160fbb19ed4b9340634e674cf2708c4ca6e'
os.environ['WC_SECRET'] = 'cs_2c8b6923da761364504ddebe03fd8259e56267a4'
os.environ['DB_USER'] = 'root'
os.environ['DB_PASSWORD'] = 'root'

@pytest.mark.customers
@pytest.mark.tcid29
def test_create_customer_only_email_password():

    logger.info("TEST: Create new customer with email and password only.")
    rand_info = generate_random_email_and_password()

    email=rand_info['email']
    password=rand_info['password']

    #create payload
    payload = rand_info

    #make the call
    cust_obj = CustomerHelper()
    cust_api_info = cust_obj.create_customer(email=email, password=password)

    #verify status code of the call - verified in utilities

    #verify email in the response
    assert cust_api_info['email'] == email, f"Create customer API return wrong email: {cust_api_info['email']}"
    assert cust_api_info['first_name'] == '', f"API have returned name: {cust_api_info['first_name']}. It should be empty."

    #verify customer is created in database
    cust_dao = CustomersDAO()
    cust_info = cust_dao.get_customer_by_email(email)

    id_in_api = cust_api_info['id']
    id_in_db = cust_info[0]['ID']

    assert id_in_db == id_in_api, f"Create customer response 'ID' not the same as ID in the database."

@pytest.mark.customers
@pytest.mark.tcid47
def test_create_customer_fail_for_existing_email():

    #get existing email from db
    cust_dao= CustomersDAO()
    existing_cust = cust_dao.get_random_customer_from_db()
    existing_mail = existing_cust[0]['user_email']

#make the call
    req_helper = RequestsUtility()
    payload = {"email":existing_mail,"password":"Passw1"}
    cust_api_info = req_helper.post(endpoint='customers', payload=payload, expected_status_code=400)

    assert cust_api_info['code'] == 'registration-error-email-exists',\
    f"Create customer with existing user. Error 'code' is not correct. Expected: registration-error-email-exists, Actual: {cust_api_info['code']}"