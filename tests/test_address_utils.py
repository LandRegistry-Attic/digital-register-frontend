from service.address_utils import get_address_lines


class TestAddressUtils:

    def test_unknown_address_formatting(self):
        address_string = "No formatting in address"
        address_dict = {"address_string": address_string}
        lines = get_address_lines(address_dict)
        assert lines == [address_string]

    def test_foreign_address_formatting(self):
        address_string = "No formatting in address"
        address_dict = {
            "address_string": address_string,
            "address_type": "BFPO",
            "foreign_bfpo_address1": "Foreign BFPO address",
            "country": "Country"
        }
        lines = get_address_lines(address_dict)
        assert lines == ["Foreign BFPO address", "Country"]

    def test_electronic_address_formatting(self):
        address_string = "No formatting in address"
        address_dict = {"address_string": address_string,
                        "address_type": "ELECTRONIC",
                        "email_address": "test@test.com"}
        lines = get_address_lines(address_dict)
        assert lines == ["test@test.com"]

    def test_dx_address_formatting(self):
        address_string = "No formatting in address"
        address_dict = {
            "address_string": address_string,
            "address_type": "DX",
            "dx_no": "12345678",
            "exchange_name": "Exchange name"
        }
        lines = get_address_lines(address_dict)
        assert lines == ["12345678", "Exchange name"]

    def test_uk_address_formatting(self):
        address_dict = {
            "address_type": "UK",
            "care_of": "care of",
            "care_of_name": "Aslan",
            "house_no": "42",
            "house_alpha": "A",
            "street_name": "Magical Street",
            "postcode": "W1 2BT",
            "town": "Town Behind the Wardrobe",
            "sub_building_description": "Queen's Palace"
        }
        lines = get_address_lines(address_dict)
        assert lines == [
            "care of Aslan",
            "Queen's Palace",
            "42A Magical Street",
            "Town Behind the Wardrobe",
            "W1 2BT"
        ]
