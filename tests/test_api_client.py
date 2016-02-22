import unittest
from unittest import mock
from _pytest.python import raises
from tests.fake_response import FakeResponse
from service import api_client


class TestApiClient(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register_title_api_url = api_client.REGISTER_TITLE_API_URL.rstrip('/')


class TestGetOfficialCopyData(TestApiClient):

    @mock.patch.object(api_client.requests, 'get', return_value=FakeResponse(b'', 404))
    def test_get_official_copy_data_calls_the_right_api_endpoint(self, mock_get):
        title_number = 'title123'

        api_client.get_official_copy_data(title_number)
        mock_get.assert_called_once_with('{}/titles/title123/official-copy'.format(self.register_title_api_url))

    @mock.patch.object(api_client.requests, 'get', return_value=FakeResponse(b'{"some": "json"}', 200))
    def test_get_official_copy_data_returns_json_from_api_when_response_is_200(self, mock_get):
        result = api_client.get_official_copy_data('title123')
        assert result == {'some': 'json'}

    @mock.patch.object(api_client.requests, 'get', return_value=FakeResponse(b'not a json', 200))
    def test_get_official_copy_data_throws_exception_when_200_response_body_is_not_json(self, mock_get):

        with raises(Exception) as e:
            api_client.get_official_copy_data('title123')

        assert 'API response body is not JSON' in str(e)

    @mock.patch.object(api_client.requests, 'get', return_value=FakeResponse(b'', 404))
    def test_get_official_copy_data_returns_none_when_api_returns_404_response(self, mock_get):
        result = api_client.get_official_copy_data('title123')
        assert result is None

    @mock.patch.object(api_client.requests, 'get', return_value=FakeResponse(b'', 500))
    def test_get_official_copy_data_throws_exception_when_api_returns_500_response(self, mock_get):

        with raises(Exception) as e:
            api_client.get_official_copy_data('title123')

        assert 'API returned an unexpected response (500)' in str(e)


class TestSaveSearchRequest(TestApiClient):

    cart_id = '5e1577160107a635dfb9c1d31089cad3ee3fd99a'
    data = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = '{}/save_search_request'.format(self.register_title_api_url)

    def make_api_call(self, params=data):
        return api_client.save_search_request(params)

    @mock.patch.object(api_client.requests, 'post', return_value=FakeResponse(bytes(cart_id, 'utf-8'), 200))
    def test_save_search_request_returns_cart_id_from_api_when_response_is_200(self, mock_post):

        response = self.make_api_call()

        assert self.cart_id == response.text

    @mock.patch.object(api_client.requests, 'post', return_value=FakeResponse(bytes(cart_id, 'utf-8'), 200))
    def test_save_search_request_calls_the_right_api_endpoint(self, mock_post):

        self.make_api_call()

        mock_post.assert_called_once_with(self.url, data=self.data)

    # Derived from http://engineroom.trackmaven.com/blog/real-life-mocking ...
    # Note: "autospec=True" ensures that we match the mocked object's attributes.
    @mock.patch('service.error_handler.error_handler', autospec=True)
    @mock.patch('service.api_client.requests.post', autospec=True)
    def test_save_search_request_http_error(self, mock_post, mock_http_error_handler):
        """
        Test getting an HTTP error.
        """

        # Construct our mock response object, giving it relevant expected behaviours.
        mock_response = mock.Mock()
        http_error = api_client.requests.exceptions.HTTPError
        mock_response.raise_for_status.side_effect = http_error()

        # Assign our mock response as the result of our patched function
        mock_post.return_value = mock_response

        with self.assertRaises(http_error):

            self.make_api_call()

            # Check that our function made the expected internal calls
            mock_post.assert_called_once_with(self.url, data=self.data)
            self.assertEqual(1, mock_response.raise_for_status.call_count)

            # Make sure we did not attempt to deserialize the response
            self.assertEqual(0, mock_response.json.call_count)

            # Make sure our HTTP error handler is called
            mock_http_error_handler.assert_called_once_with(http_error)
