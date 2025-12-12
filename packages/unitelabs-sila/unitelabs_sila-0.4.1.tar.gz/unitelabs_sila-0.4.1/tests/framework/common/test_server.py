import asyncio
import re
import unittest.mock

import pytest

from sila.framework.common.feature import Feature
from sila.framework.common.server import Server
from sila.framework.data_types.custom import Custom
from sila.framework.errors.framework_error import InvalidCommandExecutionUUID
from sila.server.command_execution import CommandExecution
from sila.server.metadata import Metadata
from sila.server.observable_command import ObservableCommand
from sila.server.observable_property import ObservableProperty
from sila.server.unobservable_command import UnobservableCommand
from sila.server.unobservable_property import UnobservableProperty


class TestStart:
    async def test_should_default_to_not_ready(self):
        # Create server
        server = Server()

        # Assert that the method returns the correct value
        assert not server._ready.is_set()

    async def test_should_set_ready(self):
        # Create server
        server = Server()

        # Start server
        await server.start()

        # Assert that the method returns the correct value
        assert server._ready.is_set()

    async def test_should_raise_when_running(self):
        # Create server
        server = Server()
        await server.start()

        # Start server
        with pytest.raises(RuntimeError, match=re.escape("The Server is already running.")):
            await server.start()


class TestStop:
    async def test_should_default_to_not_shutdown(self):
        # Create server
        server = Server()

        # Assert that the method returns the correct value
        assert not server._shutdown.set()

    async def test_should_set_shutdown(self):
        # Create server
        server = Server()

        # Stop server
        await server.stop()

        # Assert that the method returns the correct value
        assert server._shutdown.is_set()

    async def test_should_shutdown_idempotently(self):
        # Create server
        server = Server()
        await server.stop()

        # Stop server
        await server.stop()

        # Assert that the method returns the correct value
        assert server._shutdown.is_set()


class TestWaitForReady:
    async def test_should_wait_for_ready(self):
        # Create server
        server = Server()

        # Wait for ready
        task = asyncio.create_task(server.wait_for_ready())
        await server.start()
        await asyncio.sleep(0)

        # Assert that the method returns the correct value
        assert task.done()


class TestWaitForTermination:
    async def test_should_wait_for_termination(self):
        # Create server
        server = Server()

        # Wait for ready
        task = asyncio.create_task(server.wait_for_termination())
        await server.stop()
        await asyncio.sleep(0)

        # Assert that the method returns the correct value
        assert task.done()


class TestGetCommandExecution:
    def test_should_get_command_execution(self):
        # Create server
        server = Server()
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )
        server.add_command_execution(execution)

        # Get command execution
        response = server.get_command_execution(execution.command_execution_uuid)

        # Assert that the method returns the correct value
        assert response == execution

    def test_should_raise_on_duplicate_uuid(self):
        # Create server
        server = Server()
        execution = unittest.mock.Mock(
            spec=CommandExecution, command_execution_uuid=unittest.mock.sentinel.command_execution_uuid
        )

        # Add command execution
        with pytest.raises(
            InvalidCommandExecutionUUID,
            match=re.escape(f"Requested unknown command execution uuid '{execution.command_execution_uuid}'."),
        ):
            server.get_command_execution(execution.command_execution_uuid)


class TestRegisterFeature:
    async def test_should_register_feature(self):
        # Create server
        server = Server()
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")

        # Register feature
        server.register_feature(feature)

        # Assert that the method returns the correct value
        assert server.features == {feature.fully_qualified_identifier: feature}

    async def test_should_raise_when_running(self):
        # Create server
        server = Server()
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        await server.start()

        # Register feature
        with pytest.raises(RuntimeError, match=re.escape("Unable to register feature. The Server is already running.")):
            server.register_feature(feature)


class TestGetFeature:
    async def test_should_get_feature(self):
        server = Server()
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        server.register_feature(feature)

        # Get feature
        response = server.get_feature(feature.fully_qualified_identifier)

        # Assert that the method returns the correct value
        assert response == feature

    async def test_should_raise_on_invalid_feature(self):
        server = Server()

        # Get feature
        with pytest.raises(ValueError, match=re.escape("Expected fully qualified feature identifier, received ''.")):
            server.get_feature("")

    async def test_should_raise_on_unknown_feature(self):
        server = Server()

        # Get feature
        with pytest.raises(
            ValueError, match=re.escape("Requested unknown feature identifier 'org.silastandard/none/SiLAService/v1'.")
        ):
            server.get_feature("org.silastandard/none/SiLAService/v1")


class TestGetUnobservableProperty:
    async def test_should_get_unobservable_property(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        unobservable_property = UnobservableProperty(identifier="Property", display_name="Property", feature=feature)
        server.register_feature(feature)

        # Get unobservable property
        response = server.get_unobservable_property(unobservable_property.fully_qualified_identifier)

        # Assert that the method returns the correct value
        assert response == unobservable_property

    async def test_should_raise_on_unknown_unobservable_property(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        server.register_feature(feature)

        # Get unobservable property
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Requested unknown property identifier 'org.silastandard/none/Feature/v1/Property/Property'."
            ),
        ):
            server.get_unobservable_property("org.silastandard/none/Feature/v1/Property/Property")

    async def test_should_raise_on_observable_property(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        observable_property = ObservableProperty(identifier="Property", display_name="Property", feature=feature)
        server.register_feature(feature)

        # Get unobservable property
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected identifier to reference an unobservable property, received 'observable property' instead."
            ),
        ):
            server.get_unobservable_property(observable_property.fully_qualified_identifier)


class TestGetObservableProperty:
    async def test_should_get_observable_property(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        observable_property = ObservableProperty(identifier="Property", display_name="Property", feature=feature)
        server.register_feature(feature)

        # Get observable property
        response = server.get_observable_property(observable_property.fully_qualified_identifier)

        # Assert that the method returns the correct value
        assert response == observable_property

    async def test_should_raise_on_unknown_observable_property(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        server.register_feature(feature)

        # Get observable property
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Requested unknown property identifier 'org.silastandard/none/Feature/v1/Property/Property'."
            ),
        ):
            server.get_observable_property("org.silastandard/none/Feature/v1/Property/Property")

    async def test_should_raise_on_observable_property(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        unobservable_property = UnobservableProperty(identifier="Property", display_name="Property", feature=feature)
        server.register_feature(feature)

        # Get observable property
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected identifier to reference an observable property, received 'unobservable property' instead."
            ),
        ):
            server.get_observable_property(unobservable_property.fully_qualified_identifier)


class TestGetUnobservableCommand:
    async def test_should_get_unobservable_command(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        unobservable_command = UnobservableCommand(identifier="Command", display_name="Command", feature=feature)
        server.register_feature(feature)

        # Get unobservable comannd
        response = server.get_unobservable_command(unobservable_command.fully_qualified_identifier)

        # Assert that the method returns the correct value
        assert response == unobservable_command

    async def test_should_raise_on_unknown_unobservable_command(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        server.register_feature(feature)

        # Get unobservable comannd
        with pytest.raises(
            ValueError,
            match=re.escape("Requested unknown command identifier 'org.silastandard/none/Feature/v1/Command/Command'."),
        ):
            server.get_unobservable_command("org.silastandard/none/Feature/v1/Command/Command")

    async def test_should_raise_on_observable_command(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        observable_command = ObservableCommand(identifier="Command", display_name="Command", feature=feature)
        server.register_feature(feature)

        # Get unobservable comannd
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected identifier to reference an unobservable command, received 'observable command' instead."
            ),
        ):
            server.get_unobservable_command(observable_command.fully_qualified_identifier)


class TestGetObservableCommand:
    async def test_should_get_observable_command(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        observable_command = ObservableCommand(identifier="Command", display_name="Command", feature=feature)
        server.register_feature(feature)

        # Get observable comannd
        response = server.get_observable_command(observable_command.fully_qualified_identifier)

        # Assert that the method returns the correct value
        assert response == observable_command

    async def test_should_raise_on_unknown_observable_command(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        server.register_feature(feature)

        # Get observable comannd
        with pytest.raises(
            ValueError,
            match=re.escape("Requested unknown command identifier 'org.silastandard/none/Feature/v1/Command/Command'."),
        ):
            server.get_observable_command("org.silastandard/none/Feature/v1/Command/Command")

    async def test_should_raise_on_unobservable_command(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        unobservable_command = UnobservableCommand(identifier="Command", display_name="Command", feature=feature)
        server.register_feature(feature)

        # Get observable comannd
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected identifier to reference an observable command, received 'unobservable command' instead."
            ),
        ):
            server.get_observable_command(unobservable_command.fully_qualified_identifier)


class TestGetDataTypeDefinition:
    async def test_should_get_data_type_definition(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        custom = Custom.create(identifier="CustomDataType", display_name="Custom Data Type", feature=feature)
        server.register_feature(feature)

        # Get metadata
        response = server.get_data_type_definition(custom.fully_qualified_identifier())

        # Assert that the method returns the correct value
        assert response == custom

    async def test_should_raise_on_unknown_data_type_definition(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        server.register_feature(feature)

        # Get metadata
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Requested unknown custom data type identifier "
                "'org.silastandard/none/Feature/v1/DataType/CustomDataType'."
            ),
        ):
            server.get_data_type_definition("org.silastandard/none/Feature/v1/DataType/CustomDataType")


class TestGetMetadata:
    async def test_should_get_metadata(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        metadata = Metadata.create(identifier="Command", display_name="Command", feature=feature)
        server.register_feature(feature)

        # Get metadata
        response = server.get_metadata(metadata.fully_qualified_identifier())

        # Assert that the method returns the correct value
        assert response == metadata

    async def test_should_raise_on_unknown_metadata(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        server.register_feature(feature)

        # Get metadata
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Requested unknown metadata identifier 'org.silastandard/none/Feature/v1/Metadata/Meatadata'."
            ),
        ):
            server.get_metadata("org.silastandard/none/Feature/v1/Metadata/Meatadata")


class TestGetMetadataByAffect:
    async def test_should_get_metadata(self):
        server = Server()
        feature = Feature(identifier="Feature", display_name="Feature")
        metadata = Metadata.create(
            identifier="Metadata",
            display_name="Metadata",
            affects=[feature.fully_qualified_identifier],
            feature=feature,
        )
        server.register_feature(feature)

        # Get metadata
        response = server.get_metadata_by_affect(feature.fully_qualified_identifier)

        # Assert that the method returns the correct value
        assert response == [metadata]
