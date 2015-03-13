#!/usr/bin/env python
from collections import Counter
import json
from flask import abort, render_template, request, redirect, url_for, session
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
UNAUTHORISED_WORDING = 'There was an error with your Username/Password combination. Please try again'
GOOGLE_ANALYTICS_API_KEY = app.config['GOOGLE_ANALYTICS_API_KEY']
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
        self.authentication_endpoint_url = '{}user/authenticate'.format(login_api_url)

    def authenticate_user(self, username, password):
        user_dict = {"user_id": username, "password": password}
        request_dict = {"credentials": user_dict}
        request_json = json.dumps(request_dict)

        headers = {'content-type': 'application/json'}
        response = requests.post(self.authentication_endpoint_url, data=request_json, headers=headers)
        return response.status_code == 200


LOGIN_API_CLIENT = LoginApiClient(app.config['LOGIN_API'])


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', asset_path='../static/')


@app.route('/login', methods=['GET'])
def signin_page():
    return render_template(
        'display_login.html',
        asset_path='../static/',
        form=SigninForm(csrf_enabled=_is_csrf_enabled())
    )


BAD_LOGIN_COUNTER = Counter()
MAX_LOGIN_ATTEMPTS = 10
NOF_SECS_BETWEEN_LOGINS = 2


@app.route('/login', methods=['POST'])
def signin():
    form = SigninForm(csrf_enabled=_is_csrf_enabled())
    if not form.validate():
        # entered details from login form incorrectly so send back to same page with form error messages
        return render_template('display_login.html', asset_path='../static/', form=form)

    next_url = request.args.get('next', 'title-search')

    # form was valid
    username = form.username.data
    too_many_bad_logins = BAD_LOGIN_COUNTER[username] > MAX_LOGIN_ATTEMPTS
    if not too_many_bad_logins:
        # form has correct details. Now need to check authorisation
        authorised = LOGIN_API_CLIENT.authenticate_user(username, form.password.data)

        if authorised:
            del BAD_LOGIN_COUNTER[username]
            login_user(User(username))
            LOGGER.info('User {} logged in'.format(username))
            return redirect(next_url)

    # too many bad log-ins or not authorised
    time.sleep(NOF_SECS_BETWEEN_LOGINS)
    BAD_LOGIN_COUNTER.update([username])
    log_msg = 'Too many bad logins' if too_many_bad_logins else 'Invalid credentials used'
    nof_attempts = BAD_LOGIN_COUNTER[username]
    LOGGER.info('{}. username: {}, attempt: {}.'.format(log_msg, username,
                                                        nof_attempts))

    return render_template('display_login.html', asset_path='../static/', form=form,
                           unauthorised=UNAUTHORISED_WORDING, next=next_url)


@app.route('/titles/<title_ref>', methods=['GET'])
@login_required
def display_title(title_ref):
    # Check to see if the Title dict is in the session, else try to retrieve it
    title = session.pop('title', get_register_title(title_ref))
    if title:
        # If the title was found, display the page
        LOGGER.info("VIEW REGISTER: Title number {0} was viewed by {1}".format(title_ref, current_user.get_id()))
        return render_template('display_title.html', asset_path = '../static/', title=title, google_api_key=GOOGLE_ANALYTICS_API_KEY)
    else:
        abort(404)


@app.route('/title-search/', methods=['GET', 'POST'])
@login_required
def find_titles():
    # TODO: make this method use a WTF form, just like signin()
    if request.method == "POST":
        search_term = request.form['search_term']
        LOGGER.info("SEARCH REGISTER: {0} was searched by {1}".format(search_term, current_user.get_id()))
        # Determine search term type and preform search
        title_number_regex = re.compile("^([A-Z]{0,3}[1-9][0-9]{0,5}|[0-9]{1,6}[ZT])$")
        postcode_regex = re.compile("(GIR 0AA)|((([A-Z-[QVX]][0-9][0-9]?)|(([A-Z-[QVX]][A-Z-[IJZ]][0-9][0-9]?)|(([A-Z-[QVX]][0-9][A-HJKSTUW])|([A-Z-[QVX]][A-Z-[IJZ]][0-9][ABEHMNPRVWXY])))) [0-9][A-Z-[CIKMOV]]{2})")
        # If it matches the title number regex...
        print(search_term)
        #TODO Postcode search term is not be recognised
        if title_number_regex.match(search_term.upper()):
            title = get_register_title(search_term.upper())
            if title:
                # If the title exists store it in the session
                session['title'] = title
                # Redirect to the display_title method to display the digital register
                return redirect(url_for('display_title', title_ref=search_term.upper()))
            else:
                # If title not found display 'no title found' screen
                return render_template('no_title_number_results.html', asset_path = '../static/', search_term=search_term, google_api_key=google_analytics_api_key)
        # If it matches the postcode regex ...
        elif postcode_regex.match(search_term.upper()):
            postcode_search_results = get_register_title_via_postcode(search_term.upper())
            if postcode_search_results:
                # If there are results store them in the session
                session['postcode_search_results'] = postcode_search_results
                # Redirect to the results page to display the results
                return redirect(url_for('display_postcode_search_results'))
        else:
            # If search value doesn't match, return no results found screen
            return render_template('no_title_number_results.html', asset_path = '../static/', search_term=search_term, google_api_key=google_analytics_api_key)
    else:
        # If not search value enter or a GET request, display the search page
        return render_template('search.html', asset_path = '../static/',
            google_api_key=GOOGLE_ANALYTICS_API_KEY, form=TitleSearchForm())


def _is_csrf_enabled():
    return app.config.get('DISABLE_CSRF_PREVENTION') != True


@app.route('/title-search/results', methods=['GET'])
def display_postcode_search_results():
    postcode_search_result = session.pop('postcode_search_result', get_register_title(title_ref))


def get_register_title(title_ref):
    response = requests.get(REGISTER_TITLE_API+'titles/'+title_ref)
    title = format_display_json(response)
    return title

def get_register_title_via_postcode(postcode):
    response = requests.get(register_title_api+'title_search_postcode/'+postcode)
    #TODO: actually sort out a response
    results = response
    return results

def format_display_json(api_response):
    if api_response:
        title_api = api_response.json()
        proprietor_names = get_proprietor_names(title_api['data']['proprietors'])
        address_lines = get_address_lines(title_api['data']['address'])
        indexPolygon = get_property_address_index_polygon(title_api['geometry_data'])
        title = {
            #ASSUMPTION 1: All titles have a title number
            'number': title_api['title_number'],
            'last_changed': title_api['data'].get('last_application_timestamp', 'No data'),
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
        #TODO: decide which of the following fields we want to display
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
    if 'sub_building_description' in address_data and 'sub_building_no' in address_data:
        lines.append("{0} {1}".format(address_data['sub_building_description'], address_data['sub_building_no']))
    elif 'sub_building_description' in address_data:
        lines.append(address_data['sub_building_description'])
    elif 'sub_building_no' in address_data:
        lines.append(address_data['sub_building_no'])
    return lines


def get_street_name_lines(address_data):
    lines = []
    street_name_string = ""
    if 'house_no' in address_data or 'house_alpha' in address_data:
        street_name_string+="{0}{1}".format(address_data.get('house_no', ''), address_data.get('house_alpha', ''))
    if 'secondary_house_no' in address_data or 'secondary_house_alpha' in address_data:
        secondary_string = "{0}{1}".format(address_data.get('secondary_house_no', ''), address_data.get('secondary_house_alpha', ''))
        if street_name_string:
            street_name_string+="-{0}".format(secondary_string)
        else:
            street_name_string+=secondary_string
    if 'street_name' in address_data:
        street_name = address_data['street_name']
        if street_name_string:
            street_name_string+=" {0}".format(street_name)
        else:
            street_name_string+=street_name
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
    return non_empty_lines


# This method attempts to retrieve the index polygon data for the entry
def get_property_address_index_polygon(geometry_data):
    indexPolygon = None
    if geometry_data and ('index' in geometry_data):
        indexPolygon = geometry_data['index']
    return indexPolygon


class SigninForm(Form):
    username = StringField('username', [Required(message='Username is required'), Length(min=4, max=70, message='Username is incorrect')])
    password = PasswordField('password', [Required(message='Password is required')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class TitleSearchForm(Form):
    # Form used for providing CSRF tokens for title search HTTP form
    pass


def run_app():
    CsrfProtect(app)
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    run_app()
