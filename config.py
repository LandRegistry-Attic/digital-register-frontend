import os
import datetime


CONFIG_DICT = {
    'DEBUG': False,
    'REGISTER_TITLE_API': 'http://landregistry.local:8004/',
    'LOGGING_CONFIG_FILE_PATH': 'logging_config.json',
    'LOGIN_API': 'http://landregistry.local:8005/',
    'GOOGLE_ANALYTICS_API_KEY': 'UA-59849906-2',
    'PERMANENT_SESSION_LIFETIME': datetime.timedelta(minutes=15),
    'SECRET_KEY': os.environ['APPLICATION_SECRET_KEY'],
}

settings = os.environ.get('SETTINGS')

if settings == 'dev':
    CONFIG_DICT['DEBUG'] = True
elif settings == 'test':
    CONFIG_DICT['DEBUG'] = True
    CONFIG_DICT['TESTING'] = True
