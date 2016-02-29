import atexit  # type: ignore
from flask_wtf.csrf import CsrfProtect  # type: ignore
import logging  # type: ignore

from service.server import app  # type: ignore

LOGGER = logging.getLogger(__name__)


@atexit.register
def handle_shutdown(*args, **kwargs):
    LOGGER.info('Stopped the server')

LOGGER.info('Starting the server')
CsrfProtect(app)
port = int(app.config.get('PORT', 8003))
app.run(host='0.0.0.0', port=port)
