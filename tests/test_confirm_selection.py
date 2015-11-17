import os
import mock
from tests.fake_response import FakeResponse
from service.server import confirm_selection, api_client
from tests.test_search_request_interface import b_timestamp
from service import search_request_interface
from config import ROOT_DIR


fake_title_path = os.path.join(ROOT_DIR, os.path.normpath('tests/data/fake_title.json'))

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

class TestConfirmSelection:
    """
    Basic 'mock' checks of server.confirm_selection().

    Mocking for:
        * api_client.get_title (used by _get_register_title)
        * search_request_interface
    """

    # Get a fake title, for use by mocked api_client.get_title().
    # N.B.: fake_title is a class-level variable, as 'pytest' discourages the use of __init__()!
    fake_title = open(fake_title_path).readlines()      # (May raise an error; handled by pytest).

    # TODO: invoke 'confirm_selection()'

    # Use tests/data/fake_title.json as a dummy title.
    @mock.patch.object(api_client, 'get_title', return_value=fake_title)
    @mock.patch.object(search_request_interface.requests, 'post', return_value=FakeResponse(b_timestamp, 201))
    def test_confirm_selection_renders_valid_form(self, mock_title, mock_post):
        result = confirm_selection("DN1000", "LU1 1DZ")


if __name__ == '__main__':
    result = TestConfirmSelection()
    import pdb; pdb.set_trace()
