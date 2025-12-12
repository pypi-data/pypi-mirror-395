import re

import pytest

from sila.framework.common.feature import Feature
from sila.framework.property.unobservable_property import UnobservableProperty


class TestInitialize:
    async def test_should_raise_on_invalid_identifier(self):
        # Create unobservable property
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            UnobservableProperty(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create unobservable property
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            UnobservableProperty(identifier="UnobservableProperty", display_name="")

    async def test_should_set_observable_to_false(self):
        # Create unobservable property
        unobservable_property = UnobservableProperty(
            identifier="TestUnobservableProperty", display_name="Test Unobservable Property"
        )

        # Get observable
        assert unobservable_property.observable is False

    async def test_should_add_to_feature(self):
        # Create unobservable property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        unobservable_property = UnobservableProperty(
            identifier="TestUnobservableProperty", display_name="Test Unobservable Property", feature=feature
        )

        # Get fully qualified identifier
        assert unobservable_property.feature == feature
        assert feature.properties["TestUnobservableProperty"] == unobservable_property


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create unobservable property
        unobservable_property = UnobservableProperty(
            identifier="TestUnobservableProperty", display_name="Test Unobservable Property"
        )

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Unable to get fully qualified identifier for "
                "UnobservableProperty 'TestUnobservableProperty' without feature association."
            ),
        ):
            assert unobservable_property.fully_qualified_identifier is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create unobservable property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        unobservable_property = UnobservableProperty(
            identifier="TestUnobservableProperty", display_name="Test Unobservable Property", feature=feature
        )

        # Get fully qualified identifier
        assert (
            unobservable_property.fully_qualified_identifier
            == "org.silastandard/none/SiLAService/v1/Property/TestUnobservableProperty"
        )


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create unobservable property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        unobservable_property = UnobservableProperty(
            identifier="TestUnobservableProperty", display_name="Test Unobservable Property"
        )

        # Add to feature
        unobservable_property.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert unobservable_property.feature == feature
        assert feature.properties["TestUnobservableProperty"] == unobservable_property
