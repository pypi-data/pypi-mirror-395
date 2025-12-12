import re

import pytest

from sila.framework.protobuf.encode_error import EncodeError


class TestInitialize:
    def test_should_initialize(self):
        # Create error
        error = EncodeError(message="Encode Error Reason")

        # Assert that the method returns the correct value
        assert error.message == "Encode Error Reason"

    def test_should_be_instance_of_exception(self):
        # Create error
        error = EncodeError(message="Encode Error Reason")

        # Assert that the method returns the correct value
        assert isinstance(error, Exception)

    def test_should_raise_error(self):
        # Create error
        error = EncodeError(message="Encode Error Reason")

        # Assert that the method returns the correct value
        with pytest.raises(EncodeError, match=re.escape("Encode Error Reason")):
            raise error
