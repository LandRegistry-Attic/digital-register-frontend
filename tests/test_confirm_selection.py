import os
import pytest  # type: ignore
from unittest import mock
from tests.fake_response import FakeResponse
from service.server import confirm_selection, api_client, app, _get_register_title
from tests.test_search_request_interface import b_timestamp
from service import search_request_interface
from config import ROOT_DIR


# Get a fake title, for use by mocked api_client.get_title().
fake_title_path = os.path.join(ROOT_DIR, os.path.normpath('tests/data/fake_title.json'))
fake_title = open(fake_title_path).read()                       # (May raise an error; handled by pytest).
fake_response = FakeResponse(str.encode(fake_title), 200)       # N.B. Response.content is 'bytes'.


class TestConfirmSelection:
    """
    Basic 'mock' checks of server.confirm_selection().

    Mocking for:
        * api_client.get_title (used by _get_register_title)
        * search_request_interface
    """
    def setup_class(cls):
        cls.app = app.test_client()

    # Use tests/data/fake_title.json as a dummy title.
    @mock.patch('service.server.api_client.get_title', return_value=fake_response.json())
    @mock.patch.object(search_request_interface.requests, 'post', return_value=FakeResponse(b_timestamp, 201))
    def test_confirm_selection_renders_valid_form_when_response_is_200(self, mock_get, mock_post):
        response = self.app.get('/confirm-selection/DN1000/LU1%201DZ')

        assert response.status_code == 200

        page_content = response.data.decode()
        hidden_lines = [line for line in page_content.splitlines() if 'hidden' in line]
        hidden_text = '\n'.join(hidden_lines)

        price_value = app.config['TITLE_REGISTER_SUMMARY_PRICE'].split(';')[1]

        # TODO: get (and compare) 'cartId' value
        assert 'id="title_number" value="DN1000"' in hidden_text
        assert 'id="price" value="&amp;pound;1.20 (incl. VAT)"' in hidden_text
        assert 'id="address_lines" value="[&#39;17 Hazelbury Crescent&#39;,' in hidden_text
        assert 'name="cartId" value="' in hidden_text
        assert 'name="amount" value="&amp;pound;{}"'.format(price_value) in hidden_text
        assert 'name="MC_timestamp" value="' + b_timestamp.decode("utf-8") in hidden_text
        assert 'name="MC_titleNumber" value="DN1000"' in hidden_text
        assert 'name="MC_purchaseType" value="registerOnly"' in hidden_text
        assert 'name="MC_searchType" value="D"' in hidden_text


if __name__ == '__main__':
    from flask_wtf.csrf import CsrfProtect

    CsrfProtect(app)

    # Invoke 'pytest' as if from command line: python3 tests/test_confirm_selection.py
    # [Requires '. ./environment.sh' beforehand].
    pytest.main('-x --pdb {}'.format(__file__))
