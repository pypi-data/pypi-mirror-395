import re
import unittest.mock

import pytest

from sila.framework.binary_transfer.binary_transfer_handler import BinaryTransferHandler
from sila.framework.command.command_execution import CommandExecution
from sila.framework.common.context import Context
from sila.framework.common.context_proxy import ContextProxy
from sila.framework.common.feature import Feature
from sila.framework.data_types.element import Element
from sila.framework.data_types.string import String


@pytest.fixture
def context():
    class ExampleContext(Context):
        def __init__(self) -> None:
            super().__init__()
            self._binary_transfer_handler = unittest.mock.Mock(spec=BinaryTransferHandler)

    return ExampleContext()


class TestProtobuf:
    def test_should_cache_protobuf(self):
        # Create context
        context_proxy = ContextProxy()

        # Register message
        Message = context_proxy.protobuf.register_message(
            name="MessageName",
            package="sila2.org.silastandard",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
        )

        # Assert that the method returns the correct value
        assert context_proxy.protobuf.messages == {"sila2.org.silastandard.MessageName": Message}

    def test_should_forward_protobuf(self, context: Context):
        # Create context
        context_proxy = ContextProxy()
        context_proxy.context = context

        # Register message
        Message = context_proxy.protobuf.register_message(
            name="MessageName",
            package="sila2.org.silastandard",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
        )

        # Assert that the method returns the correct value
        assert context.protobuf.messages == {"sila2.org.silastandard.MessageName": Message}
        assert context_proxy.protobuf.messages == {"sila2.org.silastandard.MessageName": Message}

    def test_should_merge_protobuf(self, context: Context):
        # Create context
        context_proxy = ContextProxy()

        # Register message
        Message = context_proxy.protobuf.register_message(
            name="MessageName",
            package="sila2.org.silastandard",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
        )
        context_proxy.context = context

        # Assert that the method returns the correct value
        assert context.protobuf.messages == {"sila2.org.silastandard.MessageName": Message}
        assert context_proxy.protobuf.messages == {"sila2.org.silastandard.MessageName": Message}


class TestFeatures:
    def test_should_cache_features(self):
        # Create context
        context_proxy = ContextProxy()

        # Register feature
        feature = Feature(identifier="SiLAService", display_name="SiLAService")
        context_proxy.register_feature(feature)

        # Assert that the method returns the correct value
        assert context_proxy.features == {feature.fully_qualified_identifier: feature}

    def test_should_forward_features(self, context: Context):
        # Create context
        context_proxy = ContextProxy()
        context_proxy.context = context

        # Register feature
        feature = Feature(identifier="SiLAService", display_name="SiLAService")
        context_proxy.register_feature(feature)

        # Assert that the method returns the correct value
        assert context.features == {feature.fully_qualified_identifier: feature}
        assert context_proxy.features == {feature.fully_qualified_identifier: feature}

    def test_should_merge_features(self, context: Context):
        # Create context
        feature_0 = Feature(identifier="SiLAService", display_name="SiLAService")
        context.register_feature(feature_0)
        context_proxy = ContextProxy()

        # Register feature
        feature_1 = Feature(identifier="SiLAService", display_name="SiLAService", version="2.0")
        context_proxy.register_feature(feature_1)
        context_proxy.context = context

        # Assert that the method returns the correct value
        assert context.features == {
            feature_0.fully_qualified_identifier: feature_0,
            feature_1.fully_qualified_identifier: feature_1,
        }
        assert context_proxy.features == {
            feature_0.fully_qualified_identifier: feature_0,
            feature_1.fully_qualified_identifier: feature_1,
        }

    def test_should_override_existing_features(self, context: Context):
        # Create context
        feature_0 = Feature(identifier="SiLAService", display_name="SiLAService")
        context.register_feature(feature_0)
        context_proxy = ContextProxy()

        # Register feature
        feature_1 = Feature(identifier="SiLAService", display_name="SiLAService")
        context_proxy.register_feature(feature_1)
        context_proxy.context = context

        # Assert that the method returns the correct value
        assert context.features == {
            feature_1.fully_qualified_identifier: feature_1,
        }
        assert context_proxy.features == {
            feature_1.fully_qualified_identifier: feature_1,
        }


class TestCommandExecution:
    def test_should_cache_command_executions(self):
        # Create context
        context_proxy = ContextProxy()

        # Add command execution
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )
        context_proxy.add_command_execution(execution)

        # Assert that the method returns the correct value
        assert context_proxy.command_executions == {execution.command_execution_uuid: execution}
        assert context_proxy.get_command_execution(execution.command_execution_uuid) == execution

    def test_should_forward_command_executions(self, context: Context):
        # Create context
        context_proxy = ContextProxy()
        context_proxy.context = context

        # Add command execution
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )
        context_proxy.add_command_execution(execution)

        # Assert that the method returns the correct value
        assert context.command_executions == {execution.command_execution_uuid: execution}
        assert context.get_command_execution(execution.command_execution_uuid) == execution
        assert context_proxy.command_executions == {execution.command_execution_uuid: execution}
        assert context_proxy.get_command_execution(execution.command_execution_uuid) == execution

    async def test_should_raise_on_unknown_command_execution_uuid(self):
        # Create context
        context_proxy = ContextProxy()

        # Get command execution
        with pytest.raises(ValueError, match=re.escape("Could not find any execution with the given uuid 'abc'")):
            context_proxy.get_command_execution("abc")


class TestBinaryTransferHandler:
    def test_should_raise_on_missing_context(self):
        # Create context
        context_proxy = ContextProxy()

        # Access binary transfer handler
        with pytest.raises(
            RuntimeError, match=re.escape("Unable to access 'BinaryTransferHandler' on unbound 'Feature'")
        ):
            assert context_proxy.binary_transfer_handler is None

    def test_should_access_binary_transfer_handler(self, context: Context):
        # Create context
        context_proxy = ContextProxy()
        context_proxy.context = context

        # Access binary transfer handler
        binary_transfer_handler = context_proxy.binary_transfer_handler

        # Assert that the method returns the correct value
        assert isinstance(binary_transfer_handler, BinaryTransferHandler)
