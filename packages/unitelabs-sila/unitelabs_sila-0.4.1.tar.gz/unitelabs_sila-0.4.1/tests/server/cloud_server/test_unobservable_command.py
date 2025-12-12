import unittest.mock

from examples.server.error_handling_test import TestError as DefinedExecutionError

from sila.framework.cloud.client_message import ClientMessage
from sila.framework.cloud.command_execution_request import CommandExecutionRequest
from sila.framework.cloud.command_parameter import CommandParameter
from sila.framework.cloud.server_message import ServerMessage
from sila.framework.cloud.unobservable_command_response import UnobservableCommandResponse
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.framework.errors.validation_error import ValidationError
from sila.server.cloud_server import CloudServer


class TestUnobservableCommandExecution:
    async def test_should_execute_unobservable_command(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/CommandWithoutParametersAndResponses",
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_response=UnobservableCommandResponse(),
        )

    async def test_should_execute_unobservable_command_with_parameter(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString",
                command_parameter=CommandParameter(parameters=Integer(12345).encode(number=1)),
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_response=UnobservableCommandResponse(response=String("12345").encode(number=1)),
        )

    async def test_should_execute_unobservable_command_with_parameters(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/JoinIntegerAndString",
                command_parameter=CommandParameter(
                    parameters=Integer(123).encode(number=1) + String("abc").encode(number=2)
                ),
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_response=UnobservableCommandResponse(response=String("123abc").encode(number=1)),
        )

    async def test_should_execute_unobservable_command_with_responses(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/SplitStringAfterFirstCharacter",
                command_parameter=CommandParameter(parameters=String("abcde").encode(number=1)),
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_response=UnobservableCommandResponse(
                response=String("a").encode(number=1) + String("bcde").encode(number=2)
            ),
        )

    async def test_should_raise_on_invalid_protobuf(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString",
                command_parameter=CommandParameter(parameters=String("abc").encode(number=1)),
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=ValidationError(
                "Invalid field 'Integer' in message 'ConvertIntegerToString_Parameters': "
                "Expected wire type 'VARINT', received 'LEN'.",
                "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer",
            ),
        )

    async def test_should_raise_on_missing_parameter(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString",
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=ValidationError(
                "Missing field 'Integer' in message 'ConvertIntegerToString_Parameters'.",
                "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer",
            ),
        )

    async def test_should_raise_defined_execution_error(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseDefinedExecutionError"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=DefinedExecutionError("SiLA2_test_error_message"),
        )

    async def test_should_raise_undefined_execution_error(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseUndefinedExecutionError"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError("SiLA2_test_error_message"),
        )

    async def test_should_raise_on_malformed_identifier(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(fully_qualified_command_id=""),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError("Expected fully qualified feature identifier, received ''."),
        )

    async def test_should_raise_on_unknown_identifier(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/UnknownCommand"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError(
                "Requested unknown command identifier "
                "'org.silastandard/test/UnobservableCommandTest/v1/Command/UnknownCommand'."
            ),
        )

    async def test_should_raise_on_property_identifier(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservablePropertyTest/v1/Property/AnswerToEverything"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError(
                "Expected fully qualified feature identifier, received "
                "'org.silastandard/test/UnobservablePropertyTest/v1/Property/AnswerToEverything'."
            ),
        )

    async def test_should_raise_on_observable_command_identifier(self, cloud_server: CloudServer):
        # Execute unobservable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_command_execution=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError(
                "Expected identifier to reference an unobservable command, received 'observable command' instead."
            ),
        )
