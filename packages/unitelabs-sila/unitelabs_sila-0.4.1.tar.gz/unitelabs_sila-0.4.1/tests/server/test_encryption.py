import typing_extensions as typing
from cryptography import x509

from sila.server import generate_certificate

COMMON_NAME = "SiLA2"
OID_SILA = x509.ObjectIdentifier("1.3.6.1.4.1.58583")


async def test_should_generate_certificate():
    host = "127.0.0.1"
    uuid = "00000000-0000-0000-0000-000000000000"

    _, cert = generate_certificate(uuid, host)

    certificate = x509.load_pem_x509_certificate(cert)
    alt_names = typing.cast(
        x509.SubjectAlternativeName,
        certificate.extensions.get_extension_for_oid(x509.OID_SUBJECT_ALTERNATIVE_NAME).value,
    )

    assert certificate.issuer.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value == COMMON_NAME
    assert certificate.extensions.get_extension_for_oid(OID_SILA).value.public_bytes().decode("ascii") == uuid
    assert str(alt_names.get_values_for_type(x509.IPAddress)[0]) == host
