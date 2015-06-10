from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
import dateutil
import dateutil.parser
import faulthandler
from flask_login import LoginManager

from config import CONFIG_DICT
from service import logging_config, error_handler, static

# This causes the traceback to be written to the fault log file in case of serious faults
fault_log_file = open(CONFIG_DICT['FAULT_LOG_FILE_PATH'], 'a')
faulthandler.enable(file=fault_log_file)

app = Flask(__name__)
app.config.update(CONFIG_DICT)

static.register_assets(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.session_protection = "strong"


def format_date(value):
    return dateutil.parser.parse(value).strftime("%d %B %Y")


def format_time(value):
    return dateutil.parser.parse(value).strftime("%H:%M:%S")


def pluralize(number, singular = '', plural = 's'):
    if number == 1:
        return singular
    else:
        return plural

app.jinja_env.filters['date'] = format_date
app.jinja_env.filters['time'] = format_time
app.jinja_env.filters['pluralize'] = pluralize
GOOGLE_ANALYTICS_API_KEY = app.config['GOOGLE_ANALYTICS_API_KEY']


@app.context_processor
def inject_google_analytics():
    return dict(google_api_key=GOOGLE_ANALYTICS_API_KEY)


logging_config.setup_logging()
error_handler.setup_errors(app)
