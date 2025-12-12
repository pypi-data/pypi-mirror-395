import pytest

from sila.framework.data_types.list import List
from sila.framework.data_types.string import String
from sila.server.server import Server
from sila.server.sila_service import UnimplementedFeature


class TestServerUUID:
    async def test_should_get_server_uuid(self, server: Server):
        # Get server uuid
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ServerUUID"
        )

        server_uuid = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert server_uuid == String("00000000-0000-0000-0000-000000000000").encode(number=1)


class TestServerName:
    async def test_should_get_server_name(self, server: Server):
        # Get server name
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ServerName"
        )

        server_name = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert server_name == String("SiLA Server").encode(number=1)

    async def test_should_set_server_name(self, server: Server):
        # Set server name
        unobservable_property = server.get_unobservable_command(
            "org.silastandard/core/SiLAService/v1/Command/SetServerName"
        )

        await unobservable_property.execute(String("Hello, World!").encode(number=1))


class TestServerDescription:
    async def test_should_get_server_description(self, server: Server):
        # Get server description
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ServerDescription"
        )

        server_description = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert server_description == String("").encode(number=1)


class TestServerType:
    async def test_should_get_server_type(self, server: Server):
        # Get server type
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ServerType"
        )

        server_type = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert server_type == String("ExampleServer").encode(number=1)


class TestServerVersion:
    async def test_should_get_server_version(self, server: Server):
        # Get server version
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ServerVersion"
        )

        server_version = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert server_version == String("0.1.0").encode(number=1)


class TestServerVendorUrl:
    async def test_should_get_server_vendor_url(self, server: Server):
        # Get server vendor url
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ServerVendorURL"
        )

        server_vendor_url = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert server_vendor_url == String("https://sila-standard.com").encode(number=1)


class TestImplementedFeatures:
    async def test_should_get_implemented_features(self, server: Server):
        # Get implemented features
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ImplementedFeatures"
        )

        implemented_features = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert implemented_features == List.create(String)(
            [
                String("org.silastandard/core/SiLAService/v1"),
                String("org.silastandard/test/BinaryTransferTest/v1"),
                String("org.silastandard/test/ErrorHandlingTest/v1"),
                String("org.silastandard/test/ListDataTypeTest/v1"),
                String("org.silastandard/test/MetadataConsumerTest/v1"),
                String("org.silastandard/test/MetadataProvider/v1"),
                String("org.silastandard/test/ObservableCommandTest/v1"),
                String("org.silastandard/test/ObservablePropertyTest/v1"),
                String("org.silastandard/test/UnobservableCommandTest/v1"),
                String("org.silastandard/test/UnobservablePropertyTest/v1"),
            ]
        ).encode(number=1)


class TestGetFeatureDefinition:
    async def test_should_get_feature_definition(self, server: Server):
        # Get feature definition
        observable_property = server.get_unobservable_command(
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition"
        )

        feature_definition = await observable_property.execute(
            String("org.silastandard/core/SiLAService/v1").encode(number=1)
        )

        # Assert that the method returns the correct value
        with open("./tests/resources/SiLAService-v1_0.sila.xml", mode="r", encoding="utf-8") as handle:
            expected = handle.read()
            assert feature_definition == String(expected).encode(number=1)

    async def test_should_raise_on_unimplemented_feature(self, server: Server):
        # Get feature definition
        observable_property = server.get_unobservable_command(
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition"
        )

        with pytest.raises(UnimplementedFeature):
            await observable_property.execute(String("org.silastandard/none/UnknownFeature/v1").encode(number=1))
