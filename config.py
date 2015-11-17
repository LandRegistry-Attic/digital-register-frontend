from datetime import timedelta
import os
from typing import Dict, Union

DEBUG = False

fault_log_file_path = os.environ['FAULT_LOG_FILE_PATH']
google_analytics_api_key = os.environ['GOOGLE_ANALYTICS_API_KEY']
logging_config_file_path = os.environ['LOGGING_CONFIG_FILE_PATH']
register_title_api = os.environ['REGISTER_TITLE_API']
secret_key = os.environ['APPLICATION_SECRET_KEY']
service_notice_html = os.environ['SERVICE_NOTICE_HTML']
session_cookie_secure = os.environ['SESSION_COOKIE_SECURE'].lower() != 'false'
more_proprietor_details = os.environ['MORE_PROPRIETOR_DETAILS']
show_full_title_data = os.environ['SHOW_FULL_TITLE_DATA'].lower() == 'true'
show_full_title_pdf = os.environ['SHOW_FULL_TITLE_PDF'].lower() == 'true'
title_register_summary_price = "&pound;1.20 (incl. VAT)"
payment_interface_url = os.getenv('PAYMENT_INTERFACE_URL', 'http://127.0.0.1:5555')  # payment_interface_server.py
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
    'TITLE_REGISTER_SUMMARY_PRICE': title_register_summary_price,
    'POST_CONFIRMATION_URL': post_confirmation_url,
    'PROPERTY_SEARCH_INTERFACE_URL': property_search_interface_url
}  # type: Dict[str, Union[bool, str, timedelta]]

# <worldpay> (From https://gh-svn-d01.diti.lr.net/svn/eservices/branches/release1415/ECBX_PortServicesBackEnd).
WP_TEST_MODE_ON = 100
WP_TEST_MODE_OFF = 0

WORLDPAY_DICT = {
    'PAYMENT_INTERFACE_URL': os.getenv('PAYMENT_INTERFACE_URL', 'http://127.0.0.1:5555/'),
    'WORLDPAY_REDIRECT_URL': 'https://secure-test.worldpay.com/wcc/purchase',
    'WP_AUTH_CURR': 'GBP',
    'WP_INST_ID': os.getenv('WP_INST_ID', ''),
    'WP_ACCOUNT_ID': os.getenv('WP_ACCOUNT_ID', ''),
    'WP_AUTH_MODE': 'E',
    'WP_TEST_MODE': WP_TEST_MODE_ON,
    'WP_DEFAULT_COUNTRY': 'GB',
    'WP_CALLBACK_SERVER_URL': os.getenv('WP_CALLBACK_SERVER_URL', ''),
    'ACTION_URL1': '/download.do',
    'ACTION_URL2': '/QuickEnquiryInit.do',
    'ACTION_URL3': ''
}
#</worldpay>

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
