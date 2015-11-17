from collections import OrderedDict
from service import api_client

healthchecks = OrderedDict([
    ('digital-register-api', api_client.check_health),
])


# TODO: tested through test_app - should have its own tests now
def perform_healthchecks():
    results = [_check_application_health(app_name) for app_name in healthchecks.keys()]
    error_messages = [error_msg for result in results for error_msg in result]
    return error_messages


def _check_application_health(application_name):
    try:
        healthcheck_response = healthchecks[application_name]()
        response_json = _get_json_from_response(healthcheck_response)

        if response_json:
            return _extract_errors_from_health_response_json(response_json, application_name)
        else:
            return ['{0} health endpoint returned an invalid response: {1}'.format(
                application_name, healthcheck_response.text)]
    except Exception as e:
        return ['Problem talking to {0}: {1}'.format(application_name, str(e))]


def _get_json_from_response(response):
    try:
        return response.json()
    except Exception:
        return None


def _extract_errors_from_health_response_json(response_json, application_name):
    if response_json.get('status') == 'ok':
        return []
    elif response_json.get('errors'):
        return ['{0} health endpoint returned errors: {1}'.format(
            application_name, response_json['errors'])]
    else:
        return ['{0} health endpoint returned an invalid response: {1}'.format(
            application_name, response_json)]
