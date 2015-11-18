"""
US107 (log in)
These tests are for US107 only, so tests for PDF and title are not present.
"""

import json
import pytest
from unittest import mock
from werkzeug.datastructures import Headers
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

with open('tests/data/official_copy_response.json', 'r') as official_copy_response_file:
    official_copy_response = json.loads(official_copy_response_file.read())

unavailable_title = FakeResponse('', 404)

# DM US107
class TestSearchTerm:

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
        response = self.app.post('/title-search', data={'search_term': 'DN1000'}, follow_redirects=True, headers=self.headers)
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
        self.app.get('/title-search/search term', follow_redirects=True, headers=self.headers)
        audit_text = "SEARCH REGISTER: '{}' was searched by {}".format(search_term, TEST_USERNAME)
        mock_audit.assert_called_once_with(audit_text)

    @mock.patch('requests.get', return_value=unavailable_title)
    def test_title_search_title_not_found(self, mock_get):
        response = self.app.post('/title-search', data={'search_term': 'DT1000'}, follow_redirects=True)
        assert '0 results found' in response.data.decode()

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

class TestAuthenticated:
    """
    Put webseal header in HTTP headers, request page and ensure that username
    page element is present in response (see layout.html)
    """
    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    def test_authenticated(self):
        """ Does header contain 'iv-user' username field? """
        response = self.app.get('/title-search/plymouth', headers=self.headers)
        assert response.status_code == 200
        assert 'username' in str(response.data)

if __name__ == '__main__':
    pytest.main()
