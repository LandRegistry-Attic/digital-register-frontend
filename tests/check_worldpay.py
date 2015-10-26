from flask import Flask
from flask import render_template
from flask import request
from config import WORLDPAY_DICT

app = Flask(__name__, template_folder='service/templates')


# Fix formatting issue.
_worldpay_dict = dict((k.lower(), v) for k,v in WORLDPAY_DICT.items())
app.config.update(_worldpay_dict)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/check', methods=['GET'])
def _():
    """
    Check that import/include works and that WorldPay 'sandbox' service is OK.
    """

    return render_template('dummy_confirm_selection.html', worldpay_params=_worldpay_dict)

# This is the "Callback URL" that Worldpay invokes after completing the payment process.
@app.route('/', methods=['GET', 'POST'])
def callback():
    print(request.data)

if __name__ == '__main__':
    app.run(debug=True)
