import requests  # type: ignore
import pg8000
import config
from datetime import datetime                                                                          # type: ignore
from service import app

REGISTER_TITLE_API_URL = app.config['REGISTER_TITLE_API'].rstrip('/')
LAND_REGISTRY_PAYMENT_INTERFACE_URI = app.config['LAND_REGISTRY_PAYMENT_INTERFACE_URI']
LAND_REGISTRY_PAYMENT_INTERFACE_BASE_URI = app.config['LAND_REGISTRY_PAYMENT_INTERFACE_BASE_URI']


def get_title(title_number):
    response = requests.get('{}/titles/{}'.format(REGISTER_TITLE_API_URL, title_number))

    if response.status_code == 200:
        return _to_json(response)
    elif response.status_code == 404:
        return None
    else:
        error_msg = 'API returned an unexpected response ({0}) when called for a title'.format(
            response.status_code
        )

        raise Exception(error_msg)


# TODO: check response status
def get_titles_by_postcode(postcode, page_number):
    response = requests.get(
        '{}/title_search_postcode/{}'.format(REGISTER_TITLE_API_URL, postcode),
        params={'page': page_number}
    )

    return _to_json(response)


# TODO: check response status
def get_titles_by_address(address, page_number):
    response = requests.get(
        '{}/title_search_address/{}'.format(REGISTER_TITLE_API_URL, address),
        params={'page': page_number}
    )

    return _to_json(response)


def check_health():
    return requests.get('{0}/health'.format(REGISTER_TITLE_API_URL))


def get_official_copy_data(title_number):
    response = requests.get(
        '{}/titles/{}/official-copy'.format(REGISTER_TITLE_API_URL, title_number)
    )

    if response.status_code == 200:
        return _to_json(response)
    elif response.status_code == 404:
        return None
    else:
        error_msg_format = (
            'API returned an unexpected response ({0}) when called for official copy data'
        )

        raise Exception(error_msg_format.format(response.status_code))


# TODO: Invoke from server.py!
def send_to_payment_service_provider(payment_parameters):

    response = requests.post('{}/wp'.format(LAND_REGISTRY_PAYMENT_INTERFACE_URI), data=payment_parameters)
    response.raise_for_status()

    return response


def save_search_request(search_parameters):
    """
    Saves user's Search Request and returns the 'cart id.'
    """

    response = requests.post('{}/save_search_request'.format(REGISTER_TITLE_API_URL), data=search_parameters)
    response.raise_for_status()
    return response


def _to_json(response):
    try:
        return response.json()
    except Exception as e:
        raise Exception('API response body is not JSON', e)


def _get_time():
    # Postgres datetime format is YYYY-MM-DD MM:HH:SS.mm
    _now = datetime.now()
    return _now.strftime("%Y-%m-%d %H:%M:%S.%f")


def get_invoice_data(transaction_id):
    response = requests.get('{}/get-invoice-data?transId={}'.format(LAND_REGISTRY_PAYMENT_INTERFACE_BASE_URI, transaction_id))
    response.raise_for_status()

    return response
