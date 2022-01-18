import pdb
import random

import pytest
from myapitest.src.utilities.wooAPIUtility import WooAPIUtility
from myapitest.src.utilities.genericUtilities import generate_random_string

from myapitest.src.helper.orders_helper import OrderHelper
from myapitest.src.helper.coupon_helper import CouponHelper
from myapitest.src.helper.products_helper import ProductHelper
from myapitest.src.dao.products_dao import ProductsDAO

pytestmark = [pytest.mark.orders, pytest.mark.regression]


@pytest.mark.parametrize("new_status",
                         [
                             pytest.param('cancelled', marks=[pytest.mark.tcid55, pytest.mark.smoke]),
                             pytest.param('completed', marks=pytest.mark.tcid56),
                             pytest.param('on-hold', marks=pytest.mark.tcid57)
                         ])
def test_update_order_status(new_status):
    # create new order
    order_helper = OrderHelper()
    order_json = order_helper.create_order()

    # get the current status of order
    curr_status = order_json['status']
    order_id = order_json['id']
    assert curr_status != new_status, f"Current status of the order is already '{new_status}'"

    # update the status
    payload = {'status': new_status}
    rs_update = order_helper.call_update_an_order(order_id, payload)

    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)

    # verify the new order that was updated
    assert new_order_info['status'] == new_status, f"Updated order status to {new_status}, but order still have" \
                                                   f"status: {new_order_info['status']}."


@pytest.mark.tcid58
def test_update_status_to_random_string():
    new_status = generate_random_string()

    # create new order
    order_helper = OrderHelper()
    order_json = order_helper.create_order()

    # get the current status of order
    curr_status = order_json['status']
    order_id = order_json['id']

    # update the status
    payload = {'status': new_status}
    # expected status code is 400
    # rs_update =order_helper.call_update_an_order(order_id, payload)
    rs_update = WooAPIUtility().put(f"orders/{order_id}", params=payload, expected_status_code=400)
    assert rs_update['code'] == 'rest_invalid_param', f"Wrong response from API. Expected - 'rest_invalid_param'\n" \
                                                      f"Actual: {rs_update['code']}"


@pytest.mark.tcid59
def test_update_order_customer_note():
    new_note = generate_random_string(length=40)
    # create new order
    order_helper = OrderHelper()
    order_json = order_helper.create_order()

    # get the current status of order
    note = order_json['customer_note']
    order_id = order_json['id']
    assert note == '', f"Current note from customer is not empty. Actual '{note}'"

    # update the status
    payload = {'customer_note': new_note}
    order_helper.call_update_an_order(order_id, payload)  # do not need to retrieve a response from here
    pdb.set_trace()
    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)

    # verify the new order that was updated
    assert new_order_info['customer_note'] == new_note, f"Updated order 'customer_note' to {new_note}, but order " \
                                                        f"still have status: {new_order_info['customer_note']}."


@pytest.mark.tcid60
def test_coupon_discount_applied():
    # create new order
    order_helper = OrderHelper()
    product_helper = ProductHelper()
    coupon_helper = CouponHelper()
    product_dao = ProductsDAO()

    coupons_json = coupon_helper.call_list_all_coupons()
    coupon = random.choice(coupons_json)
    product = product_dao.get_random_product_from_db(1)[0]
    price = product_helper.get_product_by_id(product['ID'])

    add_args = {'line_items': [
        {
            "product_id": product['ID'],
            "quantity": 1
        }
    ], 'coupon_lines': [
        {
            'code': coupon['code']
        }
    ]}
    rs_api = order_helper.create_order(add_args)

    assert rs_api, "Order is not created."
    assert rs_api['coupon_lines'][0]['code'] == coupon['code'], f"Wrong coupon used. Expected: '{coupon['code']}', " \
                                                                f"actual: '{rs_api['coupon_lines'][0]['code']}'"
    total_price = float(rs_api['line_items'][0]['total'])
    subtotal_price = float(rs_api['line_items'][0]['subtotal'])
    discount = float(coupon['amount'])

    # pdb.set_trace()
    assert abs(total_price - round(subtotal_price * (100 - discount) / 100,
                                   2)) <= 0.01, f"Order reduce do not match with coupon used. " \
                                                f"Subtotal : {subtotal_price}, Discount rate: {discount}, " \
                                                f"Expected price: {round(subtotal_price * (100 - discount) / 100, 2)}, " \
                                                f"Actual price: {total_price}."

@pytest.mark.parametrize("coupon_type",
                         [
                             pytest.param('percent', marks=[pytest.mark.tcid37, pytest.mark.smoke]),
                             pytest.param('fixed_cart', marks=pytest.mark.tcid38),
                             pytest.param('fixed_product', marks=pytest.mark.tcid39)
                         ])
def test_create_coupon_of_selected_type(coupon_type):

    coupon_helper = CouponHelper()

    coupon_id = coupon_helper.call_create_coupon(discount_type= coupon_type)['id']

    coupon = coupon_helper.call_get_coupon_by_id(coupon_id)

    assert coupon_type == coupon['discount_type'], f"Wrong coupon discount type. Expected type: '{coupon_type}', " \
                                                   f"actual '{coupon['discount_type']}'"

@pytest.mark.tcid40
def test_create_invalid_coupon_type():

    discount_rate = str(random.randint(1, 50))
    coupon_code = generate_random_string()
    discount_type = generate_random_string()

    payload = {
        'code': coupon_code,
        'amount': discount_rate,
        'discount_type': discount_type
    }

    rs_api = WooAPIUtility().post("coupons", params=payload, expected_status_code=400)

    assert rs_api['code'] == 'rest_invalid_param', f"Wrong error code. Expected: 'rest_invalid_param', actual: {rs_api['code']}"
