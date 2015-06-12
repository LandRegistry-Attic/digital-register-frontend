#!/bin/sh
export SETTINGS='dev'

export APPLICATION_SECRET_KEY='secretkeyshouldberandom'
export FAULT_LOG_FILE_PATH='/var/log/applications/digital-register-frontend-fault.log'
export GOOGLE_ANALYTICS_API_KEY='UA-59849906-2'
export LOGGING_CONFIG_FILE_PATH='logging_config.json'
export LOGIN_API='http://landregistry.local:8005/'
export PYTHONPATH=.
export REGISTER_TITLE_API='http://landregistry.local:8004/'
export SERVICE_INTERRUPT_WARNING=''
export SESSION_COOKIE_SECURE='False'
