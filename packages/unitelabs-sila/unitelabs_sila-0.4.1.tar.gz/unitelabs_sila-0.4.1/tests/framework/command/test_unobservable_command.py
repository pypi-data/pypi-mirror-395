import re

import pytest

from sila.framework.command.unobservable_command import UnobservableCommand
from sila.framework.common.feature import Feature


class TestUnobservableCommand:
    async def test_should_raise_on_invalid_identifier(self):
        # Create unobservable command
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            UnobservableCommand(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create unobservable command
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            UnobservableCommand(identifier="UnobservableCommand", display_name="")

    async def test_should_set_observable_to_false(self):
        # Create unobservable command
        unobservable_command = UnobservableCommand(
            identifier="TestUnobservableCommand", display_name="TestUnobservableCommand"
        )

        # Get observable
        assert unobservable_command.observable is False

    async def test_should_add_to_feature(self):
        # Create unobservable command
        feature = Feature(identifier="SiLAService", display_name="SiLAService")
        unobservable_command = UnobservableCommand(
            identifier="TestUnobservableCommand", display_name="TestUnobservableCommand", feature=feature
        )

        # Get fully qualified identifier
        assert unobservable_command.feature == feature
        assert feature.commands["TestUnobservableCommand"] == unobservable_command


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create unobservable command
        unobservable_command = UnobservableCommand(
            identifier="TestUnobservableCommand", display_name="TestUnobservableCommand"
        )

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for "
                "UnobservableCommand 'TestUnobservableCommand' without feature association."
            ),
        ):
            assert unobservable_command.fully_qualified_identifier is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create unobservable command
        feature = Feature(identifier="SiLAService", display_name="SiLAService")
        unobservable_command = UnobservableCommand(
            identifier="TestUnobservableCommand", display_name="TestUnobservableCommand", feature=feature
        )

        # Get fully qualified identifier
        assert (
            unobservable_command.fully_qualified_identifier
            == "org.silastandard/none/SiLAService/v1/Command/TestUnobservableCommand"
        )


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create unobservable command
        feature = Feature(identifier="SiLAService", display_name="SiLAService")
        unobservable_command = UnobservableCommand(
            identifier="TestUnobservableCommand", display_name="TestUnobservableCommand"
        )

        # Add to feature
        unobservable_command.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert unobservable_command.feature == feature
        assert feature.commands["TestUnobservableCommand"] == unobservable_command
