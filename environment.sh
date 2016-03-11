#!/bin/sh
export SETTINGS='dev'

export APPLICATION_SECRET_KEY='secretkeyshouldberandom'
export FAULT_LOG_FILE_PATH='/var/log/applications/digital-register-frontend-fault.log'
export GOOGLE_ANALYTICS_API_KEY='UA-59849906-2'
export LOGGING_CONFIG_FILE_PATH='logging_config.json'
export PYTHONPATH=.
export MORE_PROPRIETOR_DETAILS='true'
export REGISTER_TITLE_API='http://172.16.42.43:8004'
# export LAND_REGISTRY_PAYMENT_INTERFACE_URI='https://preprod.registerview.landregistryconcept.co.uk/paymenti/wp'   # LRPI 'wp' endpoint
export LAND_REGISTRY_PAYMENT_INTERFACE_BASE_URI='http://172.16.42.43:8011'
export LAND_REGISTRY_PAYMENT_INTERFACE_URI='http://172.16.42.43:8011/wp'
export PAYMENT_SERVICE_PROVIDER_URI='https://secure-test.worldpay.com/wcc/purchase'
export SERVICE_NOTICE_HTML='<h2>Downtime notice</h2><p>This service will be offline between 2.00&ndash;5.00 on 31st July</p>'
export SESSION_COOKIE_SECURE='False'

# Ensure the following 2 FULL_TITLE env vars are false in pre-prod and prod (until we get the green light)
export SHOW_FULL_TITLE_DATA='true'
export SHOW_FULL_TITLE_PDF='true'
