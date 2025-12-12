import argparse
import asyncio
import contextlib
import logging

from sila.server.cloud_server import CloudServer
from sila.server.discovery import Discovery
from sila.server.server import Server, ServerConfig

from .any_type_test import AnyTypeTest
from .authentication_service import AuthenticationService
from .authentication_test import AuthenticationTest
from .authorization_service import AuthorizationService
from .basic_data_types_test import BasicDataTypesTest
from .binary_transfer_test import BinaryTransferTest
from .error_handling_test import ErrorHandlingTest
from .list_data_type_test import ListDataTypeTest
from .metadata_consumer_test import MetadataConsumerTest
from .metadata_provider import MetadataProvider
from .multi_client_test import MultiClientTest
from .observable_command_test import ObservableCommandTest
from .observable_property_test import ObservablePropertyTest
from .structure_data_type_test import StructureDataTypeTest
from .unobservable_command_test import UnobservableCommandTest
from .unobservable_property_test import UnobservablePropertyTest

logging.basicConfig(level=logging.DEBUG, force=True)


def sila_server(hostname: str, port: int) -> Server:
    server = Server(
        ServerConfig(
            hostname=hostname,
            port=port,
            tls=False,
            uuid="2be7e3fe-6a53-48fd-81d9-116f7cc5b59b",
            name="Test Server",
            type="TestServer",
            version="0.1",
            description="This is a test server",
            vendor_url="https://gitlab.com/SiLA2/sila_python",
        ),
    )

    server.register_feature(AnyTypeTest())
    server.register_feature(AuthenticationService())
    server.register_feature(AuthenticationTest())
    server.register_feature(AuthorizationService())
    server.register_feature(BasicDataTypesTest())
    server.register_feature(BinaryTransferTest())
    server.register_feature(ErrorHandlingTest())
    server.register_feature(ListDataTypeTest())
    server.register_feature(MetadataConsumerTest())
    server.register_feature(MetadataProvider())
    server.register_feature(MultiClientTest())
    server.register_feature(ObservableCommandTest())
    server.register_feature(ObservablePropertyTest())
    server.register_feature(StructureDataTypeTest())
    server.register_feature(UnobservableCommandTest())
    server.register_feature(UnobservablePropertyTest())

    return server


async def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-a",
        "--hostname",
        default="localhost",
        help="The target hostname to bind the server to. Defaults to `localhost`.",
    )
    argparser.add_argument(
        "-p",
        "--port",
        default=50001,
        type=int,
        help="The target port to bind to. If set to `0` an available port is chosen at runtime. Defaults to `50001`.",
    )
    argparser.add_argument("--disable-discovery", action="store_true", help="Disable SiLA Server Discovery")
    args = argparser.parse_args()

    tasks = []

    server = sila_server(args.hostname, args.port)
    await server.start()
    tasks.append(server.wait_for_termination())

    cloud_server = CloudServer()
    cloud_server.context = server
    await cloud_server.start()
    tasks.append(cloud_server.wait_for_termination())

    discovery = None
    if not args.disable_discovery:
        discovery = Discovery(server)
        await discovery.start()

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        if discovery:
            await discovery.stop()

        await cloud_server.stop(grace=5)
        await server.stop(grace=5)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
