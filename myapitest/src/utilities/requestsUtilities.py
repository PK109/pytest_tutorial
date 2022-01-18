import os
import requests
import logging as logger
import json
from  requests_oauthlib import OAuth1

from myapitest.src.configs.hosts_config import API_HOSTS
from myapitest.src.utilities.credentialsUtility import CredentialsUtility



class RequestsUtility(object):

    def __init__(self):

        self.wc_creds = CredentialsUtility.get_wc_api_keys()

        self.env = os.environ.get('ENV','debug')
        self.baseurl = API_HOSTS[self.env]
        self.auth = OAuth1(client_key=self.wc_creds['wc_key'], client_secret=self.wc_creds['wc_secret'])

    def assert_status_code(self):
        assert self.status_code == self.expected_status_code,\
        f"Bad status code. Expected: {self.expected_status_code}, actual: {self.status_code}"

    def post(self, endpoint, payload = None, headers = None, expected_status_code= 200):

        url = self.baseurl + endpoint
        if not headers:
            headers = {"Content-Type": "application/json"}

        rs_api = requests.post(url, data= json.dumps(payload), headers= headers,
                               auth=self.auth)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API response: {self.rs_json}")

        return rs_api.json()

    def get(self, endpoint, payload = None, headers = None, expected_status_code= 200):

        url = self.baseurl + endpoint

        if not headers:
            headers = {"Content-Type": "application/json"}

        rs_api = requests.get(url, data=json.dumps(payload), headers=headers,
                               auth=self.auth)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API GET response: {self.rs_json}")

        return self.rs_json

    def put(self, endpoint, payload=None, headers=None, expected_status_code=200):

        url = self.baseurl + endpoint
        if not headers:
            headers = {"Content-Type": "application/json"}

        rs_api = requests.put(url, data=json.dumps(payload), headers=headers,
                               auth=self.auth)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API response: {self.rs_json}")

        return rs_api.json()
