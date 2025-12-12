import re

import pytest

from sila.framework.command.observable_command import ObservableCommand
from sila.framework.common.feature import Feature


class TestObservableCommand:
    async def test_should_raise_on_invalid_identifier(self):
        # Create observable command
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            ObservableCommand(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create observable command
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            ObservableCommand(identifier="ObservableCommand", display_name="")

    async def test_should_set_observable_to_false(self):
        # Create observable command
        observable_command = ObservableCommand(
            identifier="TestObservableCommand", display_name="Test Observable Command"
        )

        # Get observable
        assert observable_command.observable is True

    async def test_should_add_to_feature(self):
        # Create observable command
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        observable_command = ObservableCommand(
            identifier="TestObservableCommand", display_name="Test Observable Command", feature=feature
        )

        # Get fully qualified identifier
        assert observable_command.feature == feature
        assert feature.commands["TestObservableCommand"] == observable_command


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create observable command
        observable_command = ObservableCommand(
            identifier="TestObservableCommand", display_name="Test Observable Command"
        )

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for "
                "ObservableCommand 'TestObservableCommand' without feature association."
            ),
        ):
            assert observable_command.fully_qualified_identifier is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create observable command
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        observable_command = ObservableCommand(
            identifier="TestObservableCommand", display_name="Test Observable Command", feature=feature
        )

        # Get fully qualified identifier
        assert (
            observable_command.fully_qualified_identifier
            == "org.silastandard/none/SiLAService/v1/Command/TestObservableCommand"
        )


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create observable command
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        observable_command = ObservableCommand(
            identifier="TestObservableCommand", display_name="Test Observable Command"
        )

        # Add to feature
        observable_command.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert observable_command.feature == feature
        assert feature.commands["TestObservableCommand"] == observable_command
