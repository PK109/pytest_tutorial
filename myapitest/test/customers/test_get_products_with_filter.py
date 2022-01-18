import pytest
from datetime import  datetime, timedelta
from myapitest.src.helper.products_helper import ProductHelper
from myapitest.src.dao.products_dao import ProductsDAO

@pytest.mark.regression
class  TestListProductsWithFilter(object):

    #no __init__ method !!

    @pytest.mark.tcid51
    def test_list_products_with_filter_after(self):

        #create data
        x_days_from_today = 300
        unformatted_date = datetime.now() - timedelta(days=x_days_from_today)
        payload = dict()
        payload['after'] = unformatted_date.replace(microsecond=0).isoformat()
        payload['per_page'] = 10
        #payload['after_second_format'] = unformatted_date.strftime('%Y-%m-%dT%H:%M:%S')
        #import pdb; pdb.set_trace()

        #make the call
        rs_api = ProductHelper().call_list_all_products(payload=payload)
        assert rs_api, "Empty response for list products"

        #get data from db
        db_products = ProductsDAO().get_products_after_date(payload['after'])

        #verify response
        assert len(rs_api) == len(db_products), f"Filtered list differs between DB and API. DB count: {len(db_products)}, API count: {len(rs_api)}"

        ids_in_api = [i['id'] for i in rs_api]
        ids_in_db = [i['ID'] for i in db_products]

        ids_diff = list(set(ids_in_api) - set(ids_in_db))
        assert not ids_diff, f"Mismatch of products filtered. {len(ids_diff)} products not found in both sides."
