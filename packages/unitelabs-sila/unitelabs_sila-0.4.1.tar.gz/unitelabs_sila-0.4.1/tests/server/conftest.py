import pytest
from examples.server.binary_transfer_test import BinaryTransferTest
from examples.server.error_handling_test import ErrorHandlingTest
from examples.server.list_data_type_test import ListDataTypeTest
from examples.server.metadata_consumer_test import MetadataConsumerTest
from examples.server.metadata_provider import MetadataProvider
from examples.server.observable_command_test import ObservableCommandTest
from examples.server.observable_property_test import ObservablePropertyTest
from examples.server.unobservable_command_test import UnobservableCommandTest
from examples.server.unobservable_property_test import UnobservablePropertyTest

from sila.server.cloud_server import CloudServer
from sila.server.server import Server, ServerConfig


@pytest.fixture
async def server():
    server = Server(ServerConfig(uuid="00000000-0000-0000-0000-000000000000"))

    server.register_feature(BinaryTransferTest())
    server.register_feature(ErrorHandlingTest())
    server.register_feature(ListDataTypeTest())
    server.register_feature(MetadataConsumerTest())
    server.register_feature(MetadataProvider())
    server.register_feature(ObservableCommandTest())
    server.register_feature(ObservablePropertyTest())
    server.register_feature(UnobservableCommandTest())
    server.register_feature(UnobservablePropertyTest())

    yield server

    await server.stop()


@pytest.fixture
async def cloud_server():
    cloud_server = CloudServer()

    cloud_server.register_feature(BinaryTransferTest())
    cloud_server.register_feature(ErrorHandlingTest())
    cloud_server.register_feature(ListDataTypeTest())
    cloud_server.register_feature(MetadataConsumerTest())
    cloud_server.register_feature(MetadataProvider())
    cloud_server.register_feature(ObservableCommandTest())
    cloud_server.register_feature(ObservablePropertyTest())
    cloud_server.register_feature(UnobservableCommandTest())
    cloud_server.register_feature(UnobservablePropertyTest())

    yield cloud_server

    await cloud_server.stop()
