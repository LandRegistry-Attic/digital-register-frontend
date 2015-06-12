import os
import datetime

fault_log_file_path = os.environ['FAULT_LOG_FILE_PATH']
google_analytics_api_key = os.environ['GOOGLE_ANALYTICS_API_KEY']
register_title_api = os.environ['REGISTER_TITLE_API']
logging_config_file_path = os.environ['LOGGING_CONFIG_FILE_PATH']
login_api = os.environ['LOGIN_API']
secret_key = os.environ['APPLICATION_SECRET_KEY']
service_interrupt_warning = os.environ['SERVICE_INTERRUPT_WARNING']
session_cookie_secure = os.environ['SESSION_COOKIE_SECURE'].lower() != 'false'

CONFIG_DICT = {
    'DEBUG': False,
    'FAULT_LOG_FILE_PATH': fault_log_file_path,
    'GOOGLE_ANALYTICS_API_KEY': google_analytics_api_key,
    'LOGGING': True,
    'LOGGING_CONFIG_FILE_PATH': logging_config_file_path,
    'LOGIN_API': login_api,
    'PERMANENT_SESSION_LIFETIME': datetime.timedelta(minutes=15),
    'REGISTER_TITLE_API': register_title_api,
    'SECRET_KEY': secret_key,
    'SERVICE_INTERRUPT_WARNING': service_interrupt_warning,
    'SESSION_COOKIE_SECURE': session_cookie_secure,
}

settings = os.environ.get('SETTINGS')

if settings == 'dev':
    CONFIG_DICT['DEBUG'] = True
elif settings == 'test':
    # We do NOT set TESTING to True here as it turns off authentication, and we
    # want to make sure the app behaves the same when running tests locally
    # as it does in production.
    CONFIG_DICT['DEBUG'] = True
    CONFIG_DICT['DISABLE_CSRF_PREVENTION'] = True
    CONFIG_DICT['FAULT_LOG_FILE_PATH'] = '/dev/null'
    CONFIG_DICT['LOGGING'] = False
    CONFIG_DICT['SLEEP_BETWEEN_LOGINS'] = False
