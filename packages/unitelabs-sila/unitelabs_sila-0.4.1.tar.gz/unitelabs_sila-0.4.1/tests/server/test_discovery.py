import pathlib

import pytest

from sila.server import Server, ServerConfig
from sila.server.discovery import Discovery


class TestFindIpAddress:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ("localhost", "127.0.0.1"),
            ("127.0.0.1", "127.0.0.1"),
        ],
    )
    def test_should_find_ip_address(self, value: str, expected: str):
        assert Discovery.find_ip_address(value) == expected

    def test_should_use_localhost_for_invalid_address(
        self,
    ):
        assert Discovery.find_ip_address("invalid") == "127.0.0.1"


class TestCreateService:
    def test_should_broadcast_properties(self):
        # Create Server
        server = Server()

        # Create service
        service = Discovery.create_service(server)

        # Assert that the method returns the correct value
        assert service.name == f"{server.uuid}._sila._tcp.local."
        assert service.properties.get(b"version", "") == server.version.encode("utf-8")
        assert service.properties.get(b"server_name", "") == server.name.encode("utf-8")
        assert server.description.encode("utf-8").startswith(service.properties.get(b"description", b"") or b"")

    def test_should_broadcast_certificate(self):
        # Create Server
        cert = pathlib.Path("./tests/resources/cert.pem").read_bytes()
        key = pathlib.Path("./tests/resources/key.pem").read_bytes()
        server = Server(ServerConfig(tls=True, certificate_chain=cert, private_key=key))

        # Create service
        service = Discovery.create_service(server)

        # Assert that the method returns the correct value
        assert cert.strip() == b"\n".join(
            [v for k, v in service.properties.items() if k.startswith(b"ca") and v is not None]
        )
