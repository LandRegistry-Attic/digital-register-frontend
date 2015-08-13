import faulthandler                   # type: ignore
from flask import Flask               # type: ignore
from flask_login import LoginManager  # type: ignore

from config import CONFIG_DICT
from service import logging_config, error_handler, static, title_utils, template_filters

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

for (filter_name, filter_method) in template_filters.get_all_filters().items():
    app.jinja_env.filters[filter_name] = filter_method

GOOGLE_ANALYTICS_API_KEY = app.config['GOOGLE_ANALYTICS_API_KEY']


@app.context_processor
def inject_google_analytics():
    return {'google_api_key': GOOGLE_ANALYTICS_API_KEY}

logging_config.setup_logging()
error_handler.setup_errors(app)
