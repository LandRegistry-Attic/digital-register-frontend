import json
import logging
import logging.config                                                                                  # type: ignore
import re
import time
from datetime import datetime                                                                          # type: ignore
from flask import abort, Markup, redirect, render_template, request, Response, url_for  # type: ignore
from flask_login import login_user, login_required, current_user, logout_user                          # type: ignore
from flask_weasyprint import HTML, render_pdf                                                          # type: ignore
from service import (address_utils, api_client, app, auditing, health_checker, login_api_client,
                     login_manager, title_formatter, title_utils, search_request_interface)
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


@app.route('/', methods=['GET'])
@app.route('/search', methods=['GET'])
def app_start():
    """ DM US107
    App entry point
    - show search page
    """
    username = _username_from_header(request)
    return render_template(
        'search.html',
        form=TitleSearchForm(),
        username=username,
        )

@app.route('/confirm-selection/<title_number>/<search_term>', methods=['GET'])
def confirm_selection(title_number, search_term):
    """ Let user confirm a selection - i.e., place an order. """

    title = _get_register_title(request.args.get('title', title_number))

    params = dict()
    params['title'] = title
    params['title_number'] = title_number
    params['search_term'] = request.args.get('search_term', search_term)
    params['display_page_number'] = 1
    params['products_string'] = "unused"
    params['price'] = app.config['TITLE_REGISTER_SUMMARY_PRICE']
    params['post_confirmation_url'] = app.config['POST_CONFIRMATION_URL']

    # Use DB API to add a record in T_PS_SRCH_REQ table, to be updated later if/when payment is made.
    property_search_purch_addr = title['address_lines']

    # Create DB record
    try:
        timestamp = search_request_interface.insert(title_number, params['price'], property_search_purch_addr)
    except Exception as e:
        # TODO: Should have a log call here.
        abort(500)

    # TODO: change the fixed values of 'cartid', 'mc_purchasetype' & 'mc_searchtype' to DRV search-related ones.
    # User-related WorldPay parameters.
    worldpay_params = dict()
    worldpay_params['cartid'] = '0001444208589806RhrHOvIFk6liOWwHE7bKfy'    # [Could be session id. + user id. perhaps]
    worldpay_params['amount'] = params['price']
    worldpay_params['mc_titlenumber'] = title_number
    worldpay_params['mc_timestamp'] = timestamp
    worldpay_params['mc_purchasetype'] = 'registerOnly'
    worldpay_params['mc_searchtype'] = 'D'

    # Last changed date - modified to remove colon in UTC offset, which python
    # datetime.strptime() doesn't like >>>

    datestring = params['title']['last_changed']
    if len(datestring) == 25:
        if datestring[22] == ':':
            l = list(datestring)
            del(l[22])
            datestring = "".join(l)

    dt_obj = datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S%z")
    params['last_changed_datestring'] = \
        "%d %s %d" % (dt_obj.day, dt_obj.strftime("%B"), dt_obj.year)
    params['last_changed_timestring'] = \
        "%s:%s:%s" % ('{:02d}'.format(dt_obj.hour),
                      '{:02d}'.format(dt_obj.minute),
                      '{:02d}'.format(dt_obj.second))

    return render_template('confirm_selection.html', params=params, worldpay_params=worldpay_params)


@app.route('/spinner-page/', methods=['POST'])
def spinner_page():
    """
    "Inform the user we're about to re-direct them to Worldpay to pay for their purchase".
    """


    return render_template('spinner-page.html')


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


@app.route('/titles/<title_number>', methods=['GET'])
@login_required
def get_title(title_number):
    title = _get_register_title(title_number)

    if title:
        display_page_number = int(request.args.get('page') or 1)
        search_term = request.args.get('search_term', title_number)
        breadcrumbs = _breadcumbs_for_title_details(title_number, search_term, display_page_number)
        show_pdf = _should_show_full_title_pdf()
        full_title_data = (
            api_client.get_official_copy_data(title_number) if _should_show_full_title_data() else None
        )

        full_title_data = _strip_delimiters(full_title_data)

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
        full_title_data = _strip_delimiters(full_title_data)
        if full_title_data:
            sub_registers = full_title_data.get('official_copy_data', {}).get('sub_registers')
            if sub_registers:
                html = _create_pdf_template(sub_registers, title, title_number)
                return render_pdf(HTML(string=html))
    abort(404)


@app.route('/title-search', methods=['POST'])
@app.route('/title-search/<search_term>', methods=['POST'])
def find_titles():
    display_page_number = int(request.args.get('page') or 1)

    search_term = request.form['search_term'].strip()
    if search_term:
        return redirect(url_for('find_titles', search_term=search_term, page=display_page_number))
    else:
        # TODO: we should redirect to that page
        return _initial_search_page(request)


# @app.route('/', methods=['GET'])
@app.route('/title-search', methods=['GET'])
@app.route('/title-search/<search_term>', methods=['GET'])
def find_titles_page(search_term=''):
    display_page_number = int(request.args.get('page') or 1)
    page_number = display_page_number - 1  # page_number is 0 indexed

    search_term = search_term.strip()
    if not search_term:
        return _initial_search_page(request)
    else:
        message_format = "SEARCH REGISTER: '{0}' was searched by '{1}'"
        auditing.audit(message_format.format(search_term, current_user.get_id()))
        return _get_address_search_response(search_term, page_number)


@app.route('/property-result/<title_number>', methods=['GET'])
@login_required
def individual_property_result(title_number):
    title = _get_register_title(title_number)

    if title:
        display_page_number = int(request.args.get('page') or 1)
        search_term = request.args.get('search_term', title_number)
        breadcrumbs = _breadcumbs_for_title_details(title_number, search_term, display_page_number)

        return _individual_property_result(title, display_page_number, search_term, breadcrumbs)
    else:
        abort(404)


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


def _individual_property_result(title, display_page_number, search_term, breadcrumbs):
    return render_template(
        'property_result.html',
        title=title,
        display_page_number=display_page_number,
        search_term=search_term,
        breadcrumbs=breadcrumbs,
    )


def _initial_search_page(request):
    username = _username_from_header(request)
    return render_template(
        'search.html',
        form=TitleSearchForm(),
        username=username,
        #username=current_user.get_id(),
    )


def _search_results_page(results, search_term):
    username = _username_from_header(request)
    return render_template(
        'search_results.html',
        search_term=search_term,
        results=results,
        form=TitleSearchForm(),
        username=username,
        breadcrumbs=[
            {'text': 'Search the land and property register', 'url': url_for('find_titles')},
            {'current': 'Search results'}
        ]
    )


def _cookies_page():
    return render_template('cookies.html', username=current_user.get_id())


def _create_string_date_only(datetoconvert):
    # converts to example : 12 August 2014
    date = datetoconvert.strftime('%-d %B %Y')
    return date


def _create_string_date_and_time(datetoconvert):
    # converts to example : 12 August 2014 12:34:06
    date = datetoconvert.strftime('%-d %B %Y at %H:%M:%S')
    return date


def _create_pdf_template(sub_registers, title, title_number):

    # TODO use real date - this is reliant on new functionality to check the daylist
    last_entry_date = _create_string_date_and_time(datetime(3001, 2, 3, 4, 5, 6))
    issued_date = _create_string_date_only(datetime.now())
    if title.get('edition_date'):
        edition_date = _create_string_date_only(datetime.strptime(title.get('edition_date'), "%Y-%m-%d"))
    else:
        edition_date = "No date given"

    districts = title.get('districts')

    class_of_title = title.get('class_of_title')
    # need to check for caution title as we don't display Class of title for them
    is_caution = title.get('is_caution_title') is True

    return render_template('full_title.html', title_number=title_number, title=title,
                           last_entry_date=last_entry_date,
                           issued_date=issued_date,
                           edition_date=edition_date,
                           class_of_title=class_of_title,
                           sub_registers=sub_registers,
                           is_caution=is_caution,
                           districts=districts)


def _strip_delimiters(json_in):
    """
    Remove all delimiters and not notes from json
    """
    json_out = json_in
    for i, sub_register in enumerate(json_in['official_copy_data']['sub_registers']):
        for j, entry in enumerate(sub_register['entries']):
            '''
            Unicode characters:
            35 - Hash #
            37 - Percentage %
            42 - Asterix *
            60 - Less than <
            61 - Equals =
            62 - Greater than >
            172 - Not note ¬
            '''
            delimiter_array = [35, 37, 42, 60, 61, 62, 172]
            txt = json_in['official_copy_data']['sub_registers'][i]['entries'][j]['full_text']
            for delimiter in delimiter_array:
                txt = txt.replace(chr(delimiter), "")
            json_out['official_copy_data']['sub_registers'][i]['entries'][j]['full_text'] = txt

    return json_out


def _username_from_header(request):
    """ US107 """
    """ Get username (if any) from WebSeal headers """
    user_id = request.headers.get("iv-user", None)
    if user_id is None:
        return None
    p = re.compile("[%][{0-9}][{0-9}]")
    user_id = p.sub("", user_id)
    return user_id
