import os
from datetime import timedelta
from typing import Dict, Union

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = False

fault_log_file_path = os.getenv('FAULT_LOG_FILE_PATH', 'fault.log')
google_analytics_api_key = os.getenv('GOOGLE_ANALYTICS_API_KEY', '')
logging_config_file_path = os.getenv('LOGGING_CONFIG_FILE_PATH', os.path.join(ROOT_DIR, 'logging_config.json'))
login_api = os.getenv('LOGIN_API', '')
register_title_api = os.getenv('REGISTER_TITLE_API', '')
secret_key = os.getenv('APPLICATION_SECRET_KEY', 'secretkeyshouldberandom')
service_notice_html = os.getenv('SERVICE_NOTICE_HTML', '<h2>Downtime notice</h2><p>This service will be offline between 2.00&ndash;5.00 on 31st July</p>')
session_cookie_secure = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() != 'false'
more_proprietor_details = os.getenv('MORE_PROPRIETOR_DETAILS', 'False')
show_full_title_data = os.getenv('SHOW_FULL_TITLE_DATA', 'True').lower() == 'true'
show_full_title_pdf = os.getenv('SHOW_FULL_TITLE_PDF', 'True').lower() == 'true'
title_register_nominal_summary_price = float(os.getenv('TITLE_REGISTER_NOMINAL_SUMMARY_PRICE', 1))  # (Pound) 'WP_AUTH_CURR': 'GBP'
standard_vat_rate = float(os.getenv('STANDARD_VAT_RATE', 20))        # %
title_register_summary_price = float(title_register_nominal_summary_price * (100 + standard_vat_rate) / 100)
search_request_interface_url = os.getenv('SEARCH_REQUEST_INTERFACE_URL', 'http://127.0.0.1:5353')
payment_interface_url = os.getenv('PAYMENT_INTERFACE_URL', 'http://127.0.0.1:5555/wp')
post_confirmation_url = os.getenv('POST_CONFIRMATION_URL', payment_interface_url)

CONFIG_DICT = {
    'DEBUG': DEBUG,
    'FAULT_LOG_FILE_PATH': fault_log_file_path,
    'GOOGLE_ANALYTICS_API_KEY': google_analytics_api_key,
    'LOGGING': True,
    'LOGGING_CONFIG_FILE_PATH': logging_config_file_path,
    'PERMANENT_SESSION_LIFETIME': timedelta(minutes=15),
    'REGISTER_TITLE_API': register_title_api,
    'SECRET_KEY': secret_key,
    'SERVICE_NOTICE_HTML': service_notice_html,
    'SESSION_COOKIE_SECURE': session_cookie_secure,
    'MORE_PROPRIETOR_DETAILS': more_proprietor_details,
    'SHOW_FULL_TITLE_DATA': show_full_title_data,
    'SHOW_FULL_TITLE_PDF': show_full_title_pdf,
    'SEARCH_REQUEST_INTERFACE_URL': search_request_interface_url,
    'TITLE_REGISTER_SUMMARY_PRICE': '{:.2f}'.format(title_register_summary_price),
    'PAYMENT_INTERFACE_URL': payment_interface_url,
    'POST_CONFIRMATION_URL': post_confirmation_url,
}  # type: Dict[str, Union[bool, str, timedelta]]

# <worldpay> (Derived from https://gh-svn-d01.diti.lr.net/svn/eservices/branches/release1415/ECBX_PortServicesBackEnd).
WORLDPAY_DICT = {
    'C_returnURL': 'http://{}/titles/',
    'C_returnURLCancel': '/title-search',
    'C_returnURLCallback': ''
}

# N.B: we do not want 'live' by default - it should be set explicitly in the environment, as required.
settings = os.getenv('SETTINGS', 'DEV').lower()

if settings == 'live':
    CONFIG_DICT['DEBUG'] = False
elif settings == 'dev':
    CONFIG_DICT['DEBUG'] = True
elif settings == 'test':
    # We do NOT set TESTING to True here as it turns off authentication, and we
    # want to make sure the app behaves the same when running tests locally
    # as it does in production.
    CONFIG_DICT['DEBUG'] = True
    CONFIG_DICT['DISABLE_CSRF_PREVENTION'] = True
    CONFIG_DICT['FAULT_LOG_FILE_PATH'] = '/dev/null'
    CONFIG_DICT['LOGGING'] = False
