from flask import render_template
from config import WORLDPAY_DICT, CONFIG_DICT, ROOT_DIR
from service import app


# Fix formatting issue (keys).
_worldpay_dict = dict((k.lower(), v) for k,v in WORLDPAY_DICT.items())

@app.route('/', methods=['GET'])
def _():
    """
    Check that WorldPay 'sandbox' service is OK.

    Note: 'test card' numbers at http://support.worldpay.com/support/kb/bg/testandgolive/tgl5103.html.
    """

    # N.B.: need fixed value for 'mc_timestamp', to suit WPAC test configuration.
    _worldpay_dict.update({'mc_timestamp': '2015-11-20 11:54:23.861921'})
    _worldpay_dict.update({'payment_interface_url': app.config['PAYMENT_INTERFACE_URL']})

    return render_template('dummy_confirm_selection.html', worldpay_params=_worldpay_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
