import os
from flask import Flask, render_template, request
from config import WORLDPAY_DICT, ROOT_DIR

tmpl_dir = os.path.join(ROOT_DIR, os.path.normpath('service/templates'))

app = Flask(__name__, template_folder=tmpl_dir)

# Fix formatting issue (keys).
_worldpay_dict = dict((k.lower(), v) for k,v in WORLDPAY_DICT.items())

@app.route('/', methods=['POST'])
def worldpay():
    """
    Populate dict with user variables passed in, then re-post to Worldpay.
    """

    _worldpay_dict.update(request.form)
    return render_template('hiddenWP.html', worldpay_params=_worldpay_dict)

if __name__ == '__main__':
    app.run(debug=True)
