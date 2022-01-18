import json
import os

from myapitest.src.dao.orders_dao import OrdersDAO
from myapitest.src.utilities.wooAPIUtility import WooAPIUtility

class OrderHelper(object):

    def __init__(self):
        self.curr_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.woo_helper = WooAPIUtility()

    def create_order(self, additional_args = None):

        payload_template = os.path.join(self.curr_file_dir, '..','data','create_order_payload.json')
            #myapitest/src/data/create_order_payload.json

        with open(payload_template) as f:
            payload: dict = json.load(f)

        if additional_args:
            assert isinstance(additional_args, dict), f"Parameter 'additional_args' must " \
                                                      f"be a dictionary but found as {type(additional_args)}"
            payload.update(additional_args)

        rs_api = self.woo_helper.post('orders',params=payload, expected_status_code=201)

        #import pdb ; pdb.set_trace()
        return  rs_api

    @staticmethod
    def verify_order_is_created(order_json, expected_cust_id, expected_products):

        orders_dao = OrdersDAO()

        # verify the response
        assert order_json, 'Create Order response is empty'
        assert order_json['customer_id'] == expected_cust_id, f"Customer_id is set to " \
                                                                 f"{order_json['customer_id']}, This is not an expected customer with id: {expected_cust_id}"
        assert len(order_json[
                       'line_items']) == len(expected_products), f"Expected {len(expected_products)} item in order, but {len(order_json['line_items'])} items found."

        # verify db
        order_db = orders_dao.get_order_lines_by_order_id(order_json['id'])
        assert order_db, f"Created order not found in the DB. Order id {order_json['id']}"
        items_db = [i for i in order_db if i['order_item_type'] == 'line_item']  # get products only, no shipping.

        assert len(items_db) == 1

        #get list of products ids in the response
        api_products_ids = [i['product_id'] for i in order_json['line_items']]

        for product in expected_products:
            assert product['product_id'] in api_products_ids, f"Create order does not have a product with id: {product['product_id']}."

    def call_update_an_order(self, order_id, payload):
        return self.woo_helper.put(f"orders/{order_id}", params= payload)

    def call_retrieve_an_order(self, order_id):
        return self.woo_helper.get(f"orders/{order_id}" )

