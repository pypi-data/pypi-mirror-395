import pytest

from sila.framework.validators.url import check_url


class TestCheckUrl:
    @pytest.mark.parametrize(
        ["url"],
        [
            ("http://sila-standard.com",),
            ("https://sila-standard.com",),
        ],
    )
    def test_should_validate_url(self, url: str):
        assert check_url(url) is url

    @pytest.mark.parametrize(
        ["url"],
        [
            (None,),
            (123,),
            ("",),
            ("sila-standard.com",),
        ],
    )
    def test_should_raise_on_invalid_url(self, url: str):
        with pytest.raises(ValueError):
            check_url(url)
