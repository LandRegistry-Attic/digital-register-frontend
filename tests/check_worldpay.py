import os
from flask import Flask
from flask import render_template
from config import WORLDPAY_DICT, ROOT_DIR
from datetime import datetime

tmpl_dir = os.path.join(ROOT_DIR, os.path.normpath('service/templates'))

app = Flask(__name__, template_folder=tmpl_dir)

# Fix formatting issue (keys).
_worldpay_dict = dict((k.lower(), v) for k,v in WORLDPAY_DICT.items())

@app.route('/', methods=['GET'])
def _():
    """
    Check that WorldPay 'sandbox' service is OK.
    """

    _worldpay_dict.update({'mc_timestamp': datetime.now()})

    return render_template('dummy_confirm_selection.html', worldpay_params=_worldpay_dict)

if __name__ == '__main__':
    app.run(debug=True)
