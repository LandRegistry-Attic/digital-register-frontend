from flask import Markup, request, render_template
from werkzeug.exceptions import default_exceptions, HTTPException


def setup_errors(app, error_template="error.html"):
    """Add a handler for each of the available HTTP error responses."""
    def error_handler(error):
        if isinstance(error, HTTPException):
            description = error.get_description(request.environ)
            code = error.code
        else:
            description = error
            code = 500
        return render_template(error_template,
                               asset_path='../static/',
                               error=error,
                               code=code,
                               description=Markup(description)), code

    for exception in default_exceptions:
        app.register_error_handler(exception, error_handler)