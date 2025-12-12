import pytest

from sila.framework.validators.uuid import check_uuid


class TestCheckUuid:
    @pytest.mark.parametrize(
        ["uuid"],
        [
            ("00000000-0000-0000-0000-000000000000",),
        ],
    )
    def test_should_validate_uuid(self, uuid: str):
        assert check_uuid(uuid) is uuid

    @pytest.mark.parametrize(
        ["uuid"],
        [
            (None,),
            (123,),
            ("",),
        ],
    )
    def test_should_raise_on_invalid_uuid(self, uuid: str):
        with pytest.raises(ValueError):
            check_uuid(uuid)
