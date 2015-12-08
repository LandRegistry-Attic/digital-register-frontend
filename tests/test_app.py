from datetime import datetime  # type: ignore
from io import BytesIO  # type: ignore
import json  # type: ignore
import mock  # type: ignore
from PyPDF2 import PdfFileReader  # type: ignore
import pytest  # type: ignore
from unittest.mock import call  # type: ignore
from werkzeug.datastructures import Headers  # type: ignore
from lxml.html import document_fromstring  # type: ignore

from config import CONFIG_DICT  # type: ignore
import service  # type: ignore
from service.server import app  # type: ignore
from .fake_response import FakeResponse  # type: ignore

TEST_USERNAME = 'username1'

with open('tests/data/fake_title.json', 'r') as fake_title_file:
    fake_title_file_json_string = fake_title_file.read()
    fake_title_bytes = str.encode(fake_title_file_json_string)
    fake_title = FakeResponse(fake_title_bytes)

with open('tests/data/fake_no_titles.json', 'r') as fake_no_titles_file:
    fake_no_titles_file_json_string = fake_no_titles_file.read()
    fake_no_titles_bytes = str.encode(fake_no_titles_file_json_string)
    fake_no_titles = FakeResponse(fake_no_titles_bytes)

with open('tests/data/fake_title_with_charge.json', 'r') as fake_title_with_charge_file:
    fake_title_with_charge_file_json_string = fake_title_with_charge_file.read()
    fake_title_with_charge_bytes = str.encode(fake_title_with_charge_file_json_string)
    fake_charge_title = FakeResponse(fake_title_with_charge_bytes)

with open('tests/data/fake_postcode_search_result.json', 'r') as fake_postcode_results_json_file:
    fake_postcode_search_results_json_string = fake_postcode_results_json_file.read()
    fake_postcode_search_bytes = str.encode(fake_postcode_search_results_json_string)
    fake_postcode_search = FakeResponse(fake_postcode_search_bytes)

fake_address_search = fake_postcode_search

with open('tests/data/fake_no_address_title.json', 'r') as fake_no_address_title_file:
    fake_no_address_title_json_string = fake_no_address_title_file.read()
    fake_no_address_title_bytes = str.encode(fake_no_address_title_json_string)
    fake_no_address_title = FakeResponse(fake_no_address_title_bytes)

with open('tests/data/fake_partial_address.json', 'r') as fake_partial_address_file:
    fake_partial_address_json_string = fake_partial_address_file.read()
    fake_partial_address_bytes = str.encode(fake_partial_address_json_string)
    fake_partial_address = FakeResponse(fake_partial_address_bytes)

with open('tests/data/address_only_no_regex_match.json', 'r') as address_only_no_regex_match_title_file:
    address_only_no_regex_match_title_json_string = address_only_no_regex_match_title_file.read()
    address_only_no_regex_match_bytes = str.encode(address_only_no_regex_match_title_json_string)
    address_only_no_regex_match_title = FakeResponse(address_only_no_regex_match_bytes)

with open('tests/data/official_copy_response.json', 'r') as official_copy_response_file:
    official_copy_response = json.loads(official_copy_response_file.read())

unavailable_title = FakeResponse('', 404)


class TestViewTitle:

    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    @mock.patch('service.api_client.requests.get', return_value=unavailable_title)
    def test_get_title_page_no_title(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 404
        assert 'Page not found' in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_get_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200

    @mock.patch('service.auditing.audit')
    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_get_title_page_audits_the_event(self, mock_get_official_copy_data, mock_get, mock_audit):
        response = self.app.get('/titles/titleref', headers=self.headers)

        mock_audit.assert_called_once_with(
            "VIEW REGISTER: Title number titleref was viewed by {}".format(TEST_USERNAME)
        )

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_date_formatting_on_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert '28 August 2014' in response.data.decode()
        assert '12:37:13' in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_address_on_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        page_content = response.data.decode()
        assert '17 Hazelbury Crescent' in page_content
        assert 'Luton' in page_content
        assert 'LU1 1DZ' in page_content

    @mock.patch('service.api_client.requests.get', return_value=fake_partial_address)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_partial_address_on_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        page_content = response.data.decode()
        assert 'Hazelbury Crescent' in page_content
        assert 'Luton' in page_content
        assert 'LU1 1DZ' in page_content

    @mock.patch('service.api_client.requests.get', return_value=fake_no_address_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_address_string_only_on_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert '17 Hazelbury Crescent<br>Luton<br>LU1 1DZ' in str(response.data)

    @mock.patch('service.api_client.requests.get', return_value=address_only_no_regex_match_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_address_string_500(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200
        assert 'West side of Narnia Road' in response.data.decode()
        assert 'MagicalTown' in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_proprietor_on_non_caution_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200

        response_data = response.data.decode()
        assert 'Scott Oakes' in response_data
        assert 'Owners' in response_data
        assert 'Cautioners' not in response_data

    @mock.patch('service.title_utils.is_caution_title', return_value=True)
    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_cautioner_on_caution_title_page(
            self, mock_get_official_copy_data, mock_get, mock_is_caution_title):

        response = self.app.get('/titles/titleref')
        assert response.status_code == 200

        response_data = response.data.decode()
        assert 'Scott Oakes' in response_data
        assert 'Owners' not in response_data
        assert 'Cautioners' in response_data

    @mock.patch('service.api_client.requests.get', return_value=fake_charge_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_lender_on_title_page_with_charge(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200
        assert 'National Westminster Home Loans Limited' in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_lender_not_on_title_page_without_charge(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200
        assert 'National Westminster Home Loans Limited' not in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_tenure_on_non_caution_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200
        response_data = response.data.decode()

        assert 'Tenure type' in response_data
        assert 'Freehold' in response_data

    @mock.patch('service.title_utils.is_caution_title', return_value=True)
    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_no_tenure_on_caution_title_page(
            self, mock_get_official_copy_data, mock_get, mock_is_caution_title):

        response = self.app.get('/titles/titleref')
        assert response.status_code == 200
        assert 'Tenure' not in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_ppi_data_on_title_page(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref')
        assert 'Price paid stated data' in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_index_geometry_on_title_page(self, mock_get_official_copy_data, mock_get):
        coordinate_data = '[[[508263.97, 221692.13],'
        response = self.app.get('/titles/titleref')
        page_content = response.data.decode()
        # import pdb; pdb.set_trace()

        assert response.status_code == 200
        assert coordinate_data in page_content
        assert 'geometry' in page_content
        assert 'coordinates' in page_content

    @mock.patch('service.auditing.audit')
    @mock.patch('service.api_client.requests.get', return_value=unavailable_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_get_title_page_returns_500_when_error(self, mock_get_official_copy_data, mock_get, mock_audit):
        mock_get.side_effect = Exception('test exception')
        response = self.app.get('/titles/titleref')
        assert response.status_code == 500
        assert 'Sorry, we are experiencing technical difficulties.' in response.data.decode()
        assert mock_audit.mock_calls == []

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_breadcrumbs_search_results_do_not_appear(self, mock_get_official_copy_data, mock_get):
        # This tests that when going directly to a title the search results breadcrumb doesn't show
        response = self.app.get('/titles/DN1000')
        page_content = response.data.decode()
        assert 'Search the land and property register' in page_content
        assert 'Search results' not in page_content
        assert 'Viewing DN1000' in page_content

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_breadcrumbs_search_results_appear(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/DN1000?search_term="testing"')
        page_content = response.data.decode()
        assert 'Search the land and property register' in page_content
        assert 'Search results' in page_content
        assert 'Viewing DN1000' in page_content

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_get_more_proprietor_data(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/AGL1000')
        page_content = response.data.decode()
        assert 'trading as RKJ Machinists PLC' in page_content
        assert 'Dr' in page_content

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch.object(service.api_client, 'get_official_copy_data')
    def test_get_title_calls_api_client_for_full_info_when_configured(self, mock_get_copy, mock_get):

        with mock.patch.dict(app.config, {'SHOW_FULL_TITLE_DATA': True}):
            title_number = 'AGL1234'
            self.app.get('/titles/{}'.format(title_number))
            mock_get_copy.assert_called_once_with(title_number)

    @mock.patch.object(service.api_client, 'get_official_copy_data')
    def test_get_title_does_not_call_api_client_for_full_info_when_not_configured(self, mock_get_copy):

        with mock.patch.dict(app.config, {'SHOW_FULL_TITLE_DATA': False}):
            title_number = 'AGL1234'
            self.app.get('/titles/{}'.format(title_number))
            assert mock_get_copy.mock_calls == []

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_get_title_returns_page_containing_official_copy_info_page_when_present(self, mock_get_copy, mock_get):
        title_number = 'AGL1234'
        response = self.app.get('/titles/{}'.format(title_number))
        assert response.status_code == 200
        response_body = response.data.decode()
        strings_to_find_on_page = [
            'AGL1234',
            'Register name : A',
            '1.  Not Dated  - A yearly ... payable yearly on ...',
            '2. 1995-11-06 - The land has the ...',
            'Register name : B',
            '1. 1996-07-01 - PROPRIETOR: JOHN SMITH',
            '2. 1996-07-01 - RESTRICTION: Except under an order of...',
            'Register name : C',
            '7. 1996-07-01 - REGISTERED CHARGE dated 3 July 1995...',
            '8. 1996-07-01 - Proprietor: WESTMINSTER H...',
        ]

        for i in range(0, len(strings_to_find_on_page)):
            string_to_find = strings_to_find_on_page[i]
            assert string_to_find in response_body

            if i > 0:
                previous_string = strings_to_find_on_page[i - 1]
                assert response_body.index(string_to_find) > response_body.index(previous_string)


class TestDisplayTitlePdf:

    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    @mock.patch('service.api_client.requests.get', return_value=unavailable_title)
    def test_display_title_pdf_no_title(self, mock_get):
        response = self.app.get('/titles/titleref.pdf')
        assert response.status_code == 404
        assert 'Page not found' in response.data.decode()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_display_title_pdf(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref.pdf')
        assert response.status_code == 200

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    @mock.patch('service.server.render_template')
    def test_display_title_pdf_renders_template(self, mock_render, mock_get_official_copy_data, mock_get):
        self.app.get('/titles/titleref.pdf')
        actual_call = mock_render.mock_calls[0]
        actual_args = actual_call[1]
        actual_kwargs = actual_call[2]

        assert actual_args[0] == 'full_title.html'
        assert actual_kwargs['title_number'] == 'titleref'
        assert actual_kwargs['last_entry_date'] == '3 February 3001 at 04:05:06'
        assert actual_kwargs['issued_date'] == datetime.now().strftime('%-d %B %Y')
        assert actual_kwargs['edition_date'] == '12 August 2013'
        assert actual_kwargs['class_of_title'] == 'Absolute'
        assert actual_kwargs['sub_registers'] == official_copy_response['official_copy_data']['sub_registers']

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_display_title_pdf_includes_official_copy_data(self, mock_get_official_copy_data, mock_get):
        response = self.app.get('/titles/titleref.pdf')
        pdf = PdfFileReader(BytesIO(response.data))
        pdf_text = '\n'.join([page.extractText() for page in pdf.pages])
        sub_registers = official_copy_response['official_copy_data']['sub_registers']
        for sub_register in sub_registers:
            for entry in sub_register['entries']:
                assert entry['full_text'] in pdf_text

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch.object(service.api_client, 'get_official_copy_data')
    def test_display_title_pdf_calls_api_client_for_full_info_when_enabled(self, mock_get_copy, mock_get):
        with mock.patch.dict(app.config, {'SHOW_FULL_TITLE_PDF': True}):
            title_number = 'AGL1234'
            self.app.get('/titles/{}.pdf'.format(title_number))
            mock_get_copy.assert_called_once_with(title_number)

    @mock.patch.object(service.api_client, 'get_official_copy_data')
    def test_display_title_pdf_doesnt_call_api_client_for_full_info_when_disabled(self, mock_get_copy):
        with mock.patch.dict(app.config, {'SHOW_FULL_TITLE_PDF': False}):
            title_number = 'AGL1234'
            self.app.get('/titles/{}.pdf'.format(title_number))
            assert mock_get_copy.mock_calls == []


class TestTitleSearch:

    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    def test_get_title_search_page(self):
        response = self.app.get('/title-search')
        assert response.status_code == 200
        assert 'Search the land and property register' in str(response.data)

    @mock.patch('requests.get', return_value=fake_title)
    @mock.patch.object(service.api_client, 'get_official_copy_data')
    def test_title_search_success(self, mock_get_official_copy, mock_get):
        response = self.app.post('/title-search', data={'search_term': 'DN1000'}, follow_redirects=True)
        assert response.status_code == 200
        page_content = response.data.decode()
        assert 'DN1000' in page_content
        assert '28 August 2014' in page_content
        assert '12:37:13' in page_content
        assert '17 Hazelbury Crescent' in page_content
        assert 'Luton' in page_content
        assert 'LU1 1DZ' in page_content

    @mock.patch('requests.get', return_value=fake_no_titles)
    def test_title_search_plain_text_value_format(self, mock_get):
        response = self.app.post('/title-search', data={'search_term': 'some text'}, follow_redirects=True)
        assert '0 results found' in response.data.decode()

    @mock.patch('service.auditing.audit')
    @mock.patch('requests.get', return_value=fake_no_titles)
    def test_title_search_audits_the_events(self, mock_get, mock_audit):
        search_term = 'search term'
        response = self.app.get('/title-search/search term', follow_redirects=True, headers=self.headers)
        audit_text = "SEARCH REGISTER: '{}' was searched by {}".format(search_term, TEST_USERNAME)
        mock_audit.assert_called_once_with(audit_text)

    @mock.patch('requests.get', return_value=fake_postcode_search)
    def test_postcode_search_success(self, mock_get):
        response = self.app.post('/title-search', data={'search_term': 'PL9 7FN'}, follow_redirects=True)
        assert response.status_code == 200
        page_content = response.data.decode()
        assert 'AGL1000' in page_content

    @mock.patch('requests.get', return_value=fake_postcode_search)
    def test_postcode_search_with_page_calls_api_correctly(self, mock_get):
        self.app.get('/title-search/PL9%207FN?page=23')
        mock_get.assert_called_with('http://landregistry.local:8004/title_search_postcode/PL9 7FN', params={'page': 22})

    @mock.patch('requests.get', return_value=fake_address_search)
    def test_address_search_with_page_calls_api_correctly(self, mock_get):
        self.app.get('/title-search/PLYMOUTH?page=23')
        mock_get.assert_called_with('http://landregistry.local:8004/title_search_address/PLYMOUTH', params={'page': 22})

    @mock.patch('requests.get', return_value=fake_postcode_search)
    def test_search_title_passes_postcode_to_api_with_space_added_when_missing(self, mock_get):
        search_term = 'PL98TB'
        expected_postcode = 'PL9 8TB'
        self.app.get('/title-search/{}'.format(search_term))

        assert len(mock_get.mock_calls) == 1
        actual_call = mock_get.mock_calls[0]
        url_param = actual_call[1][0]
        assert url_param.endswith('title_search_postcode/{}'.format(expected_postcode))

    @mock.patch('requests.get', return_value=fake_postcode_search)
    def test_search_title_passes_postcode_to_api_as_it_is_when_valid(self, mock_get):
        search_term = 'PL9 8TB'
        self.app.get('/title-search/{}'.format(search_term))

        assert len(mock_get.mock_calls) == 1
        actual_call = mock_get.mock_calls[0]
        url_param = actual_call[1][0]
        assert url_param.endswith('title_search_postcode/{}'.format(search_term))


class TestHealthcheck:

    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    @mock.patch('service.api_client.requests.get', return_value=FakeResponse())
    def test_health_calls_health_endpoints_of_apis(self, mock_api_get):
        self.app.get('/health')

        mock_api_get.assert_called_once_wth('{}health'.format(app.config['REGISTER_TITLE_API']))

    @mock.patch('service.health_checker.perform_healthchecks', return_value=[])
    def test_health_returns_ok_when_health_checker_returns_no_errors(
            self, mock_perform_healthchecks):

        response = self.app.get('/health')

        assert response.data.decode() == '{"status": "ok"}'
        assert response.status_code == 200


class TestSearchTerm:

    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    @mock.patch('requests.get', return_value=unavailable_title)
    def test_title_search_title_not_found(self, mock_get):
        response = self.app.post('/title-search', data={'search_term': 'DT1000'}, follow_redirects=True)
        assert '0 results found' in response.data.decode()


class TestAuthenticated:
    """
    Put webseal header in HTTP headers, request page and ensure that username
    page element is present in response (see layout.html)
    """
    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    @mock.patch('requests.get', return_value=fake_address_search)
    def test_authenticated(self, mock_get):
        """ Does header contain 'iv-user' username field? """
        response = self.app.get('/title-search/search term', follow_redirects=True, headers=self.headers)
        assert response.status_code == 200
        assert 'username' in str(response.data)


class TestWelsh:

    def setup_method(self, method):
        self.app = app.test_client()

    @mock.patch('service.api_client.requests.get', return_value=fake_title)
    @mock.patch('service.api_client.get_official_copy_data', return_value=official_copy_response)
    def test_welsh(self, mock_get_official_copy_data, mock_get):
        response = self.app.get("/titles/DN1000?language=cy")
        page_content = response.data.decode()
        assert response.status_code == 200
        assert "Rhif teitl" in page_content
        assert "Perchennog" in page_content

if __name__ == '__main__':
    pytest.main()
