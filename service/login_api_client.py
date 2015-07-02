import json
import requests
from service import app


LOGIN_API_URL = app.config['LOGIN_API']
AUTHENTICATE_ENDPOINT_URL = '{}user/authenticate'.format(LOGIN_API_URL)


def authenticate_user(username, password):
    user_dict = {'user_id': username, 'password': password}
    request_dict = {"credentials": user_dict}
    request_json = json.dumps(request_dict)

    headers = {'content-type': 'application/json'}
    response = requests.post(AUTHENTICATE_ENDPOINT_URL, data=request_json, headers=headers)

    if response.status_code == 200:
        return True
    elif _is_invalid_credentials_response(response):
        return False
    else:
        msg_format = ("An error occurred when trying to authenticate user '{}'. "
                      "Login API response: (HTTP status: {}) '{}'")
        raise Exception(msg_format.format(username, response.status_code, response.text))


def check_health():
    return requests.get('{0}health'.format(LOGIN_API_URL))


def _is_invalid_credentials_response(response):
    if response.status_code != 401:
        return False

    response_json = response.json()
    return response_json and response_json['error'] == 'Invalid credentials'
