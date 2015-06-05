from flask import Markup, request, render_template
from werkzeug.exceptions import default_exceptions, HTTPException
import logging

GENERIC_ERROR_WORDING = 'Sorry, we are experiencing technical difficulties.'
GENERIC_ERROR_DESCRIPTION = 'Please try again in a few moments.'
ERROR_404_WORDING = 'Page not found'
ERROR_404_DESCRIPTION = 'If you entered a web address please check it was correct.'
LOGGER = logging.getLogger(__name__)


def setup_errors(app, error_template="error.html"):
    google_analytics_api_key = app.config['GOOGLE_ANALYTICS_API_KEY']

    def error_handler(error):
        LOGGER.error('An error occurred when processing a request', exc_info=error)
        if isinstance(error, HTTPException) and error.code == 404:
            code = error.code
            error_title = ERROR_404_WORDING
            description = ERROR_404_DESCRIPTION
        else:
            code = 500
            error_title = GENERIC_ERROR_WORDING
            description = GENERIC_ERROR_DESCRIPTION
        return render_template(error_template,
                               error=error_title,
                               code=code,
                               description=Markup(description)), code

    for exception in default_exceptions:
        app.register_error_handler(exception, error_handler)
    app.register_error_handler(Exception, error_handler)
