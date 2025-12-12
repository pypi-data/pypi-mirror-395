import pytest

from sila.framework.validators.display_name import check_display_name


class TestCheckDisplayName:
    @pytest.mark.parametrize(
        ["display_name"],
        [
            ("SiLA Service",),
            ("Get Feature Definition",),
            ("Server UUID",),
            ("Version",),
        ],
    )
    def test_should_validate_display_name(self, display_name: str):
        assert check_display_name(display_name) is display_name

    @pytest.mark.parametrize(
        ["display_name"],
        [
            (None,),
            (123,),
            ("",),
            ("z" * 256,),
        ],
    )
    def test_should_raise_on_invalid_display_name(self, display_name: str):
        with pytest.raises(ValueError):
            check_display_name(display_name)
