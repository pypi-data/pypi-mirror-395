import pytest

from sila.framework.common.feature import Feature
from sila.framework.data_types.element import Element
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.errors.framework_error import InvalidMetadata
from sila.server.metadata import Metadata
from sila.server.unobservable_property import UnobservableProperty


class TestFromBuffer:
    async def test_should_initialize_from_buffer(self):
        # Create metadata
        metadata_feature = Feature(identifier="MetadataFeature", display_name="Metadata Feature")
        test_feature = Feature(identifier="TestFeature", display_name="Test Feature")
        test_handler = UnobservableProperty(
            identifier="TestProperty", display_name="Test Property", feature=test_feature
        )
        TestMetadata = Metadata.create(
            identifier="TestMetadata", display_name="Test Metadata", data_type=String, feature=metadata_feature
        )

        metadata = await TestMetadata.from_buffer(
            test_handler,
            {
                "sila-org.silastandard-none-metadatafeature-v1-metadata-testmetadata-bin": String(
                    "Hello, World!"
                ).encode(None, 1)
            },
        )

        assert metadata.value == String("Hello, World!")

    async def test_should_raise_on_missing_metadata(self):
        # Create metadata
        metadata_feature = Feature(identifier="MetadataFeature", display_name="Metadata Feature")
        test_feature = Feature(identifier="TestFeature", display_name="Test Feature")
        test_handler = UnobservableProperty(
            identifier="TestProperty", display_name="Test Property", feature=test_feature
        )
        TestMetadata = Metadata.create(
            identifier="TestMetadata", display_name="Test Metadata", data_type=String, feature=metadata_feature
        )

        with pytest.raises(
            InvalidMetadata, match="Missing metadata 'TestMetadata' in UnobservableProperty 'TestProperty'."
        ):
            await TestMetadata.from_buffer(test_handler, {})

    async def test_should_raise_on_malformed_metadata(self):
        # Create metadata
        metadata_feature = Feature(identifier="MetadataFeature", display_name="Metadata Feature")
        test_feature = Feature(identifier="TestFeature", display_name="Test Feature")
        test_handler = UnobservableProperty(
            identifier="TestProperty", display_name="Test Property", feature=test_feature
        )
        TestMetadata = Metadata.create(
            identifier="TestMetadata", display_name="Test Metadata", data_type=String, feature=metadata_feature
        )

        with pytest.raises(
            InvalidMetadata,
            match=(
                "Unable to decode metadata 'TestMetadata' in UnobservableProperty 'TestProperty': "
                "Invalid field 'TestMetadata' in message 'TestMetadata': Expected wire type 'LEN', received 'VARINT'."
            ),
        ):
            await TestMetadata.from_buffer(
                test_handler,
                {
                    "sila-org.silastandard-none-metadatafeature-v1-metadata-testmetadata-bin": Integer(42).encode(
                        None, 1
                    )
                },
            )


class TestFromNative:
    async def test_should_initialize_from_native(self):
        # Create metadata
        feature = Feature(identifier="MetadataFeature", display_name="Metadata Feature")
        TestMetadata = Metadata.create(
            identifier="TestMetadata", display_name="Test Metadata", data_type=String, feature=feature
        )
        metadata = await TestMetadata.from_native(feature.context, "Hello, World!")

        assert metadata == TestMetadata(value=String("Hello, World!"))


class TestToNative:
    async def test_should_convert_to_native(self):
        # Create metadata
        feature = Feature(identifier="MetadataFeature", display_name="Metadata Feature")
        TestMetadata = Metadata.create(
            identifier="TestMetadata", display_name="Test Metadata", data_type=String, feature=feature
        )
        metadata = TestMetadata(value=String("Hello, World!"))

        native = await metadata.to_native(feature.context)

        assert native == "Hello, World!"

    async def test_should_raise_on_malformed_native(self):
        # Create metadata
        feature = Feature(identifier="MetadataFeature", display_name="Metadata Feature")
        TestMetadata = Metadata.create(
            identifier="TestMetadata", display_name="Test Metadata", data_type=String, feature=feature
        )
        DataType = Structure.create({"value": Element(identifier="Value", display_name="Value", data_type=String)})
        metadata = TestMetadata(value=DataType(value={}))

        with pytest.raises(
            InvalidMetadata,
            match="Unable to decode metadata 'TestMetadata': Missing field 'Value' in message 'Structure'.",
        ):
            await metadata.to_native(feature.context)
