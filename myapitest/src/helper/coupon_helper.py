import random

from myapitest.src.utilities.genericUtilities import generate_random_string
from myapitest.src.utilities.wooAPIUtility import WooAPIUtility

class CouponHelper(object):

    def __init__(self):
        self.woo_helper = WooAPIUtility()

    def call_list_all_coupons(self):
        return self.woo_helper.get("coupons")


    def call_create_coupon(self, discount_type= 'percent', discount_rate=None):

        if discount_rate is None:
            discount_rate = str(random.randint(1, 50))
        coupon_code = generate_random_string()

        payload = {
            'code': coupon_code,
            'amount': discount_rate,
            'discount_type': discount_type
        }

        return self.woo_helper.post("coupons", params=payload, expected_status_code=201)

    def call_get_coupon_by_id(self, coupon_id):
        return self.woo_helper.get(f"coupons/{coupon_id}")