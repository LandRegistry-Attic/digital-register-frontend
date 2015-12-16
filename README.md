# digital-register-frontend

This is the repo for the frontend of the digital register service. It is written in Python, with the Flask framework.

### Digital Register Frontend build status

[![Build Status](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Master)/badge/icon)](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Master)/)

### Digital Register Frontend Acceptance tests status
[![Build Status](http://52.16.47.1/job/digital-register-frontend-acceptance-tests/badge/icon)](http://52.16.47.1/job/digital-register-frontend-acceptance-tests/)

## Execution

### Run the tests

To run the tests for the Digital Register, go to its folder and run `lr-run-tests`.

### Run the acceptance tests

To run the acceptance tests for the Digital Register, go to the `acceptance-tests` folder and run:

```
   ./run-tests.sh
```

You will need to have a Postgres database running (see `db/lr-start-db` and `db/insert-fake-data` scripts in the [centos-dev-env](https://github.com/LandRegistry/centos-dev-env) project), as well as the digital-register-frontend and digital-register-api applications running on your development VM.

Alternatively, simply run:

    lr-run-acceptance-tests

## Run the server

### Run in dev mode

To run the server in dev mode, go to its folder and execute the following command:

    lr-run-app

Note that pre/post execution scripts are available, which can be customised during development:

```
   .setup.sh
   .teardown.sh
```

See the 'centos-dev-env' repository for further details.

### Run using gunicorn

To run the server using gunicorn, activate your virtual environment, add the application directory to python path
(e.g. `export PYTHONPATH=/vagrant/apps/digital-register-frontend/:$PYTHONPATH`) and execute the following commands:

    pip install gunicorn
    gunicorn -p /tmp/gunicorn-digital-register-frontend.pid service.server:app -c gunicorn_settings.py


## Jenkins builds

We use three separate builds:
- [branch](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Branch)/)
- [master](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Master)/)
- [acceptance](http://52.16.47.1/job/digital-register-frontend-acceptance-tests/)

## SASS libraries

### GOV.UK template

[govuk_template](http://alphagov.github.io/govuk_template/)

In order to update:
* download the 'plain HTML' version and replace the `static/govuk_template` folder with its assets
* replace the `govuk_template.html` file in the `static/templates` folder with its HTML file

### GOV.UK frontend toolkit

[govuk_frontend_toolkit](https://github.com/alphagov/govuk_frontend_toolkit)

It is included in our `static` folder as a gitsubmodule. It can be updated by bumping up its commit hash.

## Dependencies

WeasyPrint (used to generate the PDFs) needs some dependencies. They can be installed by running the following command from inside the dev environment:

`sudo yum install cairo pango gdk-pixbuf2 libffi-devel libxslt-devel libxml2-devel python-cairosvg`

The GDSTransportWebsite fonts should also be installed (although you can generate the PDFs without them - they just wont look as nice). Copy GDSTransportWebsite.ttf and GDSTransportWebsite-Bold.ttf to /usr/share/fonts/GDSTransportWebsite/

## Third Party Tools

<a href="http://www.browserstack.com"><img src="https://www.browserstack.com/images/layout/browserstack-logo-600x315.png" alt="browserstack logo" width=300/></a>

<p>This repo is being tested using browserstack</p>
<p><i>Rapid Selenium webdriver testing with 100% reliability</i></p>

## Welsh language support

This has been implemented with Flask-Babel.

### Dependency

There is a single dependency: the Flask-Babel package. It should be specified in `requirements.sh`;

    Flask-Babel==0.9

### Setup

Include the following lines in the application `__init__.py`;

```python
from flask.ext.babel import Babel
.
.
babel = Babel(app)
.
.
@babel.localeselector
def get_locale():
    return g.locale
.
@app.before_request
def before_request():
    g.locale = request.args.get('language','en')
    g.current_lang = g.locale
```

The language code ('en' or 'cy') is maintained in the Flask global `g`. By default it is initialised to 'en' (English). The `localeselector` decorator function returns the value of `g`.

On the client side, the value is set in `display_title.html`. At the top of the template is a form with no action; when the submit button is pressed, the form will resubmit the page. The language value is set through the `name` GET parameter, which is added to the url when the page is resubmitted. Flask will detect the language code through the `before_request` decorator function and set the value of `g.locale`.

Now create a file in the root application folder and call it `babel.cfg`. Add the following lines to this file;

    python: **.py]
    [jinja2: **/templates/**.html]
    extensions=jinja2.ext.autoescape,jinja2.ext.with_

### Translations

There is a good tutorial available [here](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-i18n-and-l10n)

The following summarises the steps required to create and update the translations.

NB: Babel does not translate anything; that has to be done by a human (preferably one that is a native speaker).

#### Mark the text

Text must first be tagged (or marked) for translation. The text would normally be in a Jinja template, but it doesn't have to be (it can be anywhere in the application).

Text should be marked with a combination of Jinja and Babel tags. For example, an entry such as this;

    <h1>Heading</h1>

would be converted to;

    <h1>{{ _('Heading') }}</h1>

#### Extract the text

    NB: for all the next steps, you will need to open a terminal window and navigate
    to the root application folder (ie, digital-register-frontend/)

The next step is to extract all text that has been marked, as above.

    pybabel extract -F babel.cfg -o messages.pot .

This step creates the `messages.pot` file, which contains a list of all texts that require translation. Do not edit this file. It is temporary and can be deleted when all the steps are complete.

#### Generate the language dictionary

This next step creates the folder structure that will retain a human-readable translation file and an associated compiled file that will be used by Flask-Babel.

    pybabel init -i messages.pot -d service/translations -l cy

Make sure that there is a `translations` folder in `service/` as this is where Flask-Babel will look.

This step should create the following file;

    service/translations/cy/LC_MESSAGES/messages.po

This is the file that should contain the Welsh translations. It can be edited in any text editor.

An example of a translation is;

    #: service/templates/display_title.html:56
    #, fuzzy
    msgid "Summary of title"
    msgstr "Crynodeb o deitl "

The value for `msgstr` is added manually.

#### Compile the translations

The final step is to compile the translations into a `.mo` file. The command is;

    pybabel compile -f -d service/translations

Verify `service/translations/cy/LC_MESSAGES`; it should contain two files, 'messages.po' (the original language file) and `messages.mo` (the compiled language file).

#### Updating the translations

Translations can be updated by re-running the extract command above followed by an update;

    pybabel extract -F babel.cfg -o messages.pot .
    pybabel update -i messages.pot -d service/translations

The update command should merge existing and new translations. Following this, recompile in the same way as above;

    pybabel compile -f -d service/translations

Cael hwyl!
