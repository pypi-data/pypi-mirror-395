import re
import unittest.mock

import pytest

from sila.framework.binary_transfer.binary_transfer_handler import BinaryTransferHandler
from sila.framework.command.command_execution import CommandExecution
from sila.framework.command.observable_command import ObservableCommand
from sila.framework.command.unobservable_command import UnobservableCommand
from sila.framework.common.context import Context
from sila.framework.common.feature import Feature
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.framework_error import InvalidCommandExecutionUUID
from sila.framework.metadata.metadata import Metadata
from sila.framework.property.observable_property import ObservableProperty
from sila.framework.property.unobservable_property import UnobservableProperty
from sila.framework.protobuf.protobuf import Protobuf


class TestInitialize:
    def test_should_create_protobuf_property(self):
        # Create context
        context = Context()

        assert isinstance(context.protobuf, Protobuf)

    def test_should_create_features_property(self):
        # Create context
        context = Context()

        assert context.features == {}

    def test_should_create_command_executions_property(self):
        # Create context
        context = Context()

        assert context.command_executions == {}

    def test_should_create_binary_transfer_handler_property(self):
        # Create context
        binary_transfer_handler = unittest.mock.Mock(spec=BinaryTransferHandler)
        context = Context()
        context._binary_transfer_handler = binary_transfer_handler

        assert context.binary_transfer_handler == binary_transfer_handler


class TestRegisterFeature:
    async def test_should_register_feature(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")

        # Register feature
        context.register_feature(feature)

        # Assert that the method returns the correct value
        assert context.features == {feature.fully_qualified_identifier: feature}

    async def test_should_merge_protobuf(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")

        Message = Structure.create({}, name="Structure")
        feature.context.protobuf.register_message(message=Message)
        feature.context.protobuf.register_service(name="Get_Structure", service={})

        # Register feature
        context.register_feature(feature)

        # Assert that the method returns the correct value
        assert context.protobuf.messages == {"Structure": Message}
        assert context.protobuf.services == {"Get_Structure": {}}

    async def test_should_set_feature_context(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")

        # Register feature
        context.register_feature(feature)

        # Assert that the method returns the correct value
        assert feature.context == context


class TestGetFeature:
    async def test_should_get_feature(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)

        # Get feature
        response = context.get_feature(feature.fully_qualified_identifier)

        # Assert that the method returns the correct value
        assert response == feature

    async def test_should_raise_on_invalid_feature(self):
        context = Context()

        # Get feature
        with pytest.raises(ValueError, match=re.escape("Expected fully qualified feature identifier, received ''.")):
            context.get_feature("")

    async def test_should_raise_on_unknown_feature(self):
        # Create context
        context = Context()

        # Get feature
        with pytest.raises(
            ValueError, match=re.escape("Requested unknown feature identifier 'org.silastandard/none/SiLAService/v1'.")
        ):
            context.get_feature("org.silastandard/none/SiLAService/v1")


class TestAddCommandExecution:
    def test_should_add_command_execution(self):
        # Create context
        context = Context()
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )

        # Add command execution
        context.add_command_execution(execution)

        # Assert that the method returns the correct value
        assert context.command_executions == {execution.command_execution_uuid: execution}

    def test_should_raise_on_duplicate_uuid(self):
        # Create context
        context = Context()
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )

        # Add command execution
        context.add_command_execution(execution)
        with pytest.raises(
            InvalidCommandExecutionUUID,
            match=re.escape(f"Command execution with uuid '{execution.command_execution_uuid}' already exists."),
        ):
            context.add_command_execution(execution)


class TestGetCommandExecution:
    def test_should_get_command_execution(self):
        # Create context
        context = Context()
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )
        context.add_command_execution(execution)

        # Get command execution
        response = context.get_command_execution(execution.command_execution_uuid)

        # Assert that the method returns the correct value
        assert response == execution

    def test_should_raise_on_unknown_uuid(self):
        # Create context
        context = Context()
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )

        # Add command execution
        with pytest.raises(
            InvalidCommandExecutionUUID,
            match=re.escape(f"Requested unknown command execution uuid '{execution.command_execution_uuid}'."),
        ):
            context.get_command_execution(execution.command_execution_uuid)


class TestGetDefinedExecutionError:
    def test_should_get_defined_execution_error(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)
        error = DefinedExecutionError.create(
            identifier="DefinedExecutionError",
            display_name="Defined Execution Error",
            description="Defined Execution Error.",
        )
        error.add_to_feature(feature)

        # Get command execution
        response = context.get_defined_execution_error(
            "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

        # Assert that the method returns the correct value
        assert response == error
        assert (
            response().fully_qualified_identifier
            == "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

    def test_should_get_defined_execution_error_from_unobservable_property(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)
        error = DefinedExecutionError.create(
            identifier="DefinedExecutionError",
            display_name="Defined Execution Error",
            description="Defined Execution Error.",
        )
        UnobservableProperty(
            identifier="UnobservableProperty",
            display_name="Unobservable Property",
            description="Unobservable Property.",
            data_type=String,
            errors={error.identifier: error},
            feature=feature,
        )

        # Get command execution
        response = context.get_defined_execution_error(
            "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

        # Assert that the method returns the correct value
        assert response == error
        assert (
            response().fully_qualified_identifier
            == "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

    def test_should_get_defined_execution_error_from_observable_property(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)
        error = DefinedExecutionError.create(
            identifier="DefinedExecutionError",
            display_name="Defined Execution Error",
            description="Defined Execution Error.",
        )
        ObservableProperty(
            identifier="ObservableProperty",
            display_name="Observable Property",
            description="Observable Property.",
            data_type=String,
            errors={error.identifier: error},
            feature=feature,
        )

        # Get command execution
        response = context.get_defined_execution_error(
            "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

        # Assert that the method returns the correct value
        assert response == error
        assert (
            response().fully_qualified_identifier
            == "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

    def test_should_get_defined_execution_error_from_unobservable_command(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)
        error = DefinedExecutionError.create(
            identifier="DefinedExecutionError",
            display_name="Defined Execution Error",
            description="Defined Execution Error.",
        )
        UnobservableCommand(
            identifier="UnobservableCommand",
            display_name="Unobservable Command",
            description="Unobservable Command.",
            errors={error.identifier: error},
            feature=feature,
        )

        # Get command execution
        response = context.get_defined_execution_error(
            "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

        # Assert that the method returns the correct value
        assert response == error
        assert (
            response().fully_qualified_identifier
            == "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

    def test_should_get_defined_execution_error_from_observable_command(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)
        error = DefinedExecutionError.create(
            identifier="DefinedExecutionError",
            display_name="Defined Execution Error",
            description="Defined Execution Error.",
        )
        ObservableCommand(
            identifier="ObservableCommand",
            display_name="Observable Command",
            description="Observable Command.",
            errors={error.identifier: error},
            feature=feature,
        )

        # Get command execution
        response = context.get_defined_execution_error(
            "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

        # Assert that the method returns the correct value
        assert response == error
        assert (
            response().fully_qualified_identifier
            == "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

    def test_should_get_defined_execution_error_from_metadata(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)
        error = DefinedExecutionError.create(
            identifier="DefinedExecutionError",
            display_name="Defined Execution Error",
            description="Defined Execution Error.",
        )
        Metadata.create(
            identifier="Metadata",
            display_name="Metadata",
            description="Metadata.",
            data_type=String,
            errors={error.identifier: error},
            feature=feature,
        )

        # Get command execution
        response = context.get_defined_execution_error(
            "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

        # Assert that the method returns the correct value
        assert response == error
        assert (
            response().fully_qualified_identifier
            == "org.silastandard/none/Feature/v1/DefinedExecutionError/DefinedExecutionError"
        )

    def test_should_raise_on_unknown_identifier(self):
        # Create context
        context = Context()
        feature = Feature(identifier="Feature", display_name="Feature")
        context.register_feature(feature)

        # Add command execution
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Requested unknown error identifier 'org.silastandard/none/Feature/v1/DefinedExecutionError/Error'."
            ),
        ):
            context.get_defined_execution_error("org.silastandard/none/Feature/v1/DefinedExecutionError/Error")
