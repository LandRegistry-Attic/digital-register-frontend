#!/usr/bin/env python
from flask_login import login_user, login_required, current_user
from service import app, login_manager
import os
from flask import Flask, abort, render_template, request, redirect
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import Required
import requests
import logging
import logging.config

register_title_api = app.config['REGISTER_TITLE_API']
login_api = app.config['LOGIN_API']
login_json = '{{"credentials":{{"user_id":"{}","password":"{}"}}}}'
forward_slash = '/'
unauthorised_wording = 'There was an error with your Username/Password combination. Please try again'

LOGGER = logging.getLogger(__name__)

#This method attempts to retrieve the index polygon data for the entry
def get_property_address_index_polygon(geometry_data):
    indexPolygon = None
    if geometry_data and ('index' in geometry_data):
        indexPolygon = geometry_data['index']
    return indexPolygon


class User():
    def __init__(self, username):
        self.userid = username

    def get_id(self):
        return self.userid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', asset_path='../static/')

@app.route('/login', methods=['GET'])
def signin_page():
    # csrf_enabled = False for development environment only
    return render_template('display_login.html', asset_path='../static/', form=SigninForm(csrf_enabled=False))

@app.route('/login', methods=['POST'])
def signin():
    form = SigninForm(csrf_enabled=False)
    # need to record the URL user was trying to hit before being redirected to login page
    redirection_url = request.args.get('next') or 'search'
    redirection_url = redirection_url.replace(forward_slash, '')
    if not form.validate():
        # entered details from login form incorrect so redirect back to same page with error messages
        return render_template('display_login.html', asset_path='../static/', next=redirection_url, form=form)
    else:
        username = form.username.data
        # form has correct details. Now need to check authorisation
        authorised = get_login_auth(username, form.password.data)
        if authorised:
            login_user(User(username))
            LOGGER.info('User {} logged in'.format(username))
            return redirect(redirection_url)
        else:
            return render_template('display_login.html', asset_path='../static/', form=form, 
                                   unauthorised=unauthorised_wording, next=redirection_url)


def get_login_auth(username, password):
    login_endpoint = login_api + 'user/authenticate'
    formatted_json = login_json.format(username, password)
    headers = {'content-type': 'application/json'}
    response = requests.post(login_endpoint, data=formatted_json, headers=headers)
    authorised = False
    if response.status_code == 200:
        authorised = True
    return authorised

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return 'hello {}'.format(current_user.get_id())

@app.route('/titles/<title_ref>', methods=['GET'])
@login_required
def display_title(title_ref):
    api_response = get_register_title(title_ref)
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
        return render_template('display_title.html', asset_path='../static/', title=title)
    else:
        abort(404)


def get_register_title(title_ref):
    response = requests.get(register_title_api+'titles/'+title_ref)
    return response


def get_proprietor_names(proprietors_data):
    proprietor_names = []
    for proprietor in proprietors_data:
        name = proprietor['name']
        #ASSUMPTION 2: all proprietors have a name entry
        #ASSUMPTION 3: all proprietor names have either forename/surname or non_private_individual name
        if 'forename' in name and 'surname' in name:
            proprietor_names += [{
                "name": name['forename'] + ' ' + name['surname']
            }]
        if 'non_private_individual_name' in name:
            proprietor_names += [{
                "name": name['non_private_individual_name']
            }]
    return proprietor_names


def get_address_lines(address_data):
    address_lines = []
    #ASSUMPTION 4: all addresses are only in the house_no, street_name, town and postcode fields
    if address_data:
        first_line_address = ' '.join([address_data[k] for k in ['house_no', 'street_name'] if address_data.get(k, None)])
        all_address_lines = [
            first_line_address,
            address_data.get('town', ''),
            address_data.get('postcode', '')
        ]
        address_lines = [line for line in all_address_lines if line]
    return address_lines


class SigninForm(Form):
    username = StringField('username', [Required(message='Username is required')])
    password = PasswordField('password', [Required(message='Password is required')])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port, debug=True)
