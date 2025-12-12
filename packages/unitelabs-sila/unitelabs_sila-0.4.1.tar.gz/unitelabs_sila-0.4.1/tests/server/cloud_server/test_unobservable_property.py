import unittest.mock

from examples.server.error_handling_test import TestError as DefinedExecutionError

from sila.framework.cloud.client_message import ClientMessage
from sila.framework.cloud.property_request import PropertyRequest
from sila.framework.cloud.property_response import PropertyResponse
from sila.framework.cloud.server_message import ServerMessage
from sila.framework.data_types.integer import Integer
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.server.cloud_server import CloudServer


class TestUnobservablePropertyRead:
    async def test_should_read_unobservable_property(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_read=PropertyRequest(
                fully_qualified_property_id="org.silastandard/test/UnobservablePropertyTest/v1/Property/AnswerToEverything"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_value=PropertyResponse(value=Integer(42).encode(number=1)),
        )

    async def test_should_raise_defined_execution_error(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_read=PropertyRequest(
                fully_qualified_property_id="org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseDefinedExecutionErrorOnGet"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            property_error=DefinedExecutionError("SiLA2_test_error_message"),
        )

    async def test_should_raise_undefined_execution_error(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_read=PropertyRequest(
                fully_qualified_property_id="org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseUndefinedExecutionErrorOnGet"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            property_error=UndefinedExecutionError("SiLA2_test_error_message"),
        )

    async def test_should_raise_on_malformed_identifier(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_read=PropertyRequest(fully_qualified_property_id=""),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            property_error=UndefinedExecutionError("Expected fully qualified feature identifier, received ''."),
        )

    async def test_should_raise_on_unknown_identifier(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_read=PropertyRequest(
                fully_qualified_property_id="org.silastandard/test/UnobservablePropertyTest/v1/Property/UnknownProperty"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            property_error=UndefinedExecutionError(
                "Requested unknown property identifier "
                "'org.silastandard/test/UnobservablePropertyTest/v1/Property/UnknownProperty'."
            ),
        )

    async def test_should_raise_on_command_identifier(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_read=PropertyRequest(
                fully_qualified_property_id="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            property_error=UndefinedExecutionError(
                "Expected fully qualified feature identifier, received "
                "'org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString'."
            ),
        )

    async def test_should_raise_on_observable_property_identifier(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            unobservable_property_read=PropertyRequest(
                fully_qualified_property_id="org.silastandard/test/ObservablePropertyTest/v1/Property/Alternating"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            property_error=UndefinedExecutionError(
                "Expected identifier to reference an unobservable property, received 'observable property' instead."
            ),
        )
