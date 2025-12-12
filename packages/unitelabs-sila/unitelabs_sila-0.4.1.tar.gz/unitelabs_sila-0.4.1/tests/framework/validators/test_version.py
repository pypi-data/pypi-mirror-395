import re
import typing

import pytest

from sila.framework.validators.version import VersionLevel, check_version


class TestCheckVersion:
    def test_should_raise_on_optional_more_detailed_than_required(self):
        with pytest.raises(ValueError, match=re.escape("Optional level can not be less detailed than required level.")):
            check_version("1", required=VersionLevel.MINOR, optional=VersionLevel.MAJOR)

    @pytest.mark.parametrize(
        ["required", "optional", "version"],
        [
            (VersionLevel.MAJOR, None, "1"),
            (VersionLevel.MAJOR, None, "2"),
            (VersionLevel.MAJOR, None, "123"),
            (VersionLevel.MAJOR, VersionLevel.MINOR, "1"),
            (VersionLevel.MAJOR, VersionLevel.MINOR, "0.1"),
            (VersionLevel.MAJOR, VersionLevel.PATCH, "1"),
            (VersionLevel.MAJOR, VersionLevel.PATCH, "1.23"),
            (VersionLevel.MAJOR, VersionLevel.PATCH, "1.23.456"),
            (VersionLevel.MINOR, None, "1.23"),
            (VersionLevel.MINOR, VersionLevel.PATCH, "1.23"),
            (VersionLevel.MINOR, VersionLevel.PATCH, "1.23.456"),
            (VersionLevel.PATCH, None, "1.23.456"),
            (VersionLevel.MAJOR, VersionLevel.LABEL, "1"),
            (VersionLevel.MAJOR, VersionLevel.LABEL, "1.23"),
            (VersionLevel.MAJOR, VersionLevel.LABEL, "1.23.456"),
            (VersionLevel.MAJOR, VersionLevel.LABEL, "1.23.456_mighty_lab_devices"),
            (VersionLevel.LABEL, None, "1.23.456_mighty_lab_devices"),
        ],
    )
    def test_should_validate_version(
        self, required: VersionLevel, optional: typing.Optional[VersionLevel], version: str
    ):
        assert check_version(version, required=required, optional=optional) is version

    @pytest.mark.parametrize(
        ["required", "optional", "version"],
        [
            (VersionLevel.MAJOR, None, None),
            (VersionLevel.MAJOR, None, 123),
            (VersionLevel.MAJOR, None, ""),
            (VersionLevel.MAJOR, None, "a"),
            (VersionLevel.MAJOR, None, "1.0"),
            (VersionLevel.MAJOR, VersionLevel.MINOR, "1.0.0"),
            (VersionLevel.MINOR, None, "1"),
            (VersionLevel.MINOR, None, "1.23.456"),
            (VersionLevel.PATCH, None, "1"),
            (VersionLevel.PATCH, None, "1.23"),
            (VersionLevel.LABEL, None, "1"),
            (VersionLevel.LABEL, None, "1.23"),
            (VersionLevel.LABEL, None, "1.23.456"),
            (VersionLevel.LABEL, None, "1.23.456_build+test"),
        ],
    )
    def test_should_raise_on_invalid_version(
        self, required: VersionLevel, optional: typing.Optional[VersionLevel], version: str
    ):
        with pytest.raises(ValueError):
            check_version(version, required=required, optional=optional)
