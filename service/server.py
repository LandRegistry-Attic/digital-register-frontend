#!/usr/bin/env python
import json
from flask import abort, render_template, request, redirect, url_for, session
from flask import Markup
from flask_login import login_user, login_required, current_user, logout_user
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
UNAUTHORISED_WORDING = Markup('If this problem persists please contact us at '
                              '<a rel="external" href="mailto:digital-register-'
                              'feedback@digital.landregistry.gov.uk">'
                              'digital-register-feedback@digital.landregistry.gov.uk</a>.')
UNAUTHORISED_TITLE = Markup('There was an error with your Username/Password combination.')
TITLE_NUMBER_REGEX = re.compile('^([A-Z]{0,3}[1-9][0-9]{0,5}|[0-9]{1,6}[ZT])$')
POSTCODE_REGEX = re.compile(address_utils.BASIC_POSTCODE_REGEX)
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
        user_dict = {'user_id': username, 'password': password}
        request_dict = {"credentials": user_dict}
        request_json = json.dumps(request_dict)

        headers = {'content-type': 'application/json'}
        response = requests.post(self.authentication_endpoint_url, data=request_json,
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


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/cookies', methods=['GET'])
def cookies():
    return render_template('cookies.html', username=current_user.get_id())


@app.route('/login', methods=['GET'])
def signin_page():
    user_id = current_user.get_id()
    if user_id:
        return redirect(url_for('find_titles_page'))
    else:
        service_interrupt_warning = app.config.get('SERVICE_INTERRUPT_WARNING', None)
        return render_template('display_login.html',
                               form=SigninForm(csrf_enabled=_is_csrf_enabled()),
                               username=current_user.get_id(),
                               service_interrupt_warning=service_interrupt_warning)


@app.route('/login', methods=['POST'])
def sign_in():
    form = SigninForm(csrf_enabled=_is_csrf_enabled())
    if not form.validate():
        # entered invalid login form details so send back to same page with form error messages
        return render_template('display_login.html', form=form, username=current_user.get_id())

    next_url = request.args.get('next', 'title-search')

    # form was valid
    username = form.username.data
    # form has correct details. Now need to check authorisation
    authorised = LOGIN_API_CLIENT.authenticate_user(username, form.password.data)

    if authorised:
        login_user(User(username))
        LOGGER.info('User {} logged in'.format(username))
        return redirect(next_url)

    # too many bad log-ins or not authorised
    if app.config.get('SLEEP_BETWEEN_LOGINS', True):
        time.sleep(NOF_SECS_BETWEEN_LOGINS)

    return render_template(
        'display_login.html',
        form=form,
        unauthorised_title=UNAUTHORISED_TITLE,
        unauthorised_description=UNAUTHORISED_WORDING,
        next=next_url
    )


@app.route('/logout', methods=['GET'])
def sign_out():
    user_id = current_user.get_id()

    if user_id:
        logout_user()
        LOGGER.info('User {} logged out'.format(user_id))

    return redirect(url_for('sign_in'))


@app.route('/titles/<title_ref>', methods=['GET'])
@login_required
def display_title(title_ref):

    title = get_register_title(title_ref)
    if title:
        # If the title was found, display the page
        LOGGER.info(
            "VIEW REGISTER: Title number {0} was viewed by '{1}'".format(title_ref,
                                                                         current_user.get_id()))
        return render_template('display_title.html', title=title,
                               username=current_user.get_id())
    else:
        abort(404)


@app.route('/title-search', methods=['POST'])
@app.route('/title-search/<search_term>', methods=['POST'])
@login_required
def find_titles():
    page_num = int(request.args.get('page', 1))
    search_term = request.form['search_term'].strip()
    if search_term:
        return redirect(url_for('find_titles', search_term=search_term, page=page_num))
    else:
        # TODO: we should probably redirect to that page
        return _render_initial_search_page()


@app.route('/', methods=['GET'])
@app.route('/title-search', methods=['GET'])
@app.route('/title-search/<search_term>', methods=['GET'])
@login_required
def find_titles_page(search_term=''):
    page_number = int(request.args.get('page', 1))

    search_term = search_term.strip()
    if not search_term:
        return _render_initial_search_page()
    else:
        LOGGER.info("SEARCH REGISTER: '{0}' was searched by '{1}'".format(search_term,
                                                                          current_user.get_id()))

        return _get_address_search_response(search_term, page_number)


def render_search_results(results, search_term, page_number):
    return render_template(
        'search_results.html',
        search_term=search_term,
        page_num=page_number,
        results=results,
        form=TitleSearchForm(),
        username=current_user.get_id(),
        breadcrumbs=[
            {"text": "Find a Title", "url": url_for('find_titles')},
            {"text": "Search results", "url": ""}
        ]
    )


def get_register_title(title_ref):
    response = requests.get('{}titles/{}'.format(REGISTER_TITLE_API, title_ref))
    title = format_display_json(response)
    return title


def get_register_titles_via_postcode(postcode, page_num):
    response = requests.get('{}title_search_postcode/{}'.format(REGISTER_TITLE_API, postcode),
                            params={'page': page_num})
    results = response.json()
    return results


def get_register_titles_via_address(address, page_num):
    response = requests.get('{}title_search_address/{}'.format(REGISTER_TITLE_API, address),
                            params={'page': page_num})
    results = response.json()
    return results


def format_display_json(api_response):
    if api_response:
        title_api = api_response.json()
        proprietors = format_proprietors(title_api['data']['proprietors'])
        address_lines = address_utils.get_address_lines(title_api['data']['address'])
        indexPolygon = get_property_address_index_polygon(title_api['geometry_data'])
        title = {
            'number': title_api['title_number'],
            'last_changed': title_api['data'].get('last_application_timestamp', 'No data'),
            'address_lines': address_lines,
            'proprietors': proprietors,
            'tenure': title_api['data'].get('tenure', 'No data'),
            'indexPolygon': indexPolygon
        }
        if 'lenders' in title_api['data']:
            lenders = format_proprietors(title_api['data']['lenders'])
            title['lenders'] = lenders
        if 'ppi_data' in title_api['data']:
            # Remove period from end of PPI text if present
            title['ppi_data'] = title_api['data']['ppi_data'].rstrip('.')
        return title
    else:
        return None


def format_proprietors(proprietors_data):
    formatted_proprietors = []
    for proprietor in proprietors_data:
        name = proprietor.get('name') or ''
        addresses = proprietor.get('addresses') or []
        formatted_proprietor = {}
        if 'name_information' in name:
            formatted_proprietor["name_information"] = ', ' + name['name_information']
        if 'name_supplimentary' in name:
            formatted_proprietor["name_supplimentary"] = ', ' + name['name_supplimentary']
        if 'charity_name' in name:
            charity_name = ' of '
            if name['charity_name'].endswith(")"):
                charity_name += '('
            charity_name += name['charity_name']
            formatted_proprietor["charity_name"] = charity_name
        if 'trading_name' in name:
            formatted_proprietor["trading_name"] = ' trading as ' + name['trading_name']
        if 'forename' in name or 'surname' in name:
            formatted_proprietor["name"] = format_pi_name(name)
        if 'non_private_individual_name' in name:
            formatted_proprietor["name"] = name['non_private_individual_name']
            if 'company_reg_num' in name:
                formatted_proprietor["co_reg_no"] = 'Company registration number '\
                                                    + name['company_reg_num']
            if 'country_incorporation' in name:
                formatted_proprietor["country_incorporation"] = 'incorporated in '\
                                                                + name['country_incorporation']
        formatted_proprietor["addresses"] = []
        for address in addresses:
            formatted_proprietor["addresses"] += [{
                "lines": address_utils.get_address_lines(address)
            }]
        formatted_proprietors += [formatted_proprietor]
    return formatted_proprietors


def format_pi_name(name):
    name_list = []
    if 'title' in name:
        name_list.append(name['title'])
    if 'forename' in name:
        name_list.append(name['forename'])
    if 'surname' in name:
        name_list.append(name['surname'])
    formatted_name = ' '.join(name_list)
    if 'decoration' in name:
        formatted_name += ', ' + name['decoration']
    return formatted_name


# This method attempts to retrieve the index polygon data for the entry
def get_property_address_index_polygon(geometry_data):
    index_polygon = None
    if geometry_data and ('index' in geometry_data):
        index_polygon = geometry_data['index']
    return index_polygon


def _get_address_search_response(search_term, page_number):
    search_term = search_term.upper()
    if _is_title_number(search_term):
        return _get_search_by_title_number_response(search_term, page_number)
    elif _is_postcode(search_term):
        return _get_search_by_postcode_response(search_term, page_number)
    else:
        return _get_search_by_address_response(search_term, page_number)


def _render_initial_search_page():
    return render_template(
        'search.html',
        form=TitleSearchForm(),
        username=current_user.get_id(),
        )


def _get_search_by_title_number_response(search_term, page_number):
    title_ref = search_term
    title = get_register_title(title_ref)
    if title:
        # Redirect to the display_title method to display the digital register
        return redirect(url_for('display_title', title_ref=title_ref))
    else:
        # If title not found display 'no title found' screen
        return render_search_results([], search_term, page_number)


def _get_search_by_postcode_response(search_term, page_number):
    postcode = sanitise_postcode(search_term)
    postcode_search_results = get_register_titles_via_postcode(postcode, page_number)
    return render_search_results(postcode_search_results, postcode, page_number)


def _get_search_by_address_response(search_term, page_num):
    address_search_results = get_register_titles_via_address(search_term, page_num)
    return render_search_results(address_search_results, search_term, page_num)


def _is_title_number(search_term):
    return TITLE_NUMBER_REGEX.match(search_term)


def _is_postcode(search_term):
    return POSTCODE_REGEX.match(search_term)


def _is_invalid_credentials_response(response):
    if response.status_code != 401:
        return False

    response_json = response.json()
    return response_json and response_json['error'] == 'Invalid credentials'


class SigninForm(Form):
    username = StringField('username', [Required(message='Username is required'),
                                        Length(min=4, max=70, message='Username is incorrect')])
    password = PasswordField('password', [Required(message='Password is required')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class TitleSearchForm(Form):
    search_term = StringField('search_term',
                              [Required(message='Search term is required'),
                               Length(min=3, max=70, message='Search term is too short/long')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


def _is_csrf_enabled():
    return app.config.get('DISABLE_CSRF_PREVENTION') is not True


def run_app():
    CsrfProtect(app)
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port)
