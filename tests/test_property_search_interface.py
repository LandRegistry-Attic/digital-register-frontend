import requests
import datetime
from unittest import mock
from tests.fake_response import FakeResponse
from service import property_search_interface


class TestPropertySearchInterface:
    """
    Basic 'mock' checks of "Property Search Interface"

    N.B. DB service only returns status codes of 200 (update) or 201 (insert).
    """

    timestamp = str(datetime.datetime.now())       # This has the same format as the DB2 version.
    b_timestamp = bytes(timestamp, 'utf-8')        # 'bytes' required for Mock.

    @mock.patch.object(property_search_interface.requests, 'post', return_value=FakeResponse(b_timestamp, 201))
    def test_property_search_interface_returns_datetime_string_from_api_when_response_is_201(self, mock_post):
        result = property_search_interface.insert('title123', '1.20', '00 Test Road, Test Town, Plymouth, PL1 1AB')
        assert result == self.timestamp

    @mock.patch.object(property_search_interface.requests, 'post', return_value=FakeResponse(None, 200))
    def test_property_search_interface_returns_none_from_api_when_response_is_200(self, mock_post):
        result = property_search_interface.update("MGIRDLER", self.timestamp, "2123652039 ")
        assert result is None
