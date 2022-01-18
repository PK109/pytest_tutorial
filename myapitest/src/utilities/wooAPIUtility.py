import os
from woocommerce import API
import logging as logger

from myapitest.src.configs.hosts_config import WOO_API_HOSTS
from myapitest.src.utilities.credentialsUtility import CredentialsUtility

class WooAPIUtility(object):

    def __init__(self):

        self.wc_creds = CredentialsUtility.get_wc_api_keys()

        self.env = os.environ.get('ENV', 'test')
        self.baseurl = WOO_API_HOSTS[self.env]

        self.wcapi = API(
            url=self.baseurl,
            consumer_key=self.wc_creds['wc_key'],
            consumer_secret=self.wc_creds['wc_secret'],
            version="wc/v3"
        )

    def assert_status_code(self):
        assert self.status_code == self.expected_status_code, \
            f"Bad status code. Expected: {self.expected_status_code}, actual: {self.status_code}"

    def post(self, wc_endpoint, params=None, expected_status_code = 200):

        rs_api = self.wcapi.post(wc_endpoint, data=params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API GET response: {self.rs_json}")

        return self.rs_json

    def get(self, wc_endpoint, params= None, expected_status_code = 200):

        rs_api= self.wcapi.get(wc_endpoint, params= params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API GET response: {self.rs_json}")

        return self.rs_json

    def put(self, wc_endpoint, params = None, expected_status_code = 200):

        rs_api= self.wcapi.put(wc_endpoint, data= params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API PUT response: {self.rs_json}")

        return self.rs_json

    def delete(self, wc_endpoint, params=None, expected_status_code=200):

        if params is None:
            params = {}
        rs_api = self.wcapi.delete(wc_endpoint, **params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API DELETE response: {self.rs_json}")

        return self.rs_json


if __name__ == '__main__':

    os.environ['ENV'] = 'test'
    os.environ['WC_KEY'] = 'ck_5d2f5160fbb19ed4b9340634e674cf2708c4ca6e'
    os.environ['WC_SECRET'] = 'cs_2c8b6923da761364504ddebe03fd8259e56267a4'
    os.environ['DB_USER'] = 'root'
    os.environ['DB_PASSWORD'] = 'root'

    obj = WooAPIUtility()
    rs_api = obj.get('products')
    print(rs_api)
    import pdb; pdb.set_trace()
