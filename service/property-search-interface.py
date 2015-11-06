import requests
import json
from service import app

NULL=None       # Temporary!

def insert(title_number,
           fee_amt_quoted,
           property_search_purch_addr,
           title_plan_required_indicator='Y',
           reg_view_required_indicator='Y',
           tenure_code='F',
           price_paid_indicator='Y',
           flood_risk_report_required_indicator='N'
           ):

    """
    Insert the request details on T_PS_SRCH_REQ, return a timestamp.

    :param title_number: str
    :param fee_amt_quoted: float
    :param property_search_purch_addr: str
    :param title_plan_required_indicator: str ('bool' char)
    :param reg_view_required_indicator: str ('bool' char)
    :param tenure_code: str ('bool' char)
    :param price_paid_indicator: str ('bool' char)
    :param flood_risk_report_required_indicator: str ('bool' char)

    :return: timestamp of form 2015-11-05 10:42:42.482662

    An exception may be raised.
    """

    # Get params as dict: note that locals() should be called before any other variables are set!
    params = locals()

    property_search_interface_url = app.config['property_search_interface_url'].rstrip('/')
    url = property_search_interface_url + "/insert-to-search-request-table"

    # HTTP POST, json format.
    r = requests.post(url, json=params)
    r.raise_for_status()    # Raises error, if there is one.

    return json.loads(r.text)['data']


def update(user_id,
           row_insert_timestamp,
           lro_transaction_reference,
           property_search_rejection_timestamp=NULL,
           property_search_rejection_reference=NULL
           ):
    """
    Update a row of T_PS_SRCH_REQ.

    :param user_id: str
    :param row_insert_timestamp: str, of form 2015-11-05 10:42:42.482662
    :param lro_transaction_reference: str
    :param property_search_rejection_timestamp: str, of form 2015-11-05 10:42:42.482662
    :param property_search_rejection_reference: str

    :return: None

    An exception may be raised.
    """


    # Get params as dict: note that locals() should be called before any other variables are set!
    params = locals()

    property_search_interface_url = app.config['property_search_interface_url'].rstrip('/')
    url = property_search_interface_url + "/update-search-request-table"

    # HTTP POST, json format. Should be a PUT perhaps.
    r = requests.post(url, json=params)
    r.raise_for_status()    # Raises error, if there is one.

    return None
