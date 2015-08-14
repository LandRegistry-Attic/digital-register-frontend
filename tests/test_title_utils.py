from service import title_utils


class TestTitleUtils:

    def test_is_caution_title_returns_true_when_caution_title_info_true(self):
        title = {'is_caution_title': True}
        assert title_utils.is_caution_title(title) is True

    def test_is_caution_title_returns_false_when_caution_title_info_false(self):
        title = {'is_caution_title': False}
        assert title_utils.is_caution_title(title) is False

    def test_is_caution_title_returns_false_when_caution_title_info_absent(self):
        title = {}
        assert title_utils.is_caution_title(title) is False
