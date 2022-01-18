import random
import pdb
import pytest
import logging as logger

from myapitest.src.dao.products_dao import ProductsDAO
from myapitest.src.helper.products_helper import ProductHelper

pytestmark = [pytest.mark.products]


@pytest.fixture(scope='module')
def setup():
    product_dao = ProductsDAO()
    product_helper = ProductHelper()

    rand_prod = product_dao.get_random_product_from_db(1)
    product_id = rand_prod[0]['ID']

    info = {'product_id': product_id, 'product': rand_prod[0], 'prod_helper': product_helper}
    return info

@pytest.mark.tcid61
def test_update_price(setup):

    # get a product from db
    product = setup['product']
    product_ID = setup['product_id']

    #get product from API
    product_helper = setup['prod_helper']
    rs_api = product_helper.get_product_by_id(product_ID=product_ID)
    old_price = float(rs_api['regular_price'])

    new_price = str(random.randint(1, 2*round(old_price)))

    logger.debug(f"Regular price of product before change: {old_price}. New price will be {new_price}.")

    payload = {'regular_price': new_price}

    updated_product = product_helper.call_update_product(product_ID=product_ID, payload=payload)

    assert updated_product['regular_price'] == new_price, "Updated price do not match with requested price." \
                                                          f"Requested: {new_price}, actual: {updated_product['regular_price']}"

@pytest.mark.tcid63
@pytest.mark.tcid64
@pytest.mark.tcid65
def test_verify_sale_price(setup):

    product = setup['product']
    product_ID = setup['product_id']
    product_helper = setup['prod_helper']
    rs_api = product_helper.get_product_by_id(product_ID=product_ID)
    sale_price = str(round(float(rs_api['regular_price'])*0.8,2))
    currently_on_sale = rs_api['on_sale']

    logger.debug(f"Product 'on sale' status is {currently_on_sale}. Product sale price is: {sale_price}")

    if currently_on_sale:
        sale_price = rs_api['sale_price']

        set_sale_price(product_helper, product_ID)

        set_sale_price(product_helper,product_ID, sale_price)

    else:
        set_sale_price(product_helper,product_ID, sale_price)

        set_sale_price(product_helper,product_ID)

    #pdb.set_trace()

def set_sale_price(product_helper, product_ID, sale_price= None):

    if sale_price == None:
        #brak kwoty oznacza wyłączenie wyprzedaży
        #aktualnie produkt jest na wyprzedaży
        requested_sale = False
        sale_price = ''
    else:
        requested_sale = True

    payload = {'sale_price': sale_price}

    prod_check = product_helper.call_update_product(product_ID=product_ID, payload=payload)


    assert prod_check['sale_price'] == sale_price, "Sale price is not set as expected." \
                                                   f"Expected sale price: {sale_price}, actual: {prod_check['sale_price'] }"
    assert prod_check['on_sale'] == requested_sale, "Product did not changed 'on sale' status."

