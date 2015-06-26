#!/bin/sh
export SETTINGS='dev'

export APPLICATION_SECRET_KEY='secretkeyshouldberandom'
export FAULT_LOG_FILE_PATH='/var/log/applications/digital-register-frontend-fault.log'
export GOOGLE_ANALYTICS_API_KEY='UA-59849906-2'
export LOGGING_CONFIG_FILE_PATH='logging_config.json'
export LOGIN_API='http://landregistry.local:8005/'
export PYTHONPATH=.
export MORE_PROPRIETOR_DETAILS='true'
export REGISTER_TITLE_API='http://landregistry.local:8004/'
export SERVICE_NOTICE_HTML='<h2>Downtime notice</h2><p>This service will be offline between 2.00&ndash;5.00 on 31st July</p>'
export SESSION_COOKIE_SECURE='False'

