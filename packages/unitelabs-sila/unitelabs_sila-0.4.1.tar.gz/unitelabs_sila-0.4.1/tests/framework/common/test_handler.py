import re

import pytest

from sila.framework.common.feature import Feature
from sila.framework.common.handler import Handler


class TestInitialize:
    async def test_should_raise_on_invalid_identifier(self):
        # Create handler
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            Handler(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create handler
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            Handler(identifier="Handler", display_name="")

    async def test_should_add_to_feature(self):
        # Create handler
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        handler = Handler(identifier="TestHandler", display_name="Test Handler", feature=feature)

        # Get fully qualified identifier
        assert handler.feature == feature


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create handler
        handler = Handler(identifier="TestHandler", display_name="Test Handler")

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for Handler 'TestHandler' without feature association."
            ),
        ):
            assert handler.fully_qualified_identifier is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create handler
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        handler = Handler(identifier="TestHandler", display_name="Test Handler", feature=feature)

        # Get fully qualified identifier
        assert handler.fully_qualified_identifier == feature.fully_qualified_identifier


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create handler
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        handler = Handler(identifier="TestHandler", display_name="Test Handler")

        # Add to feature
        handler.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert handler.feature == feature
