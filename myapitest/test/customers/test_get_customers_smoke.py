
import pytest
import logging as logger

from myapitest.src.utilities.requestsUtilities import RequestsUtility

@pytest.mark.customers
@pytest.mark.tcid30
def test_get_all_customers():

    req_helper = RequestsUtility()
    rs_api = req_helper.get('customers')
    #logger.debug(f"Response of list all: {rs_api}")

    assert rs_api, f"Response of list all customers is empty"