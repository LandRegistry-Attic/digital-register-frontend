import mock

from service import template_filters


class TestTemplateFilters:
    def test_format_date_returns_correctly_formatted_date(self):
        formatted_date = template_filters.format_date('2015-08-15T12:23:45')
        assert formatted_date == '15 August 2015'

    def test_format_time_returns_correctly_formatted_time(self):
        formatted_time = template_filters.format_time('2015-08-15T12:23:45')
        assert formatted_time == '12:23:45'

    def test_pluralize_returns_given_singular_string_when_number_is_one(self):
        assert template_filters.pluralize(1, singular='singular') == 'singular'

    def test_pluralize_returns_empty_string_for_one_when_singular_not_set(self):
        assert template_filters.pluralize(1) == ''

    def test_pluralize_returns_given_plural_string_when_number_not_one(self):
        plural = 'plural'
        assert template_filters.pluralize(0, plural=plural) == plural
        assert template_filters.pluralize(2, plural=plural) == plural
        assert template_filters.pluralize(3, plural=plural) == plural

    def test_pluralize_returns_default_string_when_plural_not_set(self):
        assert template_filters.pluralize(0) == 's'
        assert template_filters.pluralize(2) == 's'
        assert template_filters.pluralize(3) == 's'

    def test_check_date_existence_returns_given_date_when_present(self):
        assert template_filters.check_date_existence('2015-03-02') == '2015-03-02'

    def test_check_date_existence_returns_default_string_when_date_absent(self):
        assert template_filters.check_date_existence('') == ' Not Dated '
        assert template_filters.check_date_existence(None) == ' Not Dated '

    @mock.patch('service.title_utils.is_caution_title', return_value=True)
    def test_tenure_info_returns_caution_info_when_caution_title(self, mock_is_caution_title):
        tenure_info = template_filters.get_tenure_info({'data': 'title_data'})
        assert tenure_info == 'Caution against first registration'

    @mock.patch('service.title_utils.is_caution_title', return_value=False)
    def test_tenure_info_returns_tenure_when_not_caution_title(self, mock_is_caution_title):
        tenure = 'tenure123'
        tenure_info = template_filters.get_tenure_info({'data': {'tenure': tenure}})
        assert tenure_info == tenure

    def test_strip_illegal_characters_filters_out_all_and_only_illegal_characters(self):
        stripped = template_filters.strip_illegal_characters('Az09_;:-,.()&£ !@#$%^*{}')
        assert stripped == 'Az09_;:-,.()&£ '

    def test_get_all_filters_returns_filter_information(self):
        filters = template_filters.get_all_filters()

        assert len(filters) == 6
        assert filters.get('date') == template_filters.format_date
        assert filters.get('time') == template_filters.format_time
        assert filters.get('pluralize') == template_filters.pluralize
        assert filters.get('check_date_existence') == template_filters.check_date_existence
        assert filters.get('strip_illegal_characters') == template_filters.strip_illegal_characters
        assert filters.get('tenure_info') == template_filters.get_tenure_info
