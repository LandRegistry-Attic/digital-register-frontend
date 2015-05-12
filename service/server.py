#!/usr/bin/env python
import json
from flask import abort, render_template, request, redirect, url_for, session
from flask import Markup
from flask_login import login_user, login_required, current_user
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
import logging
import logging.config
import os
import re
import requests
import time
from wtforms.fields import StringField, PasswordField
from wtforms.validators import Required, Length

from service import app, login_manager, address_utils


REGISTER_TITLE_API = app.config['REGISTER_TITLE_API']
UNAUTHORISED_WORDING = Markup('There was an error with your Username/Password '
                              'combination. If this problem persists please '
                              'contact us at <br/>'
                              'digital-register-feedback@'
                              'digital.landregistry.gov.uk'
                              )
GOOGLE_ANALYTICS_API_KEY = app.config['GOOGLE_ANALYTICS_API_KEY']
TITLE_NUMBER_REGEX = '^([A-Z]{0,3}[1-9][0-9]{0,5}|[0-9]{1,6}[ZT])$'
NOF_SECS_BETWEEN_LOGINS = 1
LOGGER = logging.getLogger(__name__)


class User():

    def __init__(self, username):
        self.user_id = username

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class LoginApiClient():

    def __init__(self, login_api_url):
        self.authentication_endpoint_url = '{}user/authenticate'.format(
            login_api_url)

    def authenticate_user(self, username, password):
        user_dict = {"user_id": username, "password": password}
        request_dict = {"credentials": user_dict}
        request_json = json.dumps(request_dict)

        headers = {'content-type': 'application/json'}
        response = requests.post(
            self.authentication_endpoint_url,
            data=request_json,
            headers=headers)

        if response.status_code == 200:
            return True
        elif _is_invalid_credentials_response(response):
            return False
        else:
            msg_format = ("An error occurred when trying to authenticate user '{}'. "
                          "Login API response: (HTTP status: {}) '{}'")
            raise Exception(msg_format.format(username, response.status_code, response.text))


LOGIN_API_CLIENT = LoginApiClient(app.config['LOGIN_API'])


def sanitise_postcode(postcode_in):
    # We strip out the spaces - and reintroduce one four characters from end
    no_spaces = postcode_in.replace(' ', '')
    postcode = no_spaces[:len(no_spaces) - 3] + ' ' + no_spaces[-3:]
    return postcode


@app.errorhandler(Exception)
def handle_internal_server_error(e):
    LOGGER.error('An error occurred when processing a request', exc_info=e)
    # TODO: render custom Internal Server Error page instead or reraising
    abort(500)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html',
                           google_api_key=GOOGLE_ANALYTICS_API_KEY,
                           asset_path='../static/'
                           )


@app.route('/cookies', methods=['GET'])
def cookies():
    return render_template('cookies.html',
                           google_api_key=GOOGLE_ANALYTICS_API_KEY,
                           asset_path='../static/'
                           )


@app.route('/login', methods=['GET'])
def signin_page():
    return render_template(
        'display_login.html',
        asset_path='../static/',
        google_api_key=GOOGLE_ANALYTICS_API_KEY,
        form=SigninForm(csrf_enabled=_is_csrf_enabled())
    )


@app.route('/login', methods=['POST'])
def signin():
    form = SigninForm(csrf_enabled=_is_csrf_enabled())
    if not form.validate():
        # entered details from login form incorrectly so send back to same page
        # with form error messages
        return render_template(
            'display_login.html', asset_path='../static/', form=form)

    next_url = request.args.get('next', 'title-search')

    # form was valid
    username = form.username.data
    # form has correct details. Now need to check authorisation
    authorised = LOGIN_API_CLIENT.authenticate_user(
        username,
        form.password.data
    )

    if authorised:
        login_user(User(username))
        LOGGER.info('User {} logged in'.format(username))
        return redirect(next_url)

    # too many bad log-ins or not authorised
    if app.config.get('SLEEP_BETWEEN_LOGINS', True):
        time.sleep(NOF_SECS_BETWEEN_LOGINS)

    return render_template('display_login.html',
                           google_api_key=GOOGLE_ANALYTICS_API_KEY,
                           asset_path='../static/', form=form,
                           unauthorised=UNAUTHORISED_WORDING, next=next_url
                           )


@app.route('/titles/<title_ref>', methods=['GET'])
@login_required
def display_title(title_ref):
    # Check to see if the Title dict is in the session, else try to retrieve it
    title = session.pop('title', get_register_title(title_ref))
    if title:
        # If the title was found, display the page
        LOGGER.info(
            "VIEW REGISTER: Title number {0} was viewed by {1}".format(
                title_ref,
                current_user.get_id()))
        return render_template(
            'display_title.html',
            asset_path='../static/',
            title=title,
            google_api_key=GOOGLE_ANALYTICS_API_KEY
        )
    else:
        abort(404)


@app.route('/title-search', methods=['GET', 'POST'])
@app.route('/title-search/<search_term>', methods=['GET', 'POST'])
@login_required
def find_titles(search_term=''):
    if request.method == 'POST':
        search_term = request.form['search_term'].strip()
        if search_term:
            return redirect(url_for('find_titles', search_term=search_term))
        else:
            # display the initial search page
            return redirect(url_for('find_titles'))
    # GET request
    search_term = search_term.strip()
    if not search_term:
        # display the initial search page
        return render_template('search.html', asset_path='/static/',
                               google_api_key=GOOGLE_ANALYTICS_API_KEY, form=TitleSearchForm())
    # search for something
    LOGGER.info(
        "SEARCH REGISTER: '{0}' was searched by {1}".format(
            search_term,
            current_user.get_id()))
    # Determine search term type and preform search
    title_number_regex = re.compile(TITLE_NUMBER_REGEX)
    postcode_regex = re.compile(address_utils.BASIC_POSTCODE_REGEX)
    search_term = search_term.upper()
    # If it matches the title number regex...
    if title_number_regex.match(search_term):
        title = get_register_title(search_term)
        if title:
            # If the title exists store it in the session
            session['title'] = title
            # Redirect to the display_title method to display the digital
            # register
            return redirect(url_for('display_title', title_ref=search_term))
        else:
            # If title not found display 'no title found' screen
            return render_search_results([], search_term)
    # If it matches the postcode regex ...
    elif postcode_regex.match(search_term):
        # Short term fix to enable user to search with postcode without spaces
        postcode = sanitise_postcode(search_term)
        postcode_search_results = get_register_titles_via_postcode(postcode)
        return render_search_results(postcode_search_results, postcode)
    elif search_term:
        address_search_results = get_register_titles_via_address(search_term)
        return render_search_results(address_search_results, search_term)


def render_search_results(results, search_term):
    return render_template('search_results.html',
                           asset_path='../static/',
                           search_term=search_term,
                           google_api_key=GOOGLE_ANALYTICS_API_KEY,
                           results=results,
                           form=TitleSearchForm()
                           )


def _is_csrf_enabled():
    return app.config.get('DISABLE_CSRF_PREVENTION') != True


def get_register_title(title_ref):
    response = requests.get(
        '{}titles/{}'.format(REGISTER_TITLE_API, title_ref))
    title = format_display_json(response)
    return title


def get_register_titles_via_postcode(postcode):
    response = requests.get(
        REGISTER_TITLE_API + 'title_search_postcode/' + postcode)
    results = response.json()
    return results


def get_register_titles_via_address(address):
    response = requests.get(
        REGISTER_TITLE_API + 'title_search_address/' + address)
    results = response.json()
    return results


def format_display_json(api_response):
    if api_response:
        title_api = api_response.json()
        proprietors = format_proprietors(
            title_api['data']['proprietors'])
        address_lines = address_utils.get_address_lines(title_api['data']['address'])
        indexPolygon = get_property_address_index_polygon(
            title_api['geometry_data'])
        title = {
            # ASSUMPTION 1: All titles have a title number
            'number': title_api['title_number'],
            'last_changed': title_api['data'].get(
                'last_application_timestamp',
                'No data'
            ),
            'address_lines': address_lines,
            'proprietors': proprietors,
            'tenure': title_api['data'].get('tenure', 'No data'),
            'indexPolygon': indexPolygon
        }
        print(title)
        return title
    else:
        return None


def format_proprietors(proprietors_data):
    formatted_proprietors = []
    for proprietor in proprietors_data:
        name = proprietor.get('name') or ''
        addresses = proprietor.get('addresses') or []
        formatted_proprietor = {}
        # TODO: proprietor names have potentially a lot more fields to display
        if 'forename' in name and 'surname' in name:
            formatted_proprietor["name"] = name['forename'] + ' ' + name['surname']
        if 'non_private_individual_name' in name:
            formatted_proprietor["name"] = name['non_private_individual_name']
        formatted_proprietor["addresses"] = []
        for address in addresses:
            formatted_proprietor["addresses"] += [{
                "lines": address_utils.get_address_lines(address)
            }]
        formatted_proprietors += [formatted_proprietor]
    return formatted_proprietors


# This method attempts to retrieve the index polygon data for the entry
def get_property_address_index_polygon(geometry_data):
    indexPolygon = None
    if geometry_data and ('index' in geometry_data):
        indexPolygon = geometry_data['index']
    return indexPolygon


def _is_invalid_credentials_response(response):
    if response.status_code != 401:
        return False

    response_json = response.json()
    return response_json and response_json['error'] == 'Invalid credentials'


class SigninForm(Form):
    username = StringField(
        'username', [
            Required(
                message='Username is required'), Length(
                min=4, max=70, message='Username is incorrect')])
    password = PasswordField(
        'password', [
            Required(
                message='Password is required')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class TitleSearchForm(Form):
    # Form used for providing CSRF tokens for title search HTTP form
    pass


if _is_csrf_enabled():
    CsrfProtect(app)


def run_app():
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port)
