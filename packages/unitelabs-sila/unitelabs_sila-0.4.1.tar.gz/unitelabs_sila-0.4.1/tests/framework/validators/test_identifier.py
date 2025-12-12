import pytest

from sila.framework.validators.identifier import check_identifier


class TestCheckIdentifier:
    @pytest.mark.parametrize(
        ["identifier"],
        [
            ("SiLAService",),
            ("GetFeatureDefinition",),
            ("UnimplementedFeature",),
            ("A",),
            ("Z" * 255,),
        ],
    )
    def test_should_validate_identifier(self, identifier: str):
        assert check_identifier(identifier) is identifier

    @pytest.mark.parametrize(
        ["identifier"],
        [
            (None,),
            (123,),
            ("",),
            ("a",),
            ("Z" * 256,),
            ("A.",),
            ("B-",),
            ("0A",),
        ],
    )
    def test_should_raise_on_invalid_identifier(self, identifier: str):
        with pytest.raises(ValueError):
            check_identifier(identifier)
