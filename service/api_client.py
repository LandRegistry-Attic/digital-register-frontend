import requests  # type: ignore
from flask import redirect  # type: ignore

from service import app

REGISTER_TITLE_API_URL = app.config['REGISTER_TITLE_API']
LAND_REGISTRY_PAYMENT_INTERFACE_URI = app.config['LAND_REGISTRY_PAYMENT_INTERFACE_URI']


def get_title(title_number):
    response = requests.get('{}titles/{}'.format(REGISTER_TITLE_API_URL, title_number))

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
        '{}title_search_postcode/{}'.format(REGISTER_TITLE_API_URL, postcode),
        params={'page': page_number}
    )

    return _to_json(response)


# TODO: check response status
def get_titles_by_address(address, page_number):
    response = requests.get(
        '{}title_search_address/{}'.format(REGISTER_TITLE_API_URL, address),
        params={'page': page_number}
    )

    return _to_json(response)


def check_health():
    return requests.get('{0}health'.format(REGISTER_TITLE_API_URL))


def get_official_copy_data(title_number):
    response = requests.get(
        '{}titles/{}/official-copy'.format(REGISTER_TITLE_API_URL, title_number)
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


def send_to_payment_service_provider(payment_parameters):
    response = requests.post('{}/wp'.format(LAND_REGISTRY_PAYMENT_INTERFACE_URI), data=payment_parameters)
    print('in api_client')
    print(response)
    return response


def _to_json(response):
    try:
        return response.json()
    except Exception as e:
        raise Exception('API response body is not JSON', e)
