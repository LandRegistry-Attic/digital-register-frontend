from datetime import timedelta
import os
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
payment_interface_url = os.getenv('PAYMENT_INTERFACE_URL', 'http://0.0.0.0:5555')
search_request_interface_url = os.getenv('SEARCH_REQUEST_INTERFACE_URL', 'http://127.0.0.1:5353')
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
CONFIG_DICT.update({'DEBUG': True})
WP_TEST_MODE_ON = 100
WP_TEST_MODE_OFF = 0

# N.B.: 'WP_AUTHORISATION_CALLBACK_URL' must not be prefixed by 'http://' or it will be silently rejected by Worldpay!!
WORLDPAY_DICT = {
    'WORLDPAY_REDIRECT_URL': 'https://secure-test.worldpay.com/wcc/purchase',
    'WP_AUTH_CURR': 'GBP',
    'WP_UNIT_COUNT': 1,
    'WP_INST_ID': os.getenv('WP_INST_ID', ''),
    'WP_ACCOUNT_ID': os.getenv('WP_ACCOUNT_ID', ''),
    'WP_AUTH_MODE': 'E',
    'WP_PORTALIND': 'Y',
    'WP_TEST_MODE': WP_TEST_MODE_ON,
    'WP_DEFAULT_COUNTRY': 'GB',
    'WP_AUTHORISATION_CALLBACK_URL': os.getenv('WP_AUTHORISATION_CALLBACK_URL', ''),    # -> 'WPAC' service.
    'ACTION_URL1': '/download.do',
    'ACTION_URL2': '/QuickEnquiryInit.do',
    'ACTION_URL3': ''
}

# N.B: we do not want 'live' by default - it should be set explicitly in the environment, as required.
settings = os.getenv('SETTINGS', 'DEV').lower()

if settings == 'live':
    WORLDPAY_DICT['WP_TEST_MODE'] = WP_TEST_MODE_OFF
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
