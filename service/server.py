#!/usr/bin/env python
from service import app
import os
from flask import Flask, abort, render_template, request, redirect, flash, url_for, session
import requests
import re

register_title_api = app.config['REGISTER_TITLE_API']

# TODO Create a proper secret key and store it securely
app.secret_key = 'a_secret_key'

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', asset_path = '../static/')

@app.route('/titles/<title_ref>', methods=['GET'])
def display_title(title_ref):
    # Check to see if the Title dict is in the session, else try to retrieve it
    title = session.pop('title', get_register_title(title_ref))
    if title:
        # If the title was found, display the page
        return render_template('display_title.html', asset_path = '../static/', title=title)
    else:
        abort(404)

@app.route('/title-search/', methods=['GET', 'POST'])
def find_titles():
    if request.method == "POST" and request.form['search_term']:
        search_term = request.form['search_term']
        # Determine search term type and preform search
        title_number_regex = re.compile("^([A-Z]{0,3}[1-9][0-9]{0,5}|[0-9]{1,6}[ZT])$")
        if title_number_regex.match(search_term.upper()):
            title = get_register_title(search_term.upper())
            if title:
                # If the title exists store it in the session
                session['title'] = title
                # Redirect to the display_title method to display the digital register
                return redirect(url_for('display_title', title_ref=search_term.upper()))
            else:
                # If title not found display 'no title found' screen
                return render_template('no_title_number_results.html', asset_path = '../static/', search_term=search_term)
        else:
            # If the search value was not in an expected format, return to search screen with error message
            flash('Search value not in a recognised format')
            return render_template('search.html', asset_path = '../static/', search_term=search_term)
    else:
        # If not search value enter or a GET request, display the search page
        return render_template('search.html', asset_path = '../static/')

def get_register_title(title_ref):
    response = requests.get(register_title_api+'titles/'+title_ref)
    title = format_display_json(response)
    return title

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

#This method attempts to retrieve the index polygon data for the entry
def get_property_address_index_polygon(geometry_data):
    indexPolygon = None
    if geometry_data and ('index' in geometry_data):
        indexPolygon = geometry_data['index']
    return indexPolygon

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port, debug=True)
