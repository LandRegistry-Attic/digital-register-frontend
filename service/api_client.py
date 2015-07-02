import requests
from service import app

REGISTER_TITLE_API_URL = app.config['REGISTER_TITLE_API']


def get_title(title_number):
    response = requests.get('{}titles/{}'.format(REGISTER_TITLE_API_URL, title_number))

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        error_msg = 'API returned an unexpected response ({0}) when called for a title'.format(
            response.status_code
        )

        raise Exception(error_msg)


# TODO: check response status
def get_titles_by_postcode(postcode, page_num):
    response = requests.get(
        '{}title_search_postcode/{}'.format(REGISTER_TITLE_API_URL, postcode),
        params={'page': page_num}
    )

    return response.json()


# TODO: check response status
def get_titles_by_address(address, page_num):
    response = requests.get(
        '{}title_search_address/{}'.format(REGISTER_TITLE_API_URL, address),
        params={'page': page_num}
    )

    return response.json()


def check_health():
    return requests.get('{0}health'.format(REGISTER_TITLE_API_URL))
