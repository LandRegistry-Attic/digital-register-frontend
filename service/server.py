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

from service import app, login_manager

REGISTER_TITLE_API = app.config['REGISTER_TITLE_API']
UNAUTHORISED_WORDING = Markup('There was an error with your Username/Password '
                              'combination. If this problem persists please '
                              'contact us at <br/>'
                              'digital-register-feedback@'
                              'digital.landregistry.gov.uk'
                              )
GOOGLE_ANALYTICS_API_KEY = app.config['GOOGLE_ANALYTICS_API_KEY']
TITLE_NUMBER_REGEX = '^([A-Z]{0,3}[1-9][0-9]{0,5}|[0-9]{1,6}[ZT])$'
BASIC_POSTCODE_REGEX = '^[A-Z]{1,2}[0-9R][0-9A-Z]? ?[0-9][A-Z]{2}$'
BASIC_POSTCODE_WITH_SURROUNDING_GROUPS_REGEX = (
    r'(?P<leading_text>.*\b)\s?'
    r'(?P<postcode>[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}\b)\s?'
    r'(?P<trailing_text>.*)'
)
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


@app.route('/title-search/', methods=['GET', 'POST'])
@login_required
def find_titles():
    # TODO: make this method use a WTF form, just like signin()
    if request.method == "POST":
        search_term = request.form['search_term'].strip()
        LOGGER.info(
            "SEARCH REGISTER: '{0}' was searched by {1}".format(
                search_term,
                current_user.get_id()))
        # Determine search term type and preform search
        title_number_regex = re.compile(TITLE_NUMBER_REGEX)
        postcode_regex = re.compile(BASIC_POSTCODE_REGEX)
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
        else:
            address_search_results = get_register_titles_via_address(search_term)
            return render_search_results(address_search_results, search_term)
    # If not search value enter or a GET request, display the search page
    return render_template(
        'search.html',
        asset_path='../static/',
        google_api_key=GOOGLE_ANALYTICS_API_KEY,
        form=TitleSearchForm()
    )


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
        proprietor_names = get_proprietor_names(
            title_api['data']['proprietors'])
        address_lines = get_address_lines(title_api['data']['address'])
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
            'proprietors': proprietor_names,
            'tenure': title_api['data'].get('tenure', 'No data'),
            'indexPolygon': indexPolygon
        }
        return title
    else:
        return None


def get_proprietor_names(proprietors_data):
    proprietor_names = []
    for proprietor in proprietors_data:
        name = proprietor['name']
        # TODO: decide which of the following fields we want to display
        # company_reg_num
        # country_incorporation
        # company_location
        # local_authority_area
        # name_supplimentary
        # charity_name
        # trust_format
        # name_information
        if 'forename' in name and 'surname' in name:
            proprietor_names += [{
                "name": name['forename'] + ' ' + name['surname']
            }]
        if 'non_private_individual_name' in name:
            proprietor_names += [{
                "name": name['non_private_individual_name']
            }]
    return proprietor_names


def get_building_description_lines(address_data):
    lines = []
    if ('sub_building_description' in address_data and
            'sub_building_no' in address_data):
        lines.append(
            "{0} {1}".format(
                address_data['sub_building_description'],
                address_data['sub_building_no']))
    elif 'sub_building_description' in address_data:
        lines.append(address_data['sub_building_description'])
    elif 'sub_building_no' in address_data:
        lines.append(address_data['sub_building_no'])
    return lines


def get_street_name_lines(address_data):
    lines = []
    street_name_string = ""
    if 'house_no' in address_data or 'house_alpha' in address_data:
        street_name_string += "{0}{1}".format(
            address_data.get(
                'house_no', ''), address_data.get(
                'house_alpha', ''))
    if ('secondary_house_no' in address_data or
            'secondary_house_alpha' in address_data):
        secondary_string = "{0}{1}".format(
            address_data.get(
                'secondary_house_no', ''), address_data.get(
                'secondary_house_alpha', ''))
        if street_name_string:
            street_name_string += "-{0}".format(secondary_string)
        else:
            street_name_string += secondary_string
    if 'street_name' in address_data:
        street_name = address_data['street_name']
        if street_name_string:
            street_name_string += " {0}".format(street_name)
        else:
            street_name_string += street_name
    if street_name_string:
        lines.append(street_name_string)
    return lines


def get_address_lines(address_data):
    lines = []
    if address_data:
        lines.append(address_data.get('leading_info', None))
        lines = get_building_description_lines(address_data)
        lines.append(address_data.get('house_description', None))
        lines += get_street_name_lines(address_data)
        lines.append(address_data.get('street_name_2', None))
        lines.append(address_data.get('local_name', None))
        lines.append(address_data.get('local_name_2', None))
        lines.append(address_data.get('town', None))
        lines.append(address_data.get('postcode', None))
        lines.append(address_data.get('trail_info', None))
    non_empty_lines = [x for x in lines if x is not None]
    # If the JSON doesn't contain the individual fields non_empty_lines will be
    # empty
    # Check if this is the case and if their is an address_string
    if not non_empty_lines and address_data and address_data.get(
            'address_string'):
        non_empty_lines = format_address_string(
            address_data.get('address_string'))
    return non_empty_lines


def format_address_string(address_string):
    # remove brackets and split the address string on commas
    address_lines = re.sub('[\(\)]', '', address_string).split(', ')
    result = address_lines[:]
    # Strip leading and trailing whitespace and see if the last line is a just
    # a postcode
    last_line = address_lines[-1].strip()
    if not re.search(BASIC_POSTCODE_REGEX, last_line):
        # If not, remove the line from address_lines, splt out the postcode and
        # any preceeding text and trailing text and add them to address_lines
        # as separate lines (if they exist)
        del(address_lines[-1])
        matches = re.match(
            BASIC_POSTCODE_WITH_SURROUNDING_GROUPS_REGEX,
            last_line)
        if matches:
            if matches.group('leading_text') and len(
                    matches.group('leading_text').strip()) > 0:
                address_lines.append(matches.group('leading_text').strip())
            address_lines.append(matches.group('postcode').strip())
            if matches.group('trailing_text') and len(
                    matches.group('trailing_text').strip()) > 0:
                address_lines.append(matches.group('trailing_text').strip())
            result = address_lines
    return result


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


def run_app():
    CsrfProtect(app)
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    run_app()
