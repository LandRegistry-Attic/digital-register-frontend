import logging
from flask import render_template, request, abort
from config import WORLDPAY_DICT
from service import app

LOGGER = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST'])
def worldpay():
    """
    Populate dict with user variables passed in, then re-post to Worldpay.
    """


    try:
        # N.B.: "request.form" is a 'multidict', so need to flatten it first; assume single value per key.
        WORLDPAY_DICT.update(request.form.to_dict())

        # Convert to lower case, for use by template.
        _worldpay_dict = dict((k.lower(), v) for k,v in WORLDPAY_DICT.items())

        return render_template('hiddenWP.html', worldpay_params=_worldpay_dict)

    # Any generic errors should be handled elsewhere ...
    except Exception as e:
        LOGGER.error(e)
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
