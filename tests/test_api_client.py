from service.api_client import requests
from datetime import datetime
from unittest import mock
from _pytest.python import raises
from config import CONFIG_DICT
from tests.fake_response import FakeResponse
from service import api_client, app


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
    def test_get_official_copy_data_throws_exception_when_200_response_body_is_not_json(self, mock_get):

        with raises(Exception) as e:
            api_client.get_official_copy_data('title123')

        assert 'API response body is not JSON' in str(e)

    @mock.patch.object(requests, 'get', return_value=FakeResponse(b'', 404))
    def test_get_official_copy_data_returns_none_when_api_returns_404_response(self, mock_get):
        result = api_client.get_official_copy_data('title123')
        assert result is None

    @mock.patch.object(requests, 'get', return_value=FakeResponse(b'', 500))
    def test_get_official_copy_data_throws_exception_when_api_returns_500_response(self, mock_get):

        with raises(Exception) as e:
            api_client.get_official_copy_data('title123')

        assert 'API returned an unexpected response (500)' in str(e)


    # api_client.save_search_request() ...
    cart_id = '5e1577160107a635dfb9c1d31089cad3ee3fd99a'

    @mock.patch.object(requests, 'post', return_value=FakeResponse(bytes(cart_id, 'utf-8'), 200))
    def test_save_search_request_returns_cart_id_from_api_when_response_is_200(self, mock_post):

        params = dict()
        response = api_client.save_search_request(params)

        assert self.cart_id == response.text


    @mock.patch.object(requests, 'post', return_value=FakeResponse(bytes(cart_id, 'utf-8'), 200))
    def test_save_search_request_calls_the_right_api_endpoint(self, mock_post):

        url = '{}save_search_request'.format(CONFIG_DICT['REGISTER_TITLE_API'])

        params = dict()
        api_client.save_search_request(params)

        mock_post.assert_called_once_with(url, data=params)
