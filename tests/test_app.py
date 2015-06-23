import json
import mock
import pytest
from unittest.mock import call
from config import CONFIG_DICT

from service.server import app
from .fake_response import FakeResponse


with open('tests/data/fake_title.json', 'r') as fake_title_json_file:
    fake_title_json_string = fake_title_json_file.read()
    fake_title_bytes = str.encode(fake_title_json_string)
    fake_title = FakeResponse(fake_title_bytes)

with open('tests/data/fake_title_with_charge.json', 'r') as fake_charge_title_json_file:
    fake_charge_title_json_string = fake_charge_title_json_file.read()
    fake_charge_title_bytes = str.encode(fake_charge_title_json_string)
    fake_charge_title = FakeResponse(fake_charge_title_bytes)

with open('tests/data/fake_no_titles.json', 'r') as fake_no_titles_json_file:
    fake_no_titles_json_string = fake_no_titles_json_file.read()
    fake_no_titles_bytes = str.encode(fake_no_titles_json_string)
    fake_no_titles = FakeResponse(fake_no_titles_bytes)

with open('tests/data/fake_postcode_search_result.json', 'r') as fake_postcode_results_json_file:
    fake_postcode_search_results_json_string = fake_postcode_results_json_file.read()
    fake_postcode_search_bytes = str.encode(fake_postcode_search_results_json_string)
    fake_postcode_search = FakeResponse(fake_postcode_search_bytes)

fake_address_search = fake_postcode_search

with open('tests/data/fake_no_address_title.json', 'r') as fake_no_address_title_file:
    fake_no_address_title_json_string = fake_no_address_title_file.read()
    fake_no_address_title_bytes = str.encode(fake_no_address_title_json_string)
    fake_no_address_title = FakeResponse(fake_no_address_title_bytes)

with open('tests/data/address_only_no_regex_match.json', 'r') as address_only_no_regex_match_file:
    address_only_no_regex_match_file_string = address_only_no_regex_match_file.read()
    address_only_no_regex_match_file_bytes = str.encode(address_only_no_regex_match_file_string)
    address_only_no_regex_match_title = FakeResponse(address_only_no_regex_match_file_bytes)

with open('tests/data/fake_partial_address.json', 'r') as fake_partial_address_file:
    fake_partial_address_json_string = fake_partial_address_file.read()
    fake_partial_address_bytes = str.encode(fake_partial_address_json_string)
    fake_partial_address = FakeResponse(fake_partial_address_bytes)


unavailable_title = FakeResponse('', 404)


class BaseServerTest:

    def _log_in_user(self):
        with mock.patch(
                'service.server.LoginApiClient.authenticate_user',
                return_value=True
        ):
            self.app.post(
                '/login',
                data={'username': 'username1', 'password': 'password1'},
                follow_redirects=False
            )


class TestViewTitleUnauthorised(BaseServerTest):

    def setup_method(self, method):
        self.app = app.test_client()

    def test_get_title_page_redirects_when_user_not_logged_in(self):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 302

        assert 'Location' in response.headers
        assert response.headers['Location'].endswith('/login?next=%2Ftitles%2Ftitleref')


class TestViewTitle(BaseServerTest):

    def setup_method(self, method):
        self.app = app.test_client()
        self._log_in_user()

        with mock.patch(
            'service.server.LoginApiClient.authenticate_user',
            return_value=True
        ):
            self._log_in_user()

    @mock.patch('requests.get', return_value=unavailable_title)
    def test_get_title_page_no_title(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 404
        assert 'Page not found' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_get_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200

    @mock.patch('requests.get', return_value=fake_title)
    def test_date_formatting_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert '28 August 2014' in response.data.decode()
        assert '12:37:13' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_address_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        page_content = response.data.decode()
        assert '17 Hazelbury Crescent' in page_content
        assert 'Luton' in page_content
        assert 'LU1 1DZ' in page_content

    @mock.patch('requests.get', return_value=fake_partial_address)
    def test_partial_address_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        page_content = response.data.decode()
        assert 'Hazelbury Crescent' in page_content
        assert 'Luton' in page_content
        assert 'LU1 1DZ' in page_content

    @mock.patch('requests.get', return_value=fake_no_address_title)
    def test_address_string_only_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert '17 Hazelbury Crescent<br>Luton<br>LU1 1DZ' in str(response.data)

    @mock.patch('requests.get', return_value=address_only_no_regex_match_title)
    def test_address_string_500(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200
        assert 'West side of Narnia Road' in response.data.decode()
        assert 'MagicalTown' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_proprietor_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert 'Scott Oakes' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_charge_title)
    def test_lender_on_title_page_with_charge(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert 'National Westminster Home Loans Limited' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_lender_not_on_title_page_without_charge(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert 'National Westminster Home Loans Limited' not in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_tenure_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert 'Freehold' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_ppi_data_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert 'Price paid stated data' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_index_geometry_on_title_page(self, mock_get):
        coordinate_data = '[[[508263.97, 221692.13],'
        response = self.app.get('/titles/titleref')
        page_content = response.data.decode()
        assert 'geometry' in page_content
        assert 'coordinates' in page_content
        assert coordinate_data in page_content

    @mock.patch('requests.get', return_value=unavailable_title)
    def test_get_title_page_returns_500_when_error(self, mock_get):
        mock_get.side_effect = Exception('test exception')
        response = self.app.get('/titles/titleref')
        assert response.status_code == 500
        assert 'Sorry, we are experiencing technical difficulties.' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_title)
    def test_breadcrumbs_search_results_do_not_appear(self, mock_get):
        # This tests that when going directly to a title the search results breadcrumb doesn't show
        response = self.app.get('/titles/DN1000')
        page_content = response.data.decode()
        assert 'Find a title' in page_content
        assert 'Search results' not in page_content
        assert 'Viewing DN1000' in page_content

    @mock.patch('requests.get', return_value=fake_title)
    def test_breadcrumbs_search_results_appear(self, mock_get):
        response = self.app.get('/titles/DN1000?search_term="testing"')
        page_content = response.data.decode()
        assert 'Find a title' in page_content
        assert 'Search results' in page_content
        assert 'Viewing DN1000' in page_content

    @mock.patch('requests.get', return_value=fake_title)
    def test_get_more_proprietor_data(self, mock_get):
        response = self.app.get('/titles/AGL1000')
        page_content = response.data.decode()
        assert 'trading as RKJ Machinists PLC' in page_content
        assert 'Dr' in page_content
        assert '(looking after dogs for life charity)' in page_content
        assert 'Registered overseas' in page_content
        assert 'Company registration number 999888999' in page_content


class TestTitleSearch(BaseServerTest):

    def setup_method(self, method):
        self.app = app.test_client()
        self._log_in_user()

    def test_get_title_search_page(self):
        response = self.app.get('/title-search')
        assert response.status_code == 200
        assert 'Find a title' in str(response.data)

    @mock.patch('requests.get', return_value=fake_title)
    def test_title_search_success(self, mock_get):
        response = self.app.post(
            '/title-search',
            data=dict(search_term='DN1000'),
            follow_redirects=True
        )
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
        response = self.app.post(
            '/title-search',
            data=dict(search_term='some text'),
            follow_redirects=True
        )
        assert '0 results found' in response.data.decode()

    @mock.patch('requests.get', return_value=unavailable_title)
    def test_title_search_title_not_found(self, mock_get):
        response = self.app.post(
            '/title-search',
            data=dict(search_term='DT1000'),
            follow_redirects=True
        )
        assert '0 results found' in response.data.decode()

    @mock.patch('requests.get', return_value=fake_postcode_search)
    def test_postcode_search_success(self, mock_get):
        response = self.app.post(
            '/title-search',
            data=dict(search_term='PL9 7FN'),
            follow_redirects=True
        )
        assert response.status_code == 200
        page_content = response.data.decode()
        assert 'AGL1000' in page_content
        assert '21 Murhill Lane, Saltram Meadow, Plymouth, (PL9 7FN)' in page_content

    @mock.patch('requests.get', return_value=fake_postcode_search)
    def test_postcode_search_with_page_calls_api_correctly(self, mock_get):
        self.app.get('/title-search/PL9%207FN?page=23')
        mock_get.assert_called_with('http://landregistry.local:8004/title_search_postcode/PL9 7FN',
                                    params={'page': 23})

    @mock.patch('requests.get', return_value=fake_address_search)
    def test_address_search_with_page_calls_api_correctly(self, mock_get):
        self.app.get('/title-search/PLYMOUTH?page=23')
        mock_get.assert_called_with('http://landregistry.local:8004/title_search_address/PLYMOUTH',
                                    params={'page': 23})

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


class TestHealthcheck(BaseServerTest):

    def setup_method(self, method):
        self.app = app.test_client()

    @mock.patch('requests.get', return_value=FakeResponse())
    def test_health_calls_health_endpoints_of_apis(self, mock_get):
        self.app.get('/health')
        assert mock_get.mock_calls == [
            call('{}health'.format(CONFIG_DICT['REGISTER_TITLE_API'])),
            call('{}health'.format(CONFIG_DICT['LOGIN_API'])),
        ]

    @mock.patch('requests.get', return_value=FakeResponse(b'{"status": "ok"}', 200))
    def test_health_returns_ok_status_when_both_apis_healthy(self, mock_get):
        response = self.app.get('/health')

        assert response.data.decode() == '{"status": "ok"}'
        assert response.status_code == 200

    def test_health_returns_errors_from_both_api_health_endpoints(self):
        with mock.patch('requests.get') as mock_get:
            mock_get.side_effect = [
                FakeResponse(b'{"status": "error", "errors": ["e1", "e2"]}', 500),
                FakeResponse(b'{"status": "error", "errors": ["e3", "e4"]}', 500),
            ]

            response = self.app.get('/health')
        response_json = json.loads(response.data.decode())

        assert response_json['status'] == 'error'
        errors = response_json['errors']

        assert len(errors) == 2
        assert "digital-register-api health endpoint returned errors: ['e1', 'e2']" in errors
        assert "login-api health endpoint returned errors: ['e3', 'e4']" in errors

        assert response.status_code == 500

    def test_health_returns_handles_invalid_responses_from_apis(self):
        with mock.patch('requests.get') as mock_get:
            mock_get.side_effect = [
                FakeResponse(b'{"status": "error"}', 500),
                FakeResponse(b'not a json', 500),
            ]

            response = self.app.get('/health')
        response_json = json.loads(response.data.decode())

        assert response_json['status'] == 'error'
        errors = response_json['errors']

        assert len(errors) == 2
        assert ("digital-register-api health endpoint returned "
                "an invalid response: {'status': 'error'}") in errors
        assert "login-api health endpoint returned an invalid response: not a json" in errors
        assert response.status_code == 500

if __name__ == '__main__':
    pytest.main()
