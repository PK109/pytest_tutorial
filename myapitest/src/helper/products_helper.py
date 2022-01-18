from myapitest.src.utilities.genericUtilities import generate_random_email_and_password
from myapitest.src.utilities.requestsUtilities import RequestsUtility
import logging as logger

class ProductHelper(object):

    def __init__(self):
        self.request_utility = RequestsUtility()

    def get_product_by_id(self, product_ID):
        return self.request_utility.get(f'products/{product_ID}')

    def call_create_product(self, payload):

        return self.request_utility.post('products', payload=payload, expected_status_code=201)

    def call_update_product(self, payload , product_ID):

        return self.request_utility.put(f'products/{product_ID}', payload=payload)

    def call_list_all_products(self, payload=None):

        max_pages = 1000
        all_products = []
        for i in range(1,max_pages + 1):
            logger.debug(f"List products page no: {i}. ")

            if not 'per_page' in payload.keys():
                payload['per_page'] = 100

            payload['page'] = i

            rs_api = self.request_utility.get('products', payload=payload)

            all_products.extend(rs_api)
            if len(rs_api) != payload['per_page']:
                break

        else:
             raise Exception(f"Unable to find all products after {max_pages} pages.")

        return all_products