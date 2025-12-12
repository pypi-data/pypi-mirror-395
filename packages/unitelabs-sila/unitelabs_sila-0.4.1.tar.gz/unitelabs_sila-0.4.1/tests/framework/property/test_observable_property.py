import re

import pytest

from sila.framework.common.feature import Feature
from sila.framework.property.observable_property import ObservableProperty


class TestInitialize:
    async def test_should_raise_on_invalid_identifier(self):
        # Create observable property
        with pytest.raises(
            ValueError, match=re.escape("Identifier must start with an upper-case letter, received ''.")
        ):
            ObservableProperty(identifier="")

    async def test_should_raise_on_invalid_display_name(self):
        # Create observable property
        with pytest.raises(ValueError, match=re.escape("Display name must not be empty, received ''.")):
            ObservableProperty(identifier="ObservableProperty", display_name="")

    async def test_should_set_observable_to_true(self):
        # Create observable property
        observable_property = ObservableProperty(
            identifier="TestObservableProperty", display_name="Test Observable Property"
        )

        # Get observable
        assert observable_property.observable is True

    async def test_should_add_to_feature(self):
        # Create observable property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        observable_property = ObservableProperty(
            identifier="TestObservableProperty", display_name="Test Observable Property", feature=feature
        )

        # Get fully qualified identifier
        assert observable_property.feature == feature
        assert feature.properties["TestObservableProperty"] == observable_property


class TestFullyQualifiedIdentifier:
    async def test_should_raise_on_missing_feature(self):
        # Create observable property
        observable_property = ObservableProperty(
            identifier="TestObservableProperty", display_name="Test Observable Property"
        )

        # Get fully qualified identifier
        with pytest.raises(
            RuntimeError,
            match=(
                r"Unable to get fully qualified identifier for "
                r"ObservableProperty 'TestObservableProperty' without feature association."
            ),
        ):
            assert observable_property.fully_qualified_identifier is None

    async def test_should_get_fully_qualified_identifier(self):
        # Create observable property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        observable_property = ObservableProperty(
            identifier="TestObservableProperty", display_name="Test Observable Property", feature=feature
        )

        # Get fully qualified identifier
        assert (
            observable_property.fully_qualified_identifier
            == "org.silastandard/none/SiLAService/v1/Property/TestObservableProperty"
        )


class TestAddToFeature:
    async def test_should_add_to_feature(self):
        # Create observable property
        feature = Feature(identifier="SiLAService", display_name="SiLA Service")
        observable_property = ObservableProperty(
            identifier="TestObservableProperty", display_name="Test Observable Property"
        )

        # Add to feature
        observable_property.add_to_feature(feature)

        # Assert that the method returns the correct value
        assert observable_property.feature == feature
        assert feature.properties["TestObservableProperty"] == observable_property
