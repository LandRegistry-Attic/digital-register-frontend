from unittest import mock
from _pytest.python import raises
import requests
from config import CONFIG_DICT
from tests.fake_response import FakeResponse

from service import api_client


class TestApiClient:

    @mock.patch.object(requests, 'get', return_value=FakeResponse(b'', 404))
    def test_get_official_copy_data_calls_the_right_api_endpoint(self, mock_get):
        title_number = 'title123'

        api_client.get_official_copy_data(title_number)
        mock_get.assert_called_once_with(
            '{}titles/title123/official-copy'.format(CONFIG_DICT['REGISTER_TITLE_API'])
        )

    @mock.patch.object(requests, 'get', return_value=FakeResponse(b'{"some": "json"}', 200))
    def test_get_official_copy_data_returns_json_from_api_when_response_is_200(self, mock_get):
        result = api_client.get_official_copy_data('title123')
        assert result == {'some': 'json'}

    @mock.patch.object(requests, 'get', return_value=FakeResponse(b'not a json', 200))
    def test_get_official_copy_data_throws_exception_when_200_response_body_is_not_json(
            self, mock_get):

        with raises(Exception) as e:
            api_client.get_official_copy_data('title123')

        assert 'API response body is not JSON' in str(e)

    @mock.patch.object(requests, 'get', return_value=FakeResponse(b'', 404))
    def test_get_official_copy_data_returns_none_when_api_returns_404_response(self, mock_get):
        result = api_client.get_official_copy_data('title123')
        assert result is None

    @mock.patch.object(requests, 'get', return_value=FakeResponse(b'', 500))
    def test_get_official_copy_data_throws_exception_when_api_returns_500_response(
            self, mock_get):

        with raises(Exception) as e:
            api_client.get_official_copy_data('title123')

        assert 'API returned an unexpected response (500)' in str(e)
