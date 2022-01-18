import pytest

from myapitest.src.dao.products_dao import ProductsDAO
from myapitest.src.dao.orders_dao import OrdersDAO
from myapitest.src.helper.orders_helper import OrderHelper
from myapitest.src.helper.customer_helper import CustomerHelper

@pytest.fixture(scope='module')
def my_orders_smoke_setup():
    product_dao = ProductsDAO()
    order_helper = OrderHelper()

    rand_prod = product_dao.get_random_product_from_db(1)
    product_id = rand_prod[0]['ID']

    info = {'product_id': product_id, 'order_helper': order_helper}
    return info

@pytest.mark.smoke
@pytest.mark.orders
@pytest.mark.tcid48
def test_create_paid_order_by_guest(my_orders_smoke_setup):

    order_helper = my_orders_smoke_setup['order_helper']
    # get products from db
    customer_id = 0

    # make the call
    info = {"line_items":
        [
            {
                "product_id": my_orders_smoke_setup['product_id'],
                "quantity": 1
            }
        ]
    }
    order_json = order_helper.create_order(additional_args=info)

    expected_prod= [{'product_id': my_orders_smoke_setup['product_id']}]
    order_helper.verify_order_is_created(order_json= order_json, expected_cust_id=customer_id, expected_products=expected_prod)

@pytest.mark.smoke
@pytest.mark.orders
@pytest.mark.tcid49
def test_create_paid_order_new_created_customer(my_orders_smoke_setup):

    #create helpers
    order_helper = my_orders_smoke_setup['order_helper']
    customer_helper = CustomerHelper()
    # get products from db
    product_id = my_orders_smoke_setup['product_id']

    # make the call
    customer_info = customer_helper.create_customer()

    info = {"line_items":
        [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ],
        "customer_id": customer_info['id']
    }
    order_json = order_helper.create_order(additional_args=info)

    expected_prod= [{'product_id': product_id}]
    order_helper.verify_order_is_created(order_json= order_json, expected_cust_id=customer_info['id'], expected_products=expected_prod)