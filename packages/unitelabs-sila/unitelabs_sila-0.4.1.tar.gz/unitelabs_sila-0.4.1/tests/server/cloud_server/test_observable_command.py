import asyncio
import unittest.mock

from examples.server.error_handling_test import TestError as DefinedExecutionError

from sila.framework.cloud.cancel_request import CancelRequest
from sila.framework.cloud.client_message import ClientMessage
from sila.framework.cloud.command_confirmation_response import CommandConfirmationResponse
from sila.framework.cloud.command_execution_request import CommandExecutionRequest
from sila.framework.cloud.command_execution_response import CommandExecutionResponse
from sila.framework.cloud.command_parameter import CommandParameter
from sila.framework.cloud.command_response_request import CommandResponseRequest
from sila.framework.cloud.observable_command_response import ObservableCommandResponse
from sila.framework.cloud.server_message import ServerMessage
from sila.framework.command.command_confirmation import CommandConfirmation
from sila.framework.command.command_execution_info import CommandExecutionInfo
from sila.framework.command.command_execution_uuid import CommandExecutionUUID
from sila.framework.data_types.duration import Duration
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.errors.framework_error import CommandExecutionNotFinished, InvalidCommandExecutionUUID
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.framework.errors.validation_error import ValidationError
from sila.server.cloud_server import CloudServer


async def echo_value_after_delay(cloud_server: CloudServer, delay: float) -> CommandExecutionUUID:
    request = ClientMessage(
        request_uuid=unittest.mock.sentinel.request_uuid,
        observable_command_initiation=CommandExecutionRequest(
            fully_qualified_command_id="org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay",
            command_parameter=CommandParameter(parameters=Integer(42).encode(number=1) + Real(delay).encode(number=2)),
        ),
    )
    await cloud_server.receive(request)
    response = await cloud_server._responses.__anext__()
    assert response.observable_command_confirmation

    return response.observable_command_confirmation.command_confirmation.command_execution_uuid


async def count(cloud_server: CloudServer, n: int, delay: float = 0.1) -> CommandExecutionUUID:
    request = ClientMessage(
        request_uuid=unittest.mock.sentinel.request_uuid,
        observable_command_initiation=CommandExecutionRequest(
            fully_qualified_command_id="org.silastandard/test/ObservableCommandTest/v1/Command/Count",
            command_parameter=CommandParameter(parameters=Integer(n).encode(number=1) + Real(delay).encode(number=2)),
        ),
    )
    await cloud_server.receive(request)
    response = await cloud_server._responses.__anext__()
    assert response.observable_command_confirmation

    return response.observable_command_confirmation.command_confirmation.command_execution_uuid


class TestObservableCommandInitiation:
    async def test_should_initiate_observable_command(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay",
                command_parameter=CommandParameter(parameters=Integer(42).encode(number=1) + Real(0).encode(number=2)),
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response.observable_command_confirmation

        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_confirmation=CommandConfirmationResponse(
                command_confirmation=CommandConfirmation(unittest.mock.ANY, unittest.mock.ANY),
            ),
        )

        cloud_server.get_command_execution(
            response.observable_command_confirmation.command_confirmation.command_execution_uuid.value
        ).cancel()

    async def test_should_raise_on_invalid_protobuf(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay",
                command_parameter=CommandParameter(
                    parameters=Integer(42).encode(number=1) + String("a").encode(number=2),
                ),
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=ValidationError(
                "Invalid field 'Delay' in message 'EchoValueAfterDelay_Parameters': "
                "Expected wire type 'I64', received 'LEN'.",
                "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Delay",
            ),
        )

    async def test_should_raise_on_missing_parameter(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay",
                command_parameter=CommandParameter(parameters=Integer(42).encode(number=1)),
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=ValidationError(
                "Missing field 'Delay' in message 'EchoValueAfterDelay_Parameters'.",
                "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Delay",
            ),
        )

    async def test_should_raise_on_malformed_identifier(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(fully_qualified_command_id=""),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError("Expected fully qualified feature identifier, received ''."),
        )

    async def test_should_raise_on_unknown_identifier(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
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
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
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

    async def test_should_raise_on_unobservable_command_identifier(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/UnobservableCommandTest/v1/Command/CommandWithoutParametersAndResponses"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError(
                "Expected identifier to reference an observable command, received 'unobservable command' instead."
            ),
        )


class TestObservableCommandExecutionInfo:
    async def test_should_subscribe_execution_info(self, cloud_server: CloudServer):
        # Initiate observable command
        command_execution_uuid = await echo_value_after_delay(cloud_server, delay=0.1)

        # Subscribe execution info
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandExecutionResponse(
                command_execution_uuid=command_execution_uuid,
                execution_info=CommandExecutionInfo(
                    status=CommandExecutionInfo.Status.WAITING,
                    progress=Real(0.0),
                ),
            ),
        )

        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandExecutionResponse(
                command_execution_uuid=command_execution_uuid,
                execution_info=CommandExecutionInfo(
                    status=CommandExecutionInfo.Status.RUNNING,
                    progress=Real(1.0),
                    remaining_time=Duration(),
                ),
            ),
        )

        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandExecutionResponse(
                command_execution_uuid=command_execution_uuid,
                execution_info=CommandExecutionInfo(
                    status=CommandExecutionInfo.Status.FINISHED_SUCCESSFULLY,
                    progress=Real(1.0),
                    remaining_time=Duration(seconds=0, nanos=0),
                ),
            ),
        )

    async def test_should_cancel_subscribe_execution_info(self, cloud_server: CloudServer):
        # Initiate observable command
        command_execution_uuid = await echo_value_after_delay(cloud_server, delay=0.1)

        # Subscribe execution info
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Cancel subscription
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            cancel_observable_command_execution_info=CancelRequest(),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        await asyncio.sleep(0.1)
        assert cloud_server._responses.size == 0

    async def test_should_raise_on_unknown_command_execution_uuid(self, cloud_server: CloudServer):
        # Subscribe execution info
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandResponseRequest(CommandExecutionUUID("unknown")),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=InvalidCommandExecutionUUID("Requested unknown command execution uuid 'unknown'."),
        )


class TestObservableCommandIntermediateResponse:
    async def test_should_subscribe_intermediate_response(self, cloud_server: CloudServer):
        # Initiate observable command
        command_execution_uuid = await count(cloud_server, n=2, delay=0.1)

        # Subscribe intermediate response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_intermediate_response=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.get(timeout=0.2)
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_intermediate_response=ObservableCommandResponse(
                command_execution_uuid=command_execution_uuid,
                response=Integer(0).encode(number=1),
            ),
        )

        response = await cloud_server._responses.get(timeout=0.2)
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_intermediate_response=ObservableCommandResponse(
                command_execution_uuid=command_execution_uuid,
                response=Integer(1).encode(number=1),
            ),
        )

        await asyncio.sleep(0.2)

    async def test_should_cancel_subscribe_intermediate_response(self, cloud_server: CloudServer):
        # Initiate observable command
        command_execution_uuid = await count(cloud_server, n=2, delay=0.1)

        # Subscribe intermediate response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_intermediate_response=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Cancel subscription
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            cancel_observable_command_intermediate_response=CancelRequest(),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        await asyncio.sleep(0.1)
        assert cloud_server._responses.size == 0

        await asyncio.sleep(0.2)

    async def test_should_raise_on_unknown_command_execution_uuid(self, cloud_server: CloudServer):
        # Subscribe intermediate response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_intermediate_response=CommandResponseRequest(CommandExecutionUUID("unknown")),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=InvalidCommandExecutionUUID("Requested unknown command execution uuid 'unknown'."),
        )


class TestObservableCommandResponse:
    async def test_should_raise_when_not_finished(self, cloud_server: CloudServer):
        # Initiate observable command
        command_execution_uuid = await echo_value_after_delay(cloud_server, delay=0)

        # Get observable command response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_response=CommandResponseRequest(command_execution_uuid),
        )

        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=CommandExecutionNotFinished("Result is not ready."),
        )

    async def test_should_get_observable_command_response(self, cloud_server: CloudServer):
        # Initiate observable command
        command_execution_uuid = await echo_value_after_delay(cloud_server, delay=0)
        await asyncio.sleep(0)

        # Get observable command response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_response=CommandResponseRequest(command_execution_uuid),
        )

        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_response=ObservableCommandResponse(
                command_execution_uuid=command_execution_uuid,
                response=Integer(42).encode(number=1),
            ),
        )

    async def test_should_cancel_subscriptions_on_finished(self, cloud_server: CloudServer):
        # Initiate observable command
        command_execution_uuid = await count(cloud_server, n=2, delay=0.1)

        # Subscribe execution info
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Subscribe intermediate response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_intermediate_response=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        await asyncio.sleep(0.3)
        assert cloud_server.tasks == {}

    async def test_should_raise_defined_execution_error(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseDefinedExecutionErrorObservably",
            ),
        )
        await cloud_server.receive(request)
        response = await cloud_server._responses.__anext__()
        assert response.observable_command_confirmation
        command_execution_uuid = response.observable_command_confirmation.command_confirmation.command_execution_uuid

        # Subscribe execution info
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Get observable command response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_response=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandExecutionResponse(
                command_execution_uuid=command_execution_uuid,
                execution_info=CommandExecutionInfo(
                    status=CommandExecutionInfo.Status.FINISHED_WITH_ERROR,
                    progress=Real(1.0),
                    remaining_time=Duration(seconds=0, nanos=0),
                ),
            ),
        )

        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=DefinedExecutionError("SiLA2_test_error_message"),
        )

    async def test_should_raise_undefined_execution_error(self, cloud_server: CloudServer):
        # Initiate observable command
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_initiation=CommandExecutionRequest(
                fully_qualified_command_id="org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseUndefinedExecutionErrorObservably",
            ),
        )
        await cloud_server.receive(request)
        response = await cloud_server._responses.__anext__()
        assert response.observable_command_confirmation
        command_execution_uuid = response.observable_command_confirmation.command_confirmation.command_execution_uuid

        # Subscribe execution info
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Get observable command response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_response=CommandResponseRequest(command_execution_uuid),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_execution_info=CommandExecutionResponse(
                command_execution_uuid=command_execution_uuid,
                execution_info=CommandExecutionInfo(
                    status=CommandExecutionInfo.Status.FINISHED_WITH_ERROR,
                    progress=Real(1.0),
                    remaining_time=Duration(seconds=0, nanos=0),
                ),
            ),
        )

        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=UndefinedExecutionError("SiLA2_test_error_message"),
        )

    async def test_should_raise_on_unknown_command_execution_uuid(self, cloud_server: CloudServer):
        # Get observable command response
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            observable_command_response=CommandResponseRequest(CommandExecutionUUID("unknown")),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=InvalidCommandExecutionUUID("Requested unknown command execution uuid 'unknown'."),
        )
