import re

import pytest

from sila.framework.protobuf.decode_error import DecodeError


class TestInitialize:
    async def test_should_initialize_error(self):
        # Create error
        error = DecodeError(message="Decode Error Reason", offset=5)

        # Assert that the method returns the correct value
        assert error.message == "Decode Error Reason"
        assert error.offset == 5
        assert error.path == []

    async def test_should_initialize_custom_path(self):
        # Create error
        error = DecodeError(message="Decode Error Reason", offset=5, path=["key1", 0, "key2"])

        # Assert that the method returns the correct value
        assert error.message == "Decode Error Reason"
        assert error.offset == 5
        assert error.path == ["key1", 0, "key2"]

    def test_should_be_instance_of_exception(self):
        # Create error
        error = DecodeError(message="Decode Error Reason", offset=5)

        # Assert that the method returns the correct value
        assert isinstance(error, Exception)

    def test_should_raise_error(self):
        # Create error
        error = DecodeError(message="Decode Error Reason", offset=5)

        # Assert that the method returns the correct value
        with pytest.raises(DecodeError, match=re.escape("Decode Error Reason")):
            raise error
