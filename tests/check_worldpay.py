import os
from flask import Flask
from flask import render_template
from flask import request
from config import WORLDPAY_DICT, ROOT_DIR

tmpl_dir = os.path.join(ROOT_DIR, os.path.normpath('service/templates'))

app = Flask(__name__, template_folder=tmpl_dir)

# Fix formatting issue (keys).
_worldpay_dict = dict((k.lower(), v) for k,v in WORLDPAY_DICT.items())
app.config.update(_worldpay_dict)

@app.route('/', methods=['GET'])
def _():
    """
    Check that import/include works and that WorldPay 'sandbox' service is OK.
    """

    _worldpay_dict.update({'mc_timestamp': '2015-10-07-09.58.39.347287'})
    _worldpay_dict.update({'mc_purchasetype': 'registerOnly'})
    _worldpay_dict.update({'mc_titlenumber': 'LA265'})
    _worldpay_dict.update({'mc_searchtype': 'T'})
    _worldpay_dict.update({'mc_portalind': 'Y'})

    return render_template('dummy_confirm_selection.html', worldpay_params=_worldpay_dict)

# This is the "Callback URL" that Worldpay invokes after completing the payment process.
@app.route('/callback', methods=['GET', 'POST'])
def callback():
    print(request.data)

if __name__ == '__main__':
    app.run(debug=True)
