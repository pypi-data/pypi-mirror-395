import unittest.mock

import pytest
from examples.server.metadata_provider import StringMetadata

from sila.framework.command.command_confirmation import CommandConfirmation
from sila.framework.command.command_execution_info import CommandExecutionInfo
from sila.framework.command.command_execution_uuid import CommandExecutionUUID
from sila.framework.common.feature import Feature
from sila.framework.data_types.duration import Duration
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.framework_error import InvalidCommandExecutionUUID, InvalidMetadata
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.framework.errors.validation_error import ValidationError
from sila.framework.identifiers.metadata_identifier import MetadataIdentifier
from sila.server.command_execution import CommandExecution
from sila.server.metadata import Metadata
from sila.server.observable_command import ObservableCommand
from sila.server.server import Server
from sila.testing.raises import raises


class TestInitiate:
    async def test_should_initiate_observable_command(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay",
        )
        response = await observable_command.initiate(request=Integer(42).encode(number=1) + Real(0).encode(number=2))

        # Assert that the method returns the correct value
        assert response == CommandConfirmation(unittest.mock.ANY, unittest.mock.ANY)

    async def test_should_raise_on_invalid_protobuf(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay"
        )

        with pytest.raises(
            ValidationError,
            match=(
                r"Invalid field 'Delay' in message 'EchoValueAfterDelay_Parameters': "
                r"Expected wire type 'I64', received 'LEN'\."
            ),
        ) as error:
            await observable_command.initiate(request=Integer(42).encode(number=1) + String("a").encode(number=2))

        assert (
            error.value.parameter
            == "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Delay"
        )

    async def test_should_raise_on_missing_parameter(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay"
        )

        with pytest.raises(
            ValidationError,
            match=r"Missing field 'Delay' in message 'EchoValueAfterDelay_Parameters'\.",
        ) as error:
            await observable_command.initiate(Integer(42).encode(number=1))

        assert (
            error.value.parameter
            == "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Delay"
        )

    async def test_should_intercept_metadata(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/MetadataConsumerTest/v1/Command/EchoStringMetadataObservably"
        )
        observable_command.execute = unittest.mock.AsyncMock()
        await observable_command.initiate(
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String("C").encode(
                    number=1
                )
            }
        )

        # Assert that the method returns the correct value
        observable_command.execute.assert_called_once_with(
            unittest.mock.ANY,
            {MetadataIdentifier("org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"): "C"},
            command_execution=unittest.mock.ANY,
        )

    async def test_should_ignore_additional_metadata(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay",
        )
        observable_command.execute = unittest.mock.AsyncMock()
        await observable_command.initiate(
            request=Integer(42).encode(number=1) + Real(0).encode(number=2),
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String("C").encode(
                    number=1
                )
            },
        )

        # Assert that the method returns the correct value
        observable_command.execute.assert_called_once_with(unittest.mock.ANY, {}, command_execution=unittest.mock.ANY)

    async def test_should_raise_on_invalid_metadata(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/MetadataConsumerTest/v1/Command/EchoStringMetadataObservably"
        )
        observable_command.execute = unittest.mock.AsyncMock()

        with pytest.raises(
            InvalidMetadata,
            match=r"Missing metadata 'StringMetadata' in ObservableCommand 'EchoStringMetadataObservably'\.",
        ):
            await observable_command.initiate(
                metadata={"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": b""}
            )

    async def test_should_raise_on_metadata_error(self, server: Server):
        # Initiate observable command
        feature = Feature(identifier="TestFeature", display_name="TestFeature")
        server.register_feature(feature)
        observable_command = ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            function=unittest.mock.Mock(side_effect=ValueError("Invalid value received")),
            feature=feature,
        )
        Metadata.create(
            identifier="StringMetadata",
            display_name="String Metadata",
            data_type=String,
            affects=["org.silastandard/none/TestFeature/v1"],
            function=unittest.mock.AsyncMock(
                side_effect=DefinedExecutionError.create(
                    "MetadataFailed", "Metadata Failed", "Failed to execute metadata"
                )
            ),
            feature=feature,
        )

        with pytest.raises(DefinedExecutionError, match=r"Failed to execute metadata"):
            await observable_command.initiate(
                metadata={"sila-org.silastandard-none-testfeature-v1-metadata-stringmetadata-bin": b"\x0a\x00"}
            )


class TestInitiateRpcHandler:
    async def test_should_forward_parameters(self):
        # Initiate observable command
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.initiate = unittest.mock.AsyncMock(return_value=CommandConfirmation())
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        await observable_command.initiate_rpc_handler(String("Hello, World!").encode(number=1), context)

        # Assert that the method returns the correct value
        observable_command.initiate.assert_awaited_once_with(String("Hello, World!").encode(number=1), {})

    async def test_should_forward_metadata(self):
        # Initiate observable command
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.initiate = unittest.mock.AsyncMock(return_value=CommandConfirmation())
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
        await observable_command.initiate_rpc_handler(b"", context)

        # Assert that the method returns the correct value
        observable_command.initiate.assert_awaited_once_with(
            b"",
            {"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String().encode(number=1)},
        )

    async def test_should_raise_sila_error(self):
        # Initiate observable command
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.initiate = unittest.mock.AsyncMock(
            side_effect=UndefinedExecutionError("ValueError: Invalid value received")
        )

        with raises(SiLAError, match=r"ValueError: Invalid value received") as servicer_context:
            await observable_command.initiate_rpc_handler(b"", servicer_context)


class TestSubscribeStatus:
    async def test_should_subscribe_execution_info(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay"
        )
        confirmation = await observable_command.initiate(Integer(42).encode(number=1) + Real(0).encode(number=2))

        # Subscribe execution info
        subscription = observable_command.subscribe_status(confirmation.command_execution_uuid.value)
        execution_infos = [execution_info async for execution_info in subscription]

        # Assert that the method returns the correct value
        assert execution_infos == [
            CommandExecutionInfo(
                status=CommandExecutionInfo.Status.WAITING,
                progress=Real(0.0),
            ),
            CommandExecutionInfo(
                status=CommandExecutionInfo.Status.RUNNING,
                progress=Real(1.0),
                remaining_time=Duration(),
            ),
            CommandExecutionInfo(
                status=CommandExecutionInfo.Status.FINISHED_SUCCESSFULLY,
                progress=Real(1.0),
                remaining_time=Duration(seconds=0, nanos=0),
            ),
        ]

    async def test_should_raise_on_unknown_command_execution_uuid(self, server: Server):
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay"
        )

        # Subscribe execution info
        subscription = observable_command.subscribe_status("unknown")

        # Assert that the method returns the correct value
        with pytest.raises(InvalidCommandExecutionUUID, match=r"Requested unknown command execution uuid 'unknown'\."):
            await subscription.__anext__()


class TestSubscribeStatusRpcHandler:
    async def test_should_forward_command_execution_uuid(self):
        async def iterator():
            yield CommandExecutionInfo()

        # Subscribe execution info
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.subscribe_status = unittest.mock.Mock(return_value=iterator())
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        await observable_command.subscribe_status_rpc_handler(CommandExecutionUUID().encode(), context).__anext__()

        # Assert that the method returns the correct value
        observable_command.subscribe_status.assert_called_once_with("")

    async def test_should_ignore_metadata(self):
        async def iterator():
            yield CommandExecutionInfo()

        # Subscribe execution info
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.subscribe_status = unittest.mock.Mock(return_value=iterator())
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
        await observable_command.subscribe_status_rpc_handler(CommandExecutionUUID().encode(), context).__anext__()

        # Assert that the method returns the correct value
        observable_command.subscribe_status.assert_called_once_with("")

    async def test_should_raise_sila_error(self):
        async def iterator():
            msg = "ValueError: Invalid value received"
            raise UndefinedExecutionError(msg)
            yield CommandExecutionInfo()

        # Subscribe execution info
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.subscribe_status = unittest.mock.Mock(return_value=iterator())

        with raises(SiLAError, match=r"ValueError: Invalid value received") as servicer_context:
            await observable_command.subscribe_status_rpc_handler(
                CommandExecutionUUID().encode(), servicer_context
            ).__anext__()


class TestSubscribeIntermediate:
    async def test_should_subscribe_intermediate_response(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/Count"
        )
        confirmation = await observable_command.initiate(Integer(2).encode(number=1) + Real(0.1).encode(number=2))

        # Subscribe intermediate response
        subscription = observable_command.subscribe_intermediate(confirmation.command_execution_uuid.value)
        intermediate_responses = [intermediate_response async for intermediate_response in subscription]

        # Assert that the method returns the correct value
        assert intermediate_responses == [
            Integer(0).encode(number=1),
            Integer(1).encode(number=1),
        ]

    async def test_should_raise_on_unknown_command_execution_uuid(self, server: Server):
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/Count"
        )

        # Subscribe intermediate response
        subscription = observable_command.subscribe_intermediate("unknown")

        # Assert that the method returns the correct value
        with pytest.raises(InvalidCommandExecutionUUID, match=r"Requested unknown command execution uuid 'unknown'\."):
            await subscription.__anext__()


class TestSubscribeIntermediateRpcHandler:
    async def test_should_forward_command_execution_uuid(self):
        async def iterator():
            yield CommandExecutionInfo()

        # Subscribe intermediate response
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.subscribe_intermediate = unittest.mock.Mock(return_value=iterator())
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        await observable_command.subscribe_intermediate_rpc_handler(
            CommandExecutionUUID().encode(), context
        ).__anext__()

        # Assert that the method returns the correct value
        observable_command.subscribe_intermediate.assert_called_once_with("")

    async def test_should_ignore_metadata(self):
        async def iterator():
            yield CommandExecutionInfo()

        # Subscribe intermediate response
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.subscribe_intermediate = unittest.mock.Mock(return_value=iterator())
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
        await observable_command.subscribe_intermediate_rpc_handler(
            CommandExecutionUUID().encode(), context
        ).__anext__()

        # Assert that the method returns the correct value
        observable_command.subscribe_intermediate.assert_called_once_with("")

    async def test_should_raise_sila_error(self):
        async def iterator():
            msg = "ValueError: Invalid value received"
            raise UndefinedExecutionError(msg)
            yield CommandExecutionInfo()

        # Subscribe intermediate response
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.subscribe_intermediate = unittest.mock.Mock(return_value=iterator())

        with raises(SiLAError, match=r"ValueError: Invalid value received") as servicer_context:
            await observable_command.subscribe_intermediate_rpc_handler(
                CommandExecutionUUID().encode(), servicer_context
            ).__anext__()


class TestGetResult:
    async def test_should_get_observable_command_response(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay"
        )
        confirmation = await observable_command.initiate(Integer(42).encode(number=1) + Real(0).encode(number=2))
        [_ async for _ in observable_command.subscribe_status(confirmation.command_execution_uuid.value)]

        # Get observable command response
        response = await observable_command.get_result(confirmation.command_execution_uuid.value)

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_raise_on_unknown_command_execution_uuid(self, server: Server):
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay"
        )

        # Assert that the method returns the correct value
        with pytest.raises(InvalidCommandExecutionUUID, match=r"Requested unknown command execution uuid 'unknown'\."):
            await observable_command.get_result("unknown")

    async def test_should_raise_defined_execution_error(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseDefinedExecutionErrorObservably"
        )
        confirmation = await observable_command.initiate()
        [_ async for _ in observable_command.subscribe_status(confirmation.command_execution_uuid.value)]

        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await observable_command.get_result(confirmation.command_execution_uuid.value)

    async def test_should_attach_defined_execution_error_to_feature(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseDefinedExecutionErrorObservably"
        )

        def function(**kwargs):
            msg = "SiLA2_test_error_message"
            raise DefinedExecutionError.create(identifier="TestError", display_name="TestError")(msg)

        observable_command.function = function

        confirmation = await observable_command.initiate()
        [_ async for _ in observable_command.subscribe_status(confirmation.command_execution_uuid.value)]

        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await observable_command.get_result(confirmation.command_execution_uuid.value)

    async def test_should_raise_undefined_execution_error(self, server: Server):
        # Initiate observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ErrorHandlingTest/v1/Command/RaiseUndefinedExecutionErrorObservably"
        )
        confirmation = await observable_command.initiate()
        [_ async for _ in observable_command.subscribe_status(confirmation.command_execution_uuid.value)]

        with pytest.raises(UndefinedExecutionError, match=r"SiLA2_test_error_message"):
            await observable_command.get_result(confirmation.command_execution_uuid.value)


class TestGetResultRpcHandler:
    async def test_should_return_observable_command(self):
        # Get observable command result
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.get_result = unittest.mock.AsyncMock(return_value=Integer(42).encode(number=1))
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        response = await observable_command.get_result_rpc_handler(CommandExecutionUUID().encode(), context)

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_forward_command_execution_uuid(self):
        # Subscribe execution info
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.get_result = unittest.mock.AsyncMock(return_value=Integer(42).encode(number=1))
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        await observable_command.get_result_rpc_handler(CommandExecutionUUID().encode(), context)

        # Assert that the method returns the correct value
        observable_command.get_result.assert_called_once_with("")

    async def test_should_ignore_metadata(self):
        # Subscribe execution info
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.get_result = unittest.mock.AsyncMock(return_value=Integer(42).encode(number=1))
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
        await observable_command.get_result_rpc_handler(CommandExecutionUUID().encode(), context)

        # Assert that the method returns the correct value
        observable_command.get_result.assert_called_once_with("")

    async def test_should_raise_sila_error(self):
        # Subscribe execution info
        observable_command = ObservableCommand(identifier="ObservableCommand", display_name="Observable Command")
        observable_command.get_result = unittest.mock.Mock(
            side_effect=UndefinedExecutionError("ValueError: Invalid value received")
        )

        with raises(SiLAError, match=r"ValueError: Invalid value received") as servicer_context:
            await observable_command.get_result_rpc_handler(CommandExecutionUUID().encode(), servicer_context)


class TestExecute:
    async def test_should_execute_observable_command(self, server: Server):
        # Execute observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay",
        )
        command_execution = unittest.mock.Mock(spec=CommandExecution)
        await observable_command.execute({"value": 42, "delay": 0}, {}, command_execution=command_execution)

        # Assert that the method returns the correct value
        command_execution.set_result.assert_called_once_with(Integer(42).encode(number=1))

    async def test_should_execute_observable_command_with_metadata(self, server: Server):
        # Execute observable command
        observable_command = server.get_observable_command(
            "org.silastandard/test/MetadataConsumerTest/v1/Command/EchoStringMetadataObservably"
        )
        command_execution = unittest.mock.Mock(spec=CommandExecution)
        metadata = await StringMetadata.from_buffer(
            observable_command, {StringMetadata.rpc_header(): String("C").encode(number=1)}
        )
        await observable_command.execute(
            {},
            {
                MetadataIdentifier(
                    "org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata"
                ): await metadata.to_native(server)
            },
            command_execution=command_execution,
        )

        # Assert that the method returns the correct value
        command_execution.set_result.assert_called_once_with(String("C").encode(number=1))

    async def test_should_catch_exceptions(self, server: Server):
        # Initiate observable command
        feature = Feature(identifier="TestFeature", display_name="TestFeature")
        server.register_feature(feature)
        observable_command = ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            function=unittest.mock.Mock(side_effect=ValueError("Invalid value received")),
            feature=feature,
        )
        command_execution = unittest.mock.Mock(spec=CommandExecution)
        await observable_command.execute({}, {}, command_execution=command_execution)

        # Assert that the method returns the correct value
        command_execution.set_exception.assert_called_once_with(UndefinedExecutionError("Invalid value received"))
