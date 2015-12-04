import os
import pytest  # type: ignore
import mock
from tests.fake_response import FakeResponse
from service.server import app
from tests.test_search_request_interface import b_timestamp
from service import search_request_interface
from config import ROOT_DIR
from werkzeug.datastructures import Headers  # type: ignore


# Get a fake title, for use by mocked api_client.get_title().
fake_title_path = os.path.join(ROOT_DIR, os.path.normpath('tests/data/fake_title.json'))
fake_title = open(fake_title_path).read()                       # (May raise an error; handled by pytest).
fake_response = FakeResponse(str.encode(fake_title), 200)       # N.B. Response.content is 'bytes'.

TEST_USERNAME = 'username1'

class TestConfirmSelection:
    """
    Basic 'mock' checks of server.confirm_selection().

    Mocking for:
        * api_client.get_title (used by _get_register_title)
        * search_request_interface
    """
    def setup_class(cls):
        cls.app = app.test_client()

    def setup_method(self, method):
        self.app = app.test_client()
        self.headers = Headers([('iv-user', TEST_USERNAME)])

    # Use tests/data/fake_title.json as a dummy title.
    @mock.patch('service.server.api_client.get_title', return_value=fake_response.json())
    @mock.patch.object(search_request_interface.requests, 'post', return_value=FakeResponse(b_timestamp, 201))
    def test_confirm_selection_renders_valid_form_when_response_is_200(self, mock_get, mock_post):
        response = self.app.get('/confirm-selection/DN1000/LU1%201DZ', headers=self.headers)
        assert response.status_code == 200

        page_content = response.data.decode()
        hidden_lines = [line for line in page_content.splitlines() if 'hidden' in line]
        hidden_text = '\n'.join(hidden_lines)

        price_value = app.config['TITLE_REGISTER_SUMMARY_PRICE']

        # TODO: get (and compare) 'cartId' value
        assert 'name="cartId" value="' in hidden_text
        assert 'name="amount" value="{}"'.format(price_value) in hidden_text
        assert 'name="MC_timestamp" value="' + b_timestamp.decode("utf-8") in hidden_text
        assert 'name="MC_titleNumber" value="DN1000"' in hidden_text
        assert 'name="MC_purchaseType" value="summaryView"' in hidden_text
        assert 'name="MC_searchType" value="A"' in hidden_text

if __name__ == '__main__':
    from flask_wtf.csrf import CsrfProtect

    CsrfProtect(app)

    # Invoke 'pytest' as if from command line: python3 tests/test_confirm_selection.py
    # [Requires '. ./environment.sh' beforehand].
    pytest.main('-x --pdb {}'.format(__file__))
