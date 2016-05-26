import json
import demjson
import logging
import logging.config                                                                                  # type: ignore
import re
import os
import requests
from flask import abort, Markup, redirect, render_template, request, Response, url_for  # type: ignore
from flask_weasyprint import HTML, render_pdf                                                          # type: ignore
from service import (address_utils, api_client, app, auditing, health_checker, title_formatter, title_utils)
from service.forms import TitleSearchForm, LandingPageForm, ConfirmTermsConditionsForm
from datetime import datetime

# TODO: move this to the template
UNAUTHORISED_WORDING = Markup('If this problem persists please contact us at '
                              '<a rel="external" href="mailto:digital-register-'
                              'feedback@digital.landregistry.gov.uk">'
                              'digital-register-feedback@digital.landregistry.gov.uk</a>.')
# TODO: move this to the template
TITLE_NUMBER_REGEX = re.compile('^([A-Z]{0,3}[1-9][0-9]{0,5}|[0-9]{1,6}[ZT])$')
POSTCODE_REGEX = re.compile(address_utils.BASIC_POSTCODE_REGEX)
LOGGER = logging.getLogger(__name__)


# landing page for DRV - this is whitelisted by webseal.
@app.route('/', methods=['GET', 'POST'])
def landing_page():

    form = LandingPageForm()
    price = app.config['TITLE_REGISTER_SUMMARY_PRICE']

    if request.method == 'POST' and form.validate():
        if form.information.data == 'title_summary':
            return redirect(url_for('search'))
        elif form.information.data == 'full_title_documents':
            return redirect('https://eservices.landregistry.gov.uk/wps/portal/Property_Search')
        elif form.information.data == 'official_copy':
            return redirect('https://www.gov.uk/government/publications/official-copies-of-register-or-plan-registration-oc1')

    else:
        return render_template('landing_page.html', form=form, price=price)


@app.route('/search', methods=['GET'])
def search():
    LOGGER.debug("STARTED: Search")
    username = _username_from_header(request)
    price = app.config['TITLE_REGISTER_SUMMARY_PRICE']
    price_text = app.config['TITLE_REGISTER_SUMMARY_PRICE_TEXT']
    LOGGER.debug("ENDED: Search")
    return render_template(
        'search.html',
        form=TitleSearchForm(),
        username=username,
        price=app.config['TITLE_REGISTER_SUMMARY_PRICE'],
        price_text=app.config['TITLE_REGISTER_SUMMARY_PRICE_TEXT'],
    )


@app.route('/confirm-selection-hidden/<title_number>/<search_term>', methods=['POST'])
def confirm_selection_after_login(title_number, search_term):

    LOGGER.debug("STARTED: confirm_selection_after_login title_number, search_term: {0}, {1}".format(
        title_number, search_term
    ))
    form = request.args.get('forms')
    price_text = request.args.get('price_text')
    username = _username_from_header(request)
    LOGGER.debug("ENDED: confirm_selection")

    return _payment(price_text, form, search_term, username, title_number)


@app.route('/confirm-selection/<title_number>/<search_term>', methods=['GET', 'POST'])
def confirm_selection(title_number, search_term):

    LOGGER.debug("STARTED: confirm_selection title_number, search_term: {0}, {1}".format(
        title_number, search_term
    ))

    form = ConfirmTermsConditionsForm()
    username = _username_from_header(request)
    search_term = request.args.get('search_term', search_term)
    price_text = app.config['TITLE_REGISTER_SUMMARY_PRICE_TEXT']

    LOGGER.debug("ENDED: confirm_selection")
    return _payment(price_text, form, search_term, username, title_number)

def _payment(price_text, form, search_term, username, title_number):
    LOGGER.debug("STARTED: _payment price_text, form, search_term: {0}, {1}, {2}".format(price_text,
        form, search_term
    ))

    lrpi_url = app.config['LAND_REGISTRY_PAYMENT_INTERFACE_URI']

    if request.method == 'POST' and form.validate() and username:
        # If they ticked the checkbox and are logged in ...
        params = _worldpay_form(search_term, title_number, username)

        # Save user's search details.
        response = api_client.save_search_request(params)
        params['cartId'] = response.text

        worldpay_data = requests.post(lrpi_url, data=params)

        if worldpay_data.headers['pay_mode'] == 'worldpay':
            worldpay_json = json.loads(worldpay_data.text)
            LOGGER.debug("ENDED: _payment")

            return render_template('hiddenWP.html', worldpay_params=worldpay_json)
        else:
            redirect_url = worldpay_data.text
            LOGGER.debug("ENDED: _payment")

            return redirect(redirect_url)

    elif request.method == 'POST' and form.validate() and not username:
        # If they have ticked the box but they are not logged in
        LOGGER.debug("ENDED: _payment")

        return redirect(url_for(confirm_selection_after_login, title_number=title_number, price_text=price_text, form=form,
                               search_term=search_term))

    else:
        # If they have just been sent to the page, or haven't ticked the checkbox ...
        params = _worldpay_form(search_term, title_number, username)
        params['display_page_number'] = int(request.args.get('page') or 1)
        LOGGER.debug("ENDED: _payment")

        return render_template('confirm_selection.html', title_number=title_number, params=params, price_text=price_text, form=form,
                               search_term=search_term)


@app.route('/health', methods=['GET'])
def healthcheck():
    LOGGER.debug("STARTED: healthcheck")
    errors = health_checker.perform_healthchecks()
    status, http_status = ('error', 500) if errors else ('ok', 200)

    response_body = {'status': status}

    if errors:
        response_body['errors'] = errors
    LOGGER.debug("ENDED: healthcheck")
    return Response(
        json.dumps(response_body),
        status=http_status,
        mimetype='application/json',
    )


@app.route('/cookies', methods=['GET'])
def cookies():
    return _cookies_page()


@app.route('/terms-and-conditions', methods=['GET'])
def terms_and_conditions():
    return _terms_and_conditions_page()


@app.route('/titles/<title_number>', methods=['GET'])
def get_title(title_number):
    """
    Show title (result) if user is logged in, has paid and hasn't viewed before.
    """
    LOGGER.debug("STARTED: get_title title_number: {0}".format(title_number))
    title = _get_register_title(title_number)
    username = _username_from_header(request)

    if title and _user_can_view(username, title_number):
        display_page_number = int(request.args.get('page') or 1)
        search_term = request.args.get('search_term', title_number)
        show_pdf = _should_show_full_title_pdf()
        full_title_data = (
            api_client.get_official_copy_data(title_number) if _should_show_full_title_data() else None
        )

        full_title_data = _strip_delimiters(full_title_data)

        LOGGER.debug("Title number{0}".format(title_number))
        auditing.audit("VIEW REGISTER: Title number {0} was viewed by {1}".format(
            title_number,
            username)
        )
        vat_json = {"date": 'N/A',
                    "address1": 'N/A',
                    "address2": 'N/A',
                    "address3": 'N/A',
                    "address4": 'N/A',
                    "postcode": 'N/A',
                    "title_number": 'N/A',
                    "net_amt": 0,
                    "vat_amt": 0,
                    "fee_amt": 0,
                    "vat_num": 'N/A'}

        transId = request.args.get('transid')
        if transId:
            receiptData = api_client.get_invoice_data(transId)
            receiptText = demjson.decode(receiptData.text)
            vat_json = demjson.decode(receiptText['vat_json'])

        receipt = {
            "trans_id": transId,
            "date": vat_json['date'],
            "address1": vat_json['address1'],
            "address2": vat_json['address2'],
            "address3": vat_json['address3'],
            "address4": vat_json['address4'],
            "postcode": vat_json['postcode'],
            "title_number": title_number,
            "net": "{0:.2f}".format(vat_json['net_amt']),
            "vat": "{0:.2f}".format(vat_json['vat_amt']),
            "total": "{0:.2f}".format(vat_json['fee_amt']),
            "reg_number": vat_json['vat_num']
        }

        LOGGER.debug("ENDED: get_title")

        return _title_details_page(title, search_term, show_pdf, full_title_data, request, receipt)

    else:
        LOGGER.debug("ENDED: get_title")
        abort(404)


@app.route('/titles/<title_number>.pdf', methods=['GET'])
def display_title_pdf(title_number):
    LOGGER.debug("STARTED: display_title_pdf title_number: {}".format(title_number))
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
                LOGGER.debug("ENDED: display_title_pdf")

                return render_pdf(HTML(string=html))
    LOGGER.debug("ENDED: display_title_pdf")
    abort(404)


@app.route('/title-search', methods=['POST'])
@app.route('/title-search/<search_term>', methods=['POST'])
def find_titles():
    LOGGER.debug("STARTED: find_titles")
    display_page_number = int(request.args.get('page') or 1)
    price = app.config['TITLE_REGISTER_SUMMARY_PRICE']
    price_text = app.config['TITLE_REGISTER_SUMMARY_PRICE_TEXT']
    search_term = request.form['search_term'].strip()
    form = TitleSearchForm()

    if search_term and form.validate():
        LOGGER.debug("ENDED: find_titles search_term: {0}".format(search_term))

        return redirect(url_for('find_titles', search_term=search_term, page=display_page_number, price=price, price_text=price_text,))
    else:
        # TODO: we should redirect to that page
        LOGGER.debug("ENDED: find_titles")

        return _initial_search_page(request)


@app.route('/title-search', methods=['GET'])
@app.route('/title-search/<search_term>', methods=['GET'])
def find_titles_page(search_term=''):
    LOGGER.debug("STARTED: find_titles_page search_term: {}".format(search_term))

    display_page_number = int(request.args.get('page') or 1)
    page_number = display_page_number - 1  # page_number is 0 indexed
    username = _username_from_header(request)
    search_term = search_term.strip()

    if not search_term:
        LOGGER.debug("ENDED: find_titles_page")

        return _initial_search_page(request)
    else:
        message_format = "SEARCH REGISTER: '{0}' was searched by {1}"
        auditing.audit(message_format.format(search_term, username))
        LOGGER.debug("ENDED: find_titles_page search_term: {0}".format(search_term))

        return _get_address_search_response(search_term, page_number)


def _worldpay_form(search_term, title_number, username):
    LOGGER.debug("STARTED: _worldpay_form search_term, title_number, username: {0}, {1}, {2}".format(
        search_term, title_number, username
    ))

    params = dict()
    params['search_term'] = search_term
    params['title'] = _get_register_title(title_number)
    params['title_number'] = title_number
    params['MC_titleNumber'] = title_number
    # should one of: A, D, M, T, I
    params['MC_searchType'] = 'D'
    params['MC_timestamp'] = api_client._get_time()
    params['MC_purchaseType'] = os.getenv('WP_MC_PURCHASETYPE', 'drvSummaryView')
    params['MC_unitCount'] = '1'
    params['desc'] = search_term
    params['amount'] = app.config['TITLE_REGISTER_SUMMARY_PRICE']
    params['MC_userId'] = username

    # Last changed date - modified to remove colon in UTC offset, which python
    # datetime.strptime() doesn't like >>>
    datestring = params['title']['last_changed']
    if len(datestring) == 25:
        if datestring[22] == ':':
            l = list(datestring)
            del (l[22])
            datestring = "".join(l)

    dt_obj = datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S%z")
    params['last_changed_datestring'] = \
        "%d %s %d" % (dt_obj.day, dt_obj.strftime("%B"), dt_obj.year)
    params['last_changed_timestring'] = \
        "%s:%s:%s" % ('{:02d}'.format(dt_obj.hour),
                      '{:02d}'.format(dt_obj.minute),
                      '{:02d}'.format(dt_obj.second))
    LOGGER.debug("ENDED: _worldpay_form")

    return params


def _get_register_title(title_number):
    LOGGER.debug("STARTED: _get_register_title title_number{}".format(title_number))
    title = api_client.get_title(title_number)
    LOGGER.debug("_get_register_title: {0}".format(title))
    LOGGER.debug("ENDED: _get_register_title")
    return title_formatter.format_display_json(title) if title else None


def _user_can_view(username, title_number):
    LOGGER.debug("STARTED: _user_can_view username, title_number: {0}, {1}".format(
        username, title_number
    ))
    access_granted = api_client.user_can_view(username, title_number)
    LOGGER.debug("_user_can_view: {0}".format(access_granted))
    LOGGER.debug("ENDED: _user_can_view")
    return access_granted


def _get_address_search_response(search_term, page_number):
    LOGGER.debug("STARTED: _get_address_search_response search_term, page_number: {0}, {1}".format(
        search_term, page_number
    ))
    search_term = search_term.upper()
    if _is_title_number(search_term):
        LOGGER.info('title number search used')
        LOGGER.debug("ENDED: _get_address_search_response")
        return _get_search_by_title_number_response(search_term, page_number)
    elif _is_postcode(search_term):
        LOGGER.info('postcode search used')
        LOGGER.debug("ENDED: _get_address_search_response")
        return _get_search_by_postcode_response(search_term, page_number)
    else:
        LOGGER.info('address search used')
        LOGGER.debug("ENDED: _get_address_search_response")
        return _get_search_by_address_response(search_term, page_number)


def _get_search_by_title_number_response(search_term, page_number):
    LOGGER.debug("STARTED: _get_search_by_title_number_response search_term, page_number: {0}, {1}".format(
        search_term, page_number
    ))
    display_page_number = page_number + 1
    title_number = search_term
    title = _get_register_title(title_number)
    if title:
        # Redirect to the display_title method to display the digital register
        LOGGER.debug("ENDED: _get_search_by_title_number_response")
        return redirect(url_for('get_title', title_number=title_number,
                                page_number=display_page_number, search_term=search_term))
    else:
        # If title not found display 'no title found' screen
        results = {'number_results': 0}
        LOGGER.debug("ENDED: _get_search_by_title_number_response")
        return _search_results_page(results, search_term)


def _get_search_by_postcode_response(search_term, page_number):
    LOGGER.debug("STARTED: _get_search_by_postcode_response search_term, page_number: {0}, {1}".format(
        search_term, page_number
    ))
    postcode = _normalise_postcode(search_term)
    postcode_search_results = api_client.get_titles_by_postcode(postcode, page_number)
    LOGGER.debug("_get_search_by_postcode_response: {0}".format(postcode_search_results))
    LOGGER.debug("ENDED: _get_search_by_postcode_response")
    return _search_results_page(postcode_search_results, postcode, True)


def _get_search_by_address_response(search_term, page_number):
    LOGGER.debug("STARTED: _get_search_by_address_response search_term, page_number: {0}, {1}".format(
        search_term, page_number
    ))
    address_search_results = api_client.get_titles_by_address(search_term, page_number)
    LOGGER.debug("_get_search_by_address_response: {0}".format(address_search_results))
    LOGGER.debug("ENDED: _get_search_by_address_response")
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


def _breadcumbs_for_title_details(title_number, search_term, display_page_number):
    LOGGER.debug("STARTED: _breadcumbs_for_title_details title_number, search_term, display_page_number {0}, {1}, {2}".format(
        title_number, search_term, display_page_number
    ))
    search_breadcrumb = {'text': 'Search the land and property register', 'url': url_for('find_titles')}
    results_breadcrumb = {'text': 'Search results', 'url': url_for('find_titles_page', search_term=search_term,
                                                                   page=display_page_number)}
    current_breadcrumb = {'current': 'Viewing {}'.format(title_number)}

    found_title_by_number = title_number.lower() == search_term.lower()

    if found_title_by_number:
        LOGGER.debug("ENDED: _breadcumbs_for_title_details")
        return [search_breadcrumb, current_breadcrumb]
    else:
        LOGGER.debug("ENDED: _breadcumbs_for_title_details")
        return [search_breadcrumb, results_breadcrumb, current_breadcrumb]


def _normalise_postcode(postcode_in):
    # We strip out the spaces - and reintroduce one four characters from end
    no_spaces = postcode_in.replace(' ', '')
    postcode = no_spaces[:len(no_spaces) - 3] + ' ' + no_spaces[-3:]
    return postcode


def _title_details_page(title, search_term, show_pdf, full_title_data, request, receipt):
    username = _username_from_header(request)
    return render_template(
        'display_title.html',
        title=title,
        username=username,
        search_term=search_term,
        show_pdf=show_pdf,
        full_title_data=full_title_data,
        is_caution_title=title_utils.is_caution_title(title),
        receipt=receipt,
    )


def _initial_search_page(request):
    username = _username_from_header(request)
    price = app.config['TITLE_REGISTER_SUMMARY_PRICE']
    price_text = app.config['TITLE_REGISTER_SUMMARY_PRICE_TEXT']
    form = TitleSearchForm()
    search_term = ''

    if request.method == 'POST':
        form.validate()
        search_term = request.form['search_term'].strip()

    return render_template(
        'search.html',
        form=form,
        username=username,
        price=price,
        price_text=price_text,
        search_term=search_term
    )


def _search_results_page(results, search_term, addressbase=False):
    username = _username_from_header(request)
    return render_template(
        'search_results.html',
        search_term=search_term,
        results=results,
        form=TitleSearchForm(),
        addressbase=addressbase,
        username=username
    )


def _cookies_page():
    return render_template('cookies.html', username=_username_from_header(request))


def _terms_and_conditions_page():
    return render_template('terms_and_conditions.html')


def _create_string_date_only(datetoconvert):
    # converts to example : 12 August 2014
    date = datetoconvert.strftime('%-d %B %Y')
    LOGGER.debug("_create_string_date_only: {0}".format(date))
    return date


def _create_string_date_and_time(datetoconvert):
    # converts to example : 12 August 2014 12:34:06
    date = datetoconvert.strftime('%-d %B %Y at %H:%M:%S')
    LOGGER.debug("_create_string_date_and_time: {0}".format(date))
    return date


def _create_pdf_template(sub_registers, title, title_number):
    LOGGER.debug("STARTED: _create_pdf_template sub_registers, title, title_number {0}, {1}, {2}".format(
        sub_registers, title, title_number
    ))
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

    LOGGER.debug("ENDED: _create_pdf_template")

    return render_template('pdf/full_title.html', title_number=title_number, title=title,
                           last_entry_date=last_entry_date,
                           issued_date=issued_date,
                           edition_date=edition_date,
                           class_of_title=class_of_title,
                           sub_registers=sub_registers,
                           is_caution=is_caution,
                           districts=districts)


def _strip_delimiters(json_in):
    # Remove all delimiters and not notes from json
    LOGGER.debug("STARTED: _strip_delimiters")
    json_out = json_in
    try:
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
    except Exception as e:
        # For when SHOW_FULL_TITLE_DATA = False
        pass
    LOGGER.debug("ENDED: _strip_delimiters")
    return json_out


def _username_from_header(request):
    # Gets username, if any, from webseal headers
    user_id = request.headers.get("iv-user", None)
    if user_id:
        p = re.compile("[%][{0-9}][{0-9}]")
        user_id = p.sub("", user_id)
    if user_id == "Unauthenticated":
        user_id = None
    LOGGER.debug("_username_from_header: {0}".format(user_id))
    return user_id
