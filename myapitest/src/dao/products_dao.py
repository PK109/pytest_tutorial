import datetime

from myapitest.src.utilities.dbUtility import DBUtility
import random

class ProductsDAO(object):

    def __init__(self):
        self.db_helper = DBUtility()

    def get_random_product_from_db(self, qty = 1):

        sql = 'SELECT * FROM local.wp_posts WHERE post_type = "product" LIMIT 5000;'
        rs_sql = self.db_helper.execute_select(sql)

        return random.sample(rs_sql, int(qty))

    def get_product_by_ID(self, ID):

        sql = f'SELECT * FROM local.wp_posts WHERE ID ={ID};'

        return self.db_helper.execute_select(sql)

    def get_products_after_date(self, _date):

        sql =  f'SELECT * FROM local.wp_posts WHERE post_type = "product" AND post_date > "{_date}" ;'

        return self.db_helper.execute_select(sql)
