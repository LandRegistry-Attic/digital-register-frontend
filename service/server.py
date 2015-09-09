from datetime import datetime                                                                          # type: ignore
from flask import abort, make_response, Markup, redirect, render_template, request, Response, url_for  # type: ignore
from flask_login import login_user, login_required, current_user, logout_user                          # type: ignore
from flask_weasyprint import HTML, render_pdf                                                          # type: ignore
import json
import logging
import logging.config                                                                                  # type: ignore
import re
import time

from service import (address_utils, api_client, app, auditing, health_checker, login_api_client,
                     login_manager, title_formatter, title_utils)
from service.forms import TitleSearchForm, SigninForm


LOGIN_API_URL = app.config['LOGIN_API']
# TODO: move this to the template
UNAUTHORISED_WORDING = Markup('If this problem persists please contact us at '
                              '<a rel="external" href="mailto:digital-register-'
                              'feedback@digital.landregistry.gov.uk">'
                              'digital-register-feedback@digital.landregistry.gov.uk</a>.')
# TODO: move this to the template
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


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/health', methods=['GET'])
def healthcheck():
    errors = health_checker.perform_healthchecks()
    status, http_status = ('error', 500) if errors else ('ok', 200)

    response_body = {'status': status}

    if errors:
        response_body['errors'] = errors

    return Response(
        json.dumps(response_body),
        status=http_status,
        mimetype='application/json',
    )


@app.route('/cookies', methods=['GET'])
def cookies():
    return _cookies_page()


@app.route('/login', methods=['GET'])
def signin_page():
    user_id = current_user.get_id()
    if user_id:
        return redirect(url_for('find_titles_page'))
    else:
        return _login_page()


@app.route('/login', methods=['POST'])
def sign_in():
    form = SigninForm(csrf_enabled=_is_csrf_enabled())

    if not form.validate():
        # entered invalid login form details so send back to same page with form error messages
        return _login_page(form)
    else:
        return _process_valid_login_attempt(form)


@app.route('/logout', methods=['GET'])
def sign_out():
    user_id = current_user.get_id()

    if user_id:
        logout_user()
        auditing.audit('User {} logged out'.format(user_id))

    return redirect(url_for('sign_in'))


@app.route('/titles/<title_number>', methods=['GET'])
@login_required
def get_title(title_number):
    title = _get_register_title(title_number)

    if title:
        display_page_number = int(request.args.get('page', 1))
        search_term = request.args.get('search_term', title_number)
        breadcrumbs = _breadcumbs_for_title_details(title_number, search_term, display_page_number)
        show_pdf = _should_show_full_title_pdf()
        full_title_data = (
            api_client.get_official_copy_data(title_number) if _should_show_full_title_data() else None
        )

        auditing.audit("VIEW REGISTER: Title number {0} was viewed by '{1}'".format(
            title_number,
            current_user.get_id())
        )

        return _title_details_page(title, search_term, breadcrumbs, show_pdf, full_title_data)
    else:
        abort(404)


@app.route('/titles/<title_number>.pdf', methods=['GET'])
@login_required
def display_title_pdf(title_number):
    if not _should_show_full_title_pdf():
        abort(404)

    title = _get_register_title(title_number)
    if title:
        full_title_data = api_client.get_official_copy_data(title_number)
        if full_title_data:
            sub_registers = full_title_data.get('official_copy_data', {}).get('sub_registers')
            if sub_registers:
                publication_date = datetime(3001, 2, 3, 4, 5, 6)  # TODO: get real date
                html = render_template('full_title.html', title_number=title_number, title=title,
                                       publication_date=publication_date,
                                       sub_registers=sub_registers)

                return render_pdf(HTML(string=html))
    abort(404)


@app.route('/title-search', methods=['POST'])
@app.route('/title-search/<search_term>', methods=['POST'])
@login_required
def find_titles():
    display_page_number = int(request.args.get('page', 1))

    search_term = request.form['search_term'].strip()
    if search_term:
        return redirect(url_for('find_titles', search_term=search_term, page=display_page_number))
    else:
        # TODO: we should redirect to that page
        return _initial_search_page()


@app.route('/', methods=['GET'])
@app.route('/title-search', methods=['GET'])
@app.route('/title-search/<search_term>', methods=['GET'])
@login_required
def find_titles_page(search_term=''):
    display_page_number = int(request.args.get('page', 1))
    page_number = display_page_number - 1  # page_number is 0 indexed

    search_term = search_term.strip()
    if not search_term:
        return _initial_search_page()
    else:
        message_format = "SEARCH REGISTER: '{0}' was searched by '{1}'"
        auditing.audit(message_format.format(search_term, current_user.get_id()))
        return _get_address_search_response(search_term, page_number)


def _get_register_title(title_number):
    title = api_client.get_title(title_number)
    return title_formatter.format_display_json(title) if title else None


def _process_valid_login_attempt(form):
    username = form.username.data
    authorised = login_api_client.authenticate_user(username, form.password.data)

    if authorised:
        login_user(User(username))
        next_url = request.args.get('next', 'title-search')
        auditing.audit('User {} logged in'.format(username))
        return redirect(next_url)
    else:
        # too many bad log-ins or invalid credentials
        _introduce_wait_between_login_attempts()
        return _login_page(form, show_unauthorised_message=True)


def _get_address_search_response(search_term, page_number):
    search_term = search_term.upper()
    if _is_title_number(search_term):
        return _get_search_by_title_number_response(search_term, page_number)
    elif _is_postcode(search_term):
        return _get_search_by_postcode_response(search_term, page_number)
    else:
        return _get_search_by_address_response(search_term, page_number)


def _get_search_by_title_number_response(search_term, page_number):
    display_page_number = page_number + 1
    title_number = search_term
    title = _get_register_title(title_number)
    if title:
        # Redirect to the display_title method to display the digital register
        return redirect(url_for('get_title', title_number=title_number,
                                page_number=display_page_number, search_term=search_term))
    else:
        # If title not found display 'no title found' screen
        results = {'number_results': 0}
        return _search_results_page(results, search_term)


def _get_search_by_postcode_response(search_term, page_number):
    postcode = _normalise_postcode(search_term)
    postcode_search_results = api_client.get_titles_by_postcode(postcode, page_number)
    return _search_results_page(postcode_search_results, postcode)


def _get_search_by_address_response(search_term, page_number):
    address_search_results = api_client.get_titles_by_address(search_term, page_number)
    return _search_results_page(address_search_results, search_term)


def _is_title_number(search_term):
    return TITLE_NUMBER_REGEX.match(search_term)


def _is_postcode(search_term):
    return POSTCODE_REGEX.match(search_term)


def _is_csrf_enabled():
    return app.config.get('DISABLE_CSRF_PREVENTION') is not True


def _should_show_full_title_data():
    return app.config.get('SHOW_FULL_TITLE_DATA')


def _should_show_full_title_pdf():
    return app.config.get('SHOW_FULL_TITLE_PDF')


def _introduce_wait_between_login_attempts():
    if app.config.get('SLEEP_BETWEEN_LOGINS', True):
        time.sleep(NOF_SECS_BETWEEN_LOGINS)


def _breadcumbs_for_title_details(title_number, search_term, display_page_number):
    search_breadcrumb = {'text': 'Search the land and property register', 'url': url_for('find_titles')}
    results_breadcrumb = {'text': 'Search results', 'url': url_for('find_titles_page', search_term=search_term,
                                                                   page=display_page_number)}
    current_breadcrumb = {'current': 'Viewing {}'.format(title_number)}

    found_title_by_number = title_number.lower() == search_term.lower()

    if found_title_by_number:
        return [search_breadcrumb, current_breadcrumb]
    else:
        return [search_breadcrumb, results_breadcrumb, current_breadcrumb]


def _normalise_postcode(postcode_in):
    # We strip out the spaces - and reintroduce one four characters from end
    no_spaces = postcode_in.replace(' ', '')
    postcode = no_spaces[:len(no_spaces) - 3] + ' ' + no_spaces[-3:]
    return postcode


def _login_page(form=None, show_unauthorised_message=False, next_url=None):
    if not form:
        form = SigninForm(csrf_enabled=_is_csrf_enabled())

    return render_template(
        'display_login.html',
        form=form,
        username=current_user.get_id(),
        service_notice_html=app.config.get('SERVICE_NOTICE_HTML', None),
        unauthorised_title=UNAUTHORISED_TITLE if show_unauthorised_message else None,
        unauthorised_description=UNAUTHORISED_WORDING if show_unauthorised_message else None,
        next=next_url,
    )


def _title_details_page(title, search_term, breadcrumbs, show_pdf, full_title_data):
    return render_template(
        'display_title.html',
        title=title,
        username=current_user.get_id(),
        search_term=search_term,
        breadcrumbs=breadcrumbs,
        show_pdf=show_pdf,
        full_title_data=full_title_data,
        is_caution_title=title_utils.is_caution_title(title),
    )


def _initial_search_page():
    return render_template(
        'search.html',
        form=TitleSearchForm(),
        username=current_user.get_id(),
    )


def _search_results_page(results, search_term):
    return render_template(
        'search_results.html',
        search_term=search_term,
        results=results,
        form=TitleSearchForm(),
        username=current_user.get_id(),
        breadcrumbs=[
            {'text': 'Search the land and property register', 'url': url_for('find_titles')},
            {'current': 'Search results'}
        ]
    )


def _cookies_page():
    return render_template('cookies.html', username=current_user.get_id())
