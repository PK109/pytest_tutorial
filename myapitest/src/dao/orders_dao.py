
from myapitest.src.utilities.dbUtility import DBUtility

class OrdersDAO (object):

    def __init__(self):
        self.db_helper = DBUtility()

    def get_order_lines_by_order_id(self, order_id):
        sql = f"SELECT * FROM local.wp_woocommerce_order_items where order_id = {order_id};"
        return self.db_helper.execute_select(sql)

    def get_order_item_details(self, item_id):
        sql = f"SELECT * FROM local.wp_woocommerce_order_itemmeta where order_item_id ={item_id};"
        rs_sql = self.db_helper.execute_select(sql)
        line_details = dict()
        for meta in rs_sql:
            line_details[meta['meta_key']]= meta['meta_value']
        #import pdb; pdb.set_trace()
        return line_details
