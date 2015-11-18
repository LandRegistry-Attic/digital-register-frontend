import os
import pytest  # type: ignore
import json
from unittest import mock
from tests.fake_response import FakeResponse
from service.server import confirm_selection, api_client, app, _get_register_title
from tests.test_search_request_interface import b_timestamp
from service import search_request_interface
from config import ROOT_DIR


search_results_html = \
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>

<h1 class="heading-xlarge collapse-bottom">"Search Results"</h1>

<div class="grid-row">
    <div class="column-two-thirds">
    <br/>
        <a href="{{ url_for('confirm_selection', title_number=title['title_number'], search_term='PL6 1XX'">"Dummy address ..."</a>
    </div>

</div>

</body>
</html>
"""
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


if __name__ == '__main__':
    pytest.main()
