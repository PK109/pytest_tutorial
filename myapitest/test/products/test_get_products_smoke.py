
import pytest
import logging as logger

from myapitest.src.utilities.requestsUtilities import RequestsUtility
from myapitest.src.dao.products_dao import ProductsDAO
from myapitest.src.helper.products_helper import ProductHelper

pytestmark = [pytest.mark.products, pytest.mark.smoke]

@pytest.mark.tcid24
def test_get_all_products():

    req_helper = RequestsUtility()
    rs_api = req_helper.get('products')
    #logger.debug(f"Response of list all: {rs_api}")

    assert rs_api, f"Response of list all products is empty"

@pytest.mark.tcid25
def test_get_product_by_ID():

    #get a product from db
    product = ProductsDAO().get_random_product_from_db()
    product_ID = product[0]['ID']

    #make the call
    product_helper = ProductHelper()
    rs_api = product_helper.get_product_by_id(product_ID)
    #verify the response
    assert product[0]['post_title'] == rs_api['name'], f"Get product by ID returned wrong product." \
                                                       f"ID: {product_ID}, DB_name = {product[0]['post_title']}" \
                                                       f"API Name: {rs_api['name']}"