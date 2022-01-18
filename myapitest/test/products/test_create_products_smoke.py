import pytest

from myapitest.src.utilities.genericUtilities import generate_random_string
from myapitest.src.helper.products_helper import ProductHelper
from myapitest.src.dao.products_dao import ProductsDAO

pytestmark = [pytest.mark.products, pytest.mark.smoke]

@pytest.mark.tcid26
def test_create_simple_product():

    #generate some data
    payload = dict()
    payload['name'] = generate_random_string(length= 15)
    payload['type'] = "simple"
    payload['regular_price'] = "10.01"

    #make the call
    rs_api = ProductHelper().call_create_product(payload= payload)

    #verify the response
    assert rs_api, "API did not respond with the product details."
    assert rs_api['name'] == payload['name'], f"Product have wrong name. Expected: {payload['name']}, received: {rs_api['name']}"

    #verify the product exists in the db
    rs_dao = ProductsDAO().get_product_by_ID(rs_api['id'])

    assert rs_dao[0]['post_title'] == rs_api['name'], f"Product not created in the DB or product name is different."