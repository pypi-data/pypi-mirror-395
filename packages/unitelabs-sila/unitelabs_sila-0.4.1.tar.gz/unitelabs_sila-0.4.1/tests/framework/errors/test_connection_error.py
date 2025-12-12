from sila.framework.errors.connection_error import SiLAConnectionError


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = SiLAConnectionError("Connection Error.")

        # Assert that the method returns the correct value
        assert error.message == "Connection Error."
