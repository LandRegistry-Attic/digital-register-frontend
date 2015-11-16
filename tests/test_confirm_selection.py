from unittest import mock
from tests.fake_response import FakeResponse
from service.server import confirm_selection, _get_register_title


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
    """

    # TODO: mock '_get_register_title()', to use 'fake_title.json'
    # TODO: invoke 'confirm_selection()'
    # TODO: continue to WP interface

    # Use tests/data/fake_title.json as a dummy title.
    @mock.patch.object(search_request_interface.requests, 'post', return_value=FakeResponse(b_timestamp, 201))
    def test_property_search_interface_returns_datetime_string_from_api_when_response_is_201(self, mock_post):
        result = search_request_interface.insert('title123', '1.20', '00 Test Road, Test Town, Plymouth, PL1 1AB')
        assert result == self.timestamp

    @mock.patch.object(search_request_interface.requests, 'post', return_value=FakeResponse(None, 200))
    def test_property_search_interface_returns_none_from_api_when_response_is_200(self, mock_post):
        result = search_request_interface.update("MGIRDLER", self.timestamp, "2123652039 ")
        assert result is None
