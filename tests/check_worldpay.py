import os
from service import utils
from flask import Flask, render_template
from config import CONFIG_DICT
#from service.server import app

app = Flask(__name__,  template_folder='/vagrant/apps/digital-register-frontend/service/templates')
app.config.update(CONFIG_DICT)


@app.route('/wp', methods=['GET'])
def _():
    """
    Check that WorldPay 'sandbox' service is OK.

    Note: 'test card' numbers at http://support.worldpay.com/support/kb/bg/testandgolive/tgl5103.html.
    """

    _worldpay_dict = dict()

    # N.B.: need fixed value for 'mc_timestamp', to suit WPAC test configuration.
    _worldpay_dict['PAYMENT_INTERFACE_URL'] = app.config['PAYMENT_INTERFACE_URL']
    _worldpay_dict['MC_unitCount'] = '1'
    _worldpay_dict['MC_timestamp'] = os.getenv('WP_MC_timestamp', '')
    _worldpay_dict['amount'] = os.getenv('WP_amount', '')
    _worldpay_dict['MC_titleNumber'] = os.getenv('WP_MC_titleNumber', '')
    _worldpay_dict['cartId'] = os.getenv('WP_cartId', '')

    # Form valid URL for external remote access.
    # N.B.: cannot use 'request.host' because that may return given setting (e.g. '0.0.0.0') rather than IP address.
    ip_address = utils.get_ip_address()
    _worldpay_dict['C_returnURL'] = 'http://{}/titles/'.format(ip_address)

    return render_template('dummy_confirm_selection.html', worldpay_params=_worldpay_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
