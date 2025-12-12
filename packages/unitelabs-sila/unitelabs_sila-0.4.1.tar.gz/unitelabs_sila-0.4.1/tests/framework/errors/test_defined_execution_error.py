import re
import textwrap

import pytest

from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.serializer import Serializer
from sila.framework.identifiers.error_identifier import ErrorIdentifier


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = DefinedExecutionError("Defined Execution Error.")

        # Assert that the method returns the correct value
        assert error.message == "Defined Execution Error."


class TestCreate:
    async def test_should_raise_on_invalid_identifier(self):
        # Create error
        with pytest.raises(
            ValueError, match=re.compile("Identifier must start with an upper-case letter, received ''.")
        ):
            DefinedExecutionError.create(identifier="", display_name="Error")

    async def test_should_raise_on_invalid_display_name(self):
        # Create error
        with pytest.raises(ValueError, match=re.compile("Display name must not be empty, received ''.")):
            DefinedExecutionError.create(identifier="Error", display_name="")

    async def test_should_create_error(self):
        # Create error
        error = DefinedExecutionError.create(
            identifier="TestError", display_name="Test Error", description="Test Error."
        )

        # Assert that the method returns the correct value
        assert issubclass(error, DefinedExecutionError)
        assert error.identifier == "TestError"
        assert error.display_name == "Test Error"
        assert error.description == "Test Error."


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create error
        error = DefinedExecutionError.create("MyError", "My Error")()

        # Assert that the method returns the correct value
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for DefinedExecutionError "
                "'MyError' without feature association."
            ),
        ):
            assert error.fully_qualified_identifier

    async def test_should_get_fully_qualified_identifier(self):
        # Create error
        error = DefinedExecutionError.create("MyError", "My Error")().with_feature(
            "org.silastandard/core/SiLAService/v1"
        )

        # Assert that the method returns the correct value
        assert error.fully_qualified_identifier == ErrorIdentifier(
            "org.silastandard/core/SiLAService/v1/DefinedExecutionError/MyError"
        )


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode error
        message = DefinedExecutionError.decode(b"")

        # Assert that the method returns the correct value
        assert message == DefinedExecutionError()

    async def test_should_decode_custom_buffer(self):
        # Create error
        error = DefinedExecutionError.create("UnimplementedFeature", "Unimplemented Feature")("Unimplemented Feature.")
        buffer = (
            b"\x12\x6b\x0a\x4forg.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature"
            b"\x12\x16Unimplemented Feature.\x18\x00"
        )

        # Decode error
        message = SiLAError.decode(buffer)

        # Assert that the method returns the correct value
        assert isinstance(message, DefinedExecutionError)
        assert message == error
        assert (
            message.fully_qualified_identifier
            == "org.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature"
        )

    async def test_should_decode_multiple_fields(self):
        # Decode error
        message = DefinedExecutionError.decode(b"\x12\x05Hello\x12\x05World")

        # Assert that the method returns the correct value
        assert message == DefinedExecutionError("World")

    async def test_should_decode_limited_buffer(self):
        # Decode error
        message = DefinedExecutionError.decode(
            b"\x12\x05Hello\x12\x05World",
            len(b"\x12\x05Hello"),
        )

        # Assert that the method returns the correct value
        assert message == DefinedExecutionError("Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode error
        message = DefinedExecutionError().encode()

        # Assert that the method returns the correct value
        assert message == b"\x12\x00"

    async def test_should_encode_custom_values(self):
        # Encode error
        message = (
            DefinedExecutionError.create("UnimplementedFeature", "Unimplemented Feature")("Unimplemented Feature.")
            .with_feature("org.silastandard/core/SiLAService/v1")
            .encode()
        )

        # Assert that the method returns the correct value
        assert message == (
            b"\x12\x69\x0a\x4forg.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature"
            b"\x12\x16Unimplemented Feature."
        )

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x12\x00", id="default"),
            pytest.param(2, b"\x12\x02\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode error
        error = DefinedExecutionError()
        message = error.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_xml(self):
        # Create error
        error = DefinedExecutionError.create(
            identifier="DefinedExecutionError",
            display_name="Defined Execution Error",
            description="Defined Execution Error.",
        )

        # Serialize
        xml = Serializer.serialize(error.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DefinedExecutionError>
              <Identifier>DefinedExecutionError</Identifier>
              <DisplayName>Defined Execution Error</DisplayName>
              <Description>Defined Execution Error.</Description>
            </DefinedExecutionError>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_xml(self):
        # Create xml
        xml = """
            <DefinedExecutionError>
              <Identifier>DefinedExecutionError</Identifier>
              <DisplayName>Defined Execution Error</DisplayName>
              <Description>Defined Execution Error.</Description>
            </DefinedExecutionError>
            """

        # Deserialize
        data_type = Deserializer.deserialize(xml, DefinedExecutionError.deserialize)

        # Assert that the method returns the correct value
        assert data_type.identifier == "DefinedExecutionError"
        assert data_type.display_name == "Defined Execution Error"
        assert data_type.description == "Defined Execution Error."

    async def test_should_extend_existing_custom(self):
        # Create xml
        error = DefinedExecutionError.create(identifier="DefinedExecutionError", display_name="DefinedExecutionError")
        xml = """
            <DefinedExecutionError>
              <Identifier>DefinedExecutionError</Identifier>
              <DisplayName>Defined Execution Error</DisplayName>
              <Description>Defined Execution Error.</Description>
            </DefinedExecutionError>
            """

        # Deserialize
        data_type = Deserializer.deserialize(
            xml,
            DefinedExecutionError.deserialize,
            {"definition": True, "error_definitions": {"DefinedExecutionError": error}},
        )

        # Assert that the method returns the correct value
        assert error == data_type
        assert error.identifier == "DefinedExecutionError"
        assert error.display_name == "Defined Execution Error"
        assert error.description == "Defined Execution Error."


class TestStringify:
    async def test_should_convert_to_string(self):
        # Create error
        error = DefinedExecutionError("Defined Execution Error.")

        # Assert that the method returns the correct value
        assert str(error) == "Defined Execution Error."


class TestEquality:
    def test_should_be_true_on_equal_type(self):
        # Create error
        error_0 = DefinedExecutionError("Defined Execution Error.")
        error_1 = DefinedExecutionError("Defined Execution Error.")

        # Compare equality
        assert error_0 == error_1

    def test_should_be_false_on_unequal_type(self):
        # Create error
        error_0 = DefinedExecutionError("Defined Execution Error.")
        error_1 = UndefinedExecutionError("Defined Execution Error.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_message(self):
        # Create error
        error_0 = DefinedExecutionError("Defined Execution Error.")
        error_1 = DefinedExecutionError("Another Execution Error.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_non_sila_error(self):
        # Create error
        error = DefinedExecutionError("Defined Execution Error.")

        # Compare equality
        assert error != Exception()
