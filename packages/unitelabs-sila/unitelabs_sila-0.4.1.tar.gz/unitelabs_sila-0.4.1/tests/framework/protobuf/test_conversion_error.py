import re

import pytest

from sila.framework.protobuf.conversion_error import ConversionError


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = ConversionError("Conversion Error Reason", path=["Root", "Element"])

        # Assert that the method returns the correct value
        assert error.message == "Conversion Error Reason"
        assert error.path == ["Root", "Element"]

    async def test_should_initialize_custom_path(self):
        # Create error
        error = ConversionError(message="Decode Error Reason", path=["key1", 0, "key2"])

        # Assert that the method returns the correct value
        assert error.message == "Decode Error Reason"
        assert error.path == ["key1", 0, "key2"]

    def test_should_be_instance_of_exception(self):
        # Create error
        error = ConversionError(message="Decode Error Reason")

        # Assert that the method returns the correct value
        assert isinstance(error, Exception)

    def test_should_raise_error(self):
        # Create error
        error = ConversionError(message="Decode Error Reason")

        # Assert that the method returns the correct value
        with pytest.raises(ConversionError, match=re.escape("Decode Error Reason")):
            raise error
