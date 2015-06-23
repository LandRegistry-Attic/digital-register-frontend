#!/bin/sh
export SETTINGS='dev'
export REGISTER_TITLE_API='http://landregistry.local:8004/'
export LOGGING_CONFIG_FILE_PATH='logging_config.json'
export FAULT_LOG_FILE_PATH='/var/log/applications/digital-register-frontend-fault.log'
export GOOGLE_ANALYTICS_API_KEY='UA-59849906-2'
export APPLICATION_SECRET_KEY='secretkeyshouldberandom'
export LOGIN_API='http://landregistry.local:8005/'
export SESSION_COOKIE_SECURE='False'
export PYTHONPATH=.
export MORE_PROPRIETOR_DETAILS='true'
