import unittest.mock

import pytest

from sila.framework.common.feature import Feature
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.framework_error import InvalidMetadata, NoMetadataAllowed
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.framework.errors.validation_error import ValidationError
from sila.server.server import Server
from sila.server.unobservable_command import UnobservableCommand
from sila.testing.raises import raises


class TestExecute:
    async def test_should_execute_unobservable_command(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/UnobservableCommandTest/v1/Command/CommandWithoutParametersAndResponses"
        )
        response = await unobservable_command.execute()

        # Assert that the method returns the correct value
        assert response == b""

    async def test_should_execute_unobservable_command_with_parameter(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString"
        )
        response = await unobservable_command.execute(request=Integer(12345).encode(number=1))

        # Assert that the method returns the correct value
        assert response == String("12345").encode(number=1)

    async def test_should_execute_unobservable_command_with_parameters(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/UnobservableCommandTest/v1/Command/JoinIntegerAndString"
        )
        response = await unobservable_command.execute(
            request=Integer(123).encode(number=1) + String("abc").encode(number=2)
        )

        # Assert that the method returns the correct value
        assert response == String("123abc").encode(number=1)

    async def test_should_execute_unobservable_command_with_responses(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/UnobservableCommandTest/v1/Command/SplitStringAfterFirstCharacter"
        )
        response = await unobservable_command.execute(request=String("abcde").encode(number=1))

        # Assert that the method returns the correct value
        assert response == String("a").encode(number=1) + String("bcde").encode(number=2)

    async def test_should_raise_on_invalid_protobuf(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString"
        )

        with pytest.raises(
            ValidationError,
            match=(
                r"Invalid field 'Integer' in message 'ConvertIntegerToString_Parameters': "
                r"Expected wire type 'VARINT', received 'LEN'\."
            ),
        ) as error:
            await unobservable_command.execute(request=String("abc").encode(number=1))

        assert (
            error.value.parameter
            == "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer"
        )

    async def test_should_raise_on_missing_parameter(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString"
        )

        with pytest.raises(
            ValidationError,
            match=r"Missing field 'Integer' in message 'ConvertIntegerToString_Parameters'\.",
        ) as error:
            await unobservable_command.execute()

        assert (
            error.value.parameter
            == "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer"
        )

    async def test_should_raise_defined_execution_error(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseDefinedExecutionError"
        )

        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await unobservable_command.execute()

    async def test_should_attach_defined_execution_error_to_feature(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseDefinedExecutionError"
        )

        def function(**kwargs):
            msg = "SiLA2_test_error_message"
            raise DefinedExecutionError.create(identifier="TestError", display_name="TestError")(msg)

        unobservable_command.function = function

        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await unobservable_command.execute()

    async def test_should_raise_undefined_execution_error(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseUndefinedExecutionError"
        )

        with pytest.raises(UndefinedExecutionError, match=r"SiLA2_test_error_message"):
            await unobservable_command.execute()

    async def test_should_catch_exceptions(self, server: Server):
        # Execute unobservable command
        feature = Feature(identifier="TestFeature", display_name="TestFeature")
        server.register_feature(feature)
        unobservable_command = UnobservableCommand(
            identifier="UnobservableCommand",
            display_name="Unobservable Command",
            function=unittest.mock.Mock(side_effect=ValueError("Invalid value received")),
            feature=feature,
        )

        with pytest.raises(UndefinedExecutionError, match=r"Invalid value received"):
            await unobservable_command.execute()

    async def test_should_intercept_metadata(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/MetadataConsumerTest/v1/Command/EchoStringMetadata"
        )
        response = await unobservable_command.execute(
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String("C").encode(
                    number=1
                )
            }
        )

        # Assert that the method returns the correct value
        assert response == String("C").encode(number=1)

    async def test_should_ignore_additional_metadata(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/UnobservableCommandTest/v1/Command/CommandWithoutParametersAndResponses"
        )
        response = await unobservable_command.execute(
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String().encode(number=1)
            }
        )

        # Assert that the method returns the correct value
        assert response == b""

    async def test_should_raise_on_unallowed_metadata(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/core/SiLAService/v1/Command/SetServerName"
        )

        with pytest.raises(NoMetadataAllowed, match=r"No metadata allowed for the SiLA Service feature\."):
            await unobservable_command.execute(
                metadata={"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": b""}
            )

    async def test_should_raise_on_invalid_metadata(self, server: Server):
        # Execute unobservable command
        unobservable_command = server.get_unobservable_command(
            "org.silastandard/test/MetadataConsumerTest/v1/Command/EchoStringMetadata"
        )

        with pytest.raises(
            InvalidMetadata,
            match=r"Missing metadata 'StringMetadata' in UnobservableCommand 'EchoStringMetadata'\.",
        ):
            await unobservable_command.execute(
                metadata={"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": b""}
            )


class TestExecuteRpcHandler:
    async def test_should_return_unobservable_command(self):
        # Execute unobservable command
        unobservable_command = UnobservableCommand(
            identifier="UnobservableCommand", display_name="Unobservable Command"
        )
        unobservable_command.execute = unittest.mock.AsyncMock(return_value=Integer(42).encode(number=1))
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        response = await unobservable_command.execute_rpc_handler(b"", context)

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_forward_parameters(self):
        # Execute unobservable command
        unobservable_command = UnobservableCommand(
            identifier="UnobservableCommand", display_name="Unobservable Command"
        )
        unobservable_command.execute = unittest.mock.AsyncMock()
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        await unobservable_command.execute_rpc_handler(String("Hello, World!").encode(number=1), context)

        # Assert that the method returns the correct value
        unobservable_command.execute.assert_awaited_once_with(String("Hello, World!").encode(number=1), {})

    async def test_should_forward_metadata(self):
        # Execute unobservable command
        unobservable_command = UnobservableCommand(
            identifier="UnobservableCommand", display_name="Unobservable Command"
        )
        unobservable_command.execute = unittest.mock.AsyncMock()
        context = unittest.mock.Mock(
            invocation_metadata=unittest.mock.Mock(
                return_value=[
                    (
                        "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin",
                        String().encode(number=1),
                    )
                ]
            )
        )
        await unobservable_command.execute_rpc_handler(b"", context)

        # Assert that the method returns the correct value
        unobservable_command.execute.assert_awaited_once_with(
            b"",
            {"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String().encode(number=1)},
        )

    async def test_should_raise_sila_error(self):
        # Execute unobservable command
        unobservable_command = UnobservableCommand(
            identifier="UnobservableCommand", display_name="Unobservable Command"
        )
        unobservable_command.execute = unittest.mock.AsyncMock(
            side_effect=UndefinedExecutionError("ValueError: Invalid value received")
        )

        with raises(SiLAError, match=r"ValueError: Invalid value received") as servicer_context:
            await unobservable_command.execute_rpc_handler(b"", servicer_context)
