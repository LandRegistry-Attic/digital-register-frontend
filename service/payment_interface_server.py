import os
from flask import Flask, render_template, request, flash
from config import WORLDPAY_DICT, ROOT_DIR

tmpl_dir = os.path.join(ROOT_DIR, os.path.normpath('service/templates'))

app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/', methods=['GET', 'POST'])
def worldpay():
    """
    Populate dict with user variables passed in, then re-post to Worldpay.
    """

    # N.B.: "request.form" is a 'multidict', so need to flatten it first; assume single value per key.
    WORLDPAY_DICT.update(request.form.to_dict())

    # Convert to lower case, for use by template.
    _worldpay_dict = dict((k.lower(), v) for k,v in WORLDPAY_DICT.items())
    for k,v in _worldpay_dict.items():
        flash("%s: %s" % (k,v))

    return render_template('hiddenWP.html', worldpay_params=_worldpay_dict)

if __name__ == '__main__':
    app.run(debug=True, port=5555)
