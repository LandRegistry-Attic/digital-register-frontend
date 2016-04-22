import os
from datetime import timedelta
from typing import Dict, Union


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
title_register_summary_price_text = "&pound{} inc VAT"

CONFIG_DICT = {  # type: ignore
    'LOGGING_LEVEL': os.environ.get('LOGGING_LEVEL', "WARN"),
    'FAULT_LOG_FILE_PATH': fault_log_file_path,
    'GOOGLE_ANALYTICS_API_KEY': google_analytics_api_key,
    'LOGGING': True,
    'LOGGING_CONFIG_FILE_PATH': logging_config_file_path,
    'PERMANENT_SESSION_LIFETIME': timedelta(minutes=15),
    'REGISTER_TITLE_API': register_title_api,
    'LAND_REGISTRY_PAYMENT_INTERFACE_URI': os.environ['LAND_REGISTRY_PAYMENT_INTERFACE_URI'],
    'LAND_REGISTRY_PAYMENT_INTERFACE_BASE_URI': os.environ['LAND_REGISTRY_PAYMENT_INTERFACE_BASE_URI'],
    'SECRET_KEY': secret_key,
    'SERVICE_NOTICE_HTML': service_notice_html,
    'SESSION_COOKIE_SECURE': session_cookie_secure,
    'MORE_PROPRIETOR_DETAILS': more_proprietor_details,
    'SHOW_FULL_TITLE_DATA': show_full_title_data,
    'SHOW_FULL_TITLE_PDF': show_full_title_pdf,
    'TITLE_REGISTER_SUMMARY_PRICE_TEXT': title_register_summary_price_text,

    # This value is set at run-time.
    'TITLE_REGISTER_SUMMARY_PRICE': None,
}  # type: Dict[str, Union[bool, str, timedelta]]

settings = os.environ.get('SETTINGS')

if settings == 'test':
    # We do NOT set TESTING to True here as it turns off authentication, and we
    # want to make sure the app behaves the same when running tests locally
    # as it does in production.
    CONFIG_DICT['DISABLE_CSRF_PREVENTION'] = True
    CONFIG_DICT['FAULT_LOG_FILE_PATH'] = '/dev/null'
