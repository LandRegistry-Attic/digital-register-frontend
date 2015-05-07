from flask import Flask
import dateutil
import dateutil.parser
import faulthandler
from flask_login import LoginManager

from config import CONFIG_DICT
from service import logging_config

# This causes the traceback to be written to stderr in case of faults
faulthandler.enable()

app = Flask(__name__)
app.config.update(CONFIG_DICT)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.session_protection = "strong"


def format_datetime(value):
    return dateutil.parser.parse(value).strftime("%d %B %Y at %H:%M:%S")

app.jinja_env.filters['datetime'] = format_datetime
logging_config.setup_logging()
