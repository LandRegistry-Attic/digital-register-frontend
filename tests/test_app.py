import mock
import pytest

from service.server import app, sanitise_postcode
from .fake_response import FakeResponse


with open('tests/fake_title.json', 'r') as fake_title_json_file:
    fake_title_json_string = fake_title_json_file.read()
    fake_title_bytes = str.encode(fake_title_json_string)
    fake_title = FakeResponse(fake_title_bytes)

fake_no_titles_json_string = '[]'
fake_no_titles_bytes = str.encode(fake_no_titles_json_string)
fake_no_titles = FakeResponse(fake_no_titles_bytes)

with open('tests/fake_postcode_search_result.json', 'r') as fake_postcode_search_results_json_file:
    fake_postcode_search_results_json_string = fake_postcode_search_results_json_file.read()
    fake_postcode_search_bytes = str.encode(fake_postcode_search_results_json_string)
    fake_postcode_search = FakeResponse(fake_postcode_search_bytes)

with open('tests/fake_no_address_title.json', 'r') as fake_no_address_title_file:
    fake_no_address_title_json_string = fake_no_address_title_file.read()
    fake_no_address_title_bytes = str.encode(fake_no_address_title_json_string)
    fake_no_address_title = FakeResponse(fake_no_address_title_bytes)

with open('tests/address_only_no_regex_match.json', 'r') as address_only_no_regex_match_file:
    address_only_no_regex_match_file_string = address_only_no_regex_match_file.read()
    address_only_no_regex_match_file_bytes = str.encode(address_only_no_regex_match_file_string)
    address_only_no_regex_match_title = FakeResponse(address_only_no_regex_match_file_bytes)

with open('tests/fake_partial_address.json', 'r') as fake_partial_address_file:
    fake_partial_address_json_string = fake_partial_address_file.read()
    fake_partial_address_bytes = str.encode(fake_partial_address_json_string)
    fake_partial_address = FakeResponse(fake_partial_address_bytes)


unavailable_title = FakeResponse('', 404)


class TestViewTitleUnauthorised:
    def setup_method(self, method):
        self.app = app.test_client()

    def test_get_title_page_redirects_when_user_not_logged_in(self):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 302

        assert 'Location' in response.headers
        assert response.headers['Location'].endswith('/login?next=%2Ftitles%2Ftitleref')


class TestViewTitle:

    def setup_method(self, method):
        self.app = app.test_client()

        with mock.patch(
            'service.server.LoginApiClient.authenticate_user',
            return_value=True
        ) as mock_authorize:
            self._log_in_user()

    @mock.patch('requests.get', return_value=unavailable_title)
    def test_get_title_page_no_title(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 404

    @mock.patch('requests.get', return_value=fake_title)
    def test_get_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert response.status_code == 200

    @mock.patch('requests.get', return_value=fake_title)
    def test_date_formatting_on_title_page(self, mock_get):
        response = self.app.get('/titles/titleref')
        assert '28 August 2014 at 12:37:13' in response.data.decode()

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

    @mock.patch('requests.get', return_value=fake_title)
    def test_index_geometry_on_title_page(self, mock_get):
        coordinate_data = '[[[508263.97, 221692.13],'
        response = self.app.get('/titles/titleref')
        page_content = response.data.decode()
        assert 'geometry' in page_content
        assert 'coordinates' in page_content
        assert coordinate_data in page_content

    def test_get_title_search_page(self):
        response = self.app.get('/title-search/')
        assert response.status_code == 200
        assert 'Find a title' in str(response.data)

    @mock.patch('requests.get', return_value=fake_title)
    def test_title_search_success(self, mock_get):
        response = self.app.post(
            '/title-search/',
            data=dict(search_term='DN1000'),
            follow_redirects=True
        )
        assert response.status_code == 200
        page_content = response.data.decode()
        assert 'DN1000' in page_content
        assert '28 August 2014 at 12:37:13' in page_content
        assert '17 Hazelbury Crescent' in page_content
        assert 'Luton' in page_content
        assert 'LU1 1DZ' in page_content

    @mock.patch('requests.get', return_value=fake_no_titles)
    def test_title_search_plain_text_value_format(self, mock_get):
        response = self.app.post(
            '/title-search/',
            data=dict(search_term='some text')
        )
        assert 'No result(s) found' in response.data.decode()

    @mock.patch('requests.get', return_value=unavailable_title)
    def test_title_search_title_not_found(self, mock_get):
        response = self.app.post(
            '/title-search/',
            data=dict(search_term='DT1000')
        )
        assert 'No result(s) found' in response.data.decode()

    def _log_in_user(self):
        self.app.post(
            '/login',
            data={'username': 'username1', 'password': 'password1'},
            follow_redirects=False
        )

    @mock.patch('requests.get', return_value=fake_postcode_search)
    def test_postcode_search_success(self, mock_get):
        response = self.app.post(
            '/title-search/',
            data=dict(search_term='PL9 7FN'),
            follow_redirects=True
        )
        assert response.status_code == 200
        page_content = response.data.decode()
        assert 'AGL1000' in page_content
        assert '21 Murhill Lane, Saltram Meadow, Plymouth, (PL9 7FN)' in page_content

    def test_postcode_without_space_search_success(self):
        search_term = 'PL98TB'
        postcode = sanitise_postcode(search_term)
        assert postcode == 'PL9 8TB'

    def test_postcode_bad_space_search_success(self):
        search_term = 'PL 98TB'
        postcode = sanitise_postcode(search_term)
        assert postcode == 'PL9 8TB'


if __name__ == '__main__':
    pytest.main()
