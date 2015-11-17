import datetime
from unittest.mock import patch
from tests.fake_response import FakeResponse
from service import search_request_interface


timestamp = str(datetime.datetime.now())       # This has the same format as the DB2 version.
b_timestamp = bytes(timestamp, 'utf-8')        # 'bytes' required for Mock.

# Mocked functions ...
@patch.object(search_request_interface.requests, 'post', return_value=FakeResponse(b_timestamp, 201))
def _mock_insert(mock_post):
    return search_request_interface.insert('title123', '1.20', '00 Test Road, Test Town, Plymouth, PL1 1AB')

@patch.object(search_request_interface.requests, 'post', return_value=FakeResponse(None, 200))
def _mock_update(mock_post):
    return search_request_interface.update("MGIRDLER", timestamp, "2123652039 ")


class TestPropertySearchInterface:
    """
    Basic 'mock' checks of "Property Search Interface"

    N.B. DB service only returns status codes of 200 (update) or 201 (insert).
    """

    # Tests proper ...
    def test_property_search_interface_returns_datetime_string_from_api_when_response_is_201(self):
        assert _mock_insert() == timestamp

    def test_property_search_interface_returns_none_from_api_when_response_is_200(self):
        assert _mock_update() is None
