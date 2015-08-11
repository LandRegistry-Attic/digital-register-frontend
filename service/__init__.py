import dateutil                       # type: ignore
import dateutil.parser                # type: ignore
import faulthandler                   # type: ignore
from flask import Flask               # type: ignore
from flask_login import LoginManager  # type: ignore
import re

from config import CONFIG_DICT
from service import logging_config, error_handler, static

pattern = re.compile(r'[^a-zA-Z0-9_ ;:\-,\.()&£]+', re.UNICODE)

# This causes the traceback to be written to the fault log file in case of serious faults
fault_log_file = open(str(CONFIG_DICT['FAULT_LOG_FILE_PATH']), 'a')
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


def pluralize(number, singular='', plural='s'):
    if number == 1:
        return singular
    else:
        return plural


def checkexistence(value):
    if not value:
        return ' Not Dated '
    else:
        return value


def strip_non_alpha_numeric_vales(value):
    return re.sub(pattern, '', value)


app.jinja_env.filters['date'] = format_date
app.jinja_env.filters['time'] = format_time
app.jinja_env.filters['pluralize'] = pluralize
app.jinja_env.filters['checkexistence'] = checkexistence
app.jinja_env.filters['strip_non_alpha_numeric_vales'] = strip_non_alpha_numeric_vales

GOOGLE_ANALYTICS_API_KEY = app.config['GOOGLE_ANALYTICS_API_KEY']


@app.context_processor
def inject_google_analytics():
    return {'google_api_key': GOOGLE_ANALYTICS_API_KEY}


logging_config.setup_logging()
error_handler.setup_errors(app)
