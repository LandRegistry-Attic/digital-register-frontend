from flask import Flask, render_template, request, abort
from config import WORLDPAY_DICT, ROOT_DIR
from service import app


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
        # TODO: Should have a log call here.
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
