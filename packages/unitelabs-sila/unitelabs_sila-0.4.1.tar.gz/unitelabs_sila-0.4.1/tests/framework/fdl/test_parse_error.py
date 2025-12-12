from sila.framework.fdl.parse_error import ParseError


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = ParseError("Decode Error Reason", path=["Root", "Element"], line=2, column=16)

        # Assert that the method returns the correct value
        assert error.message == "Decode Error Reason"
        assert error.path == ["Root", "Element"]
        assert error.line == 2
        assert error.column == 16


class TestStringify:
    async def test_should_convert_to_string(self):
        # Create error
        error = ParseError("Decode Error Reason", path=["Root", "Element"])

        # Assert that the method returns the correct value
        assert str(error) == "Decode Error Reason"
