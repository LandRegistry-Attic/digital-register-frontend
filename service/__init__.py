import faulthandler                     # type: ignore
from flask import Flask, request, g     # type: ignore
from flask.ext.babel import Babel       # type: ignore

from config import CONFIG_DICT          # type: ignore
from service import logging_config, error_handler, static, title_utils, template_filters   # type: ignore

# This causes the traceback to be written to the fault log file in case of serious faults
fault_log_file = open(str(CONFIG_DICT['FAULT_LOG_FILE_PATH']), 'a')
faulthandler.enable(file=fault_log_file)

app = Flask(__name__)
app.config.update(CONFIG_DICT)
babel = Babel(app)

LANGUAGES = {
    'cy': 'Cymraeg',
    'en': 'English'
}

# app.config['BABEL_DEFAULT_LOCALE'] = 'en'


@babel.localeselector
def get_locale():
    return g.locale


@app.before_request
def before_request():
    g.locale = request.args.get('language', 'en')
    g.current_lang = g.locale


static.register_assets(app)  # type: ignore

for (filter_name, filter_method) in template_filters.get_all_filters().items():  # type: ignore
    app.jinja_env.filters[filter_name] = filter_method

GOOGLE_ANALYTICS_API_KEY = app.config['GOOGLE_ANALYTICS_API_KEY']


@app.context_processor
def inject_google_analytics():
    return {'google_api_key': GOOGLE_ANALYTICS_API_KEY}


logging_config.setup_logging()  # type: ignore
if app.config['DEBUG'] is False:
    # Retain traceback when DEBUG = True
    error_handler.setup_errors(app)  # type: ignore
error_handler.setup_errors(app)  # type: ignore
