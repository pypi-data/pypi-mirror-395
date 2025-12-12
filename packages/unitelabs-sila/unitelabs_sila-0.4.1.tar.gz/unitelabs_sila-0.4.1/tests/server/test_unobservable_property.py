import unittest.mock

import pytest

from sila.framework.common.feature import Feature
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.framework_error import InvalidMetadata, NoMetadataAllowed
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.server.server import Server
from sila.server.unobservable_property import UnobservableProperty
from sila.testing.raises import raises


class TestRead:
    async def test_should_read_unobservable_property(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/test/UnobservablePropertyTest/v1/Property/AnswerToEverything"
        )
        response = await unobservable_property.read()

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_raise_defined_execution_error(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseDefinedExecutionErrorOnGet"
        )

        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await unobservable_property.read()

    async def test_should_attach_defined_execution_error_to_feature(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseDefinedExecutionErrorOnGet"
        )

        def function(**kwargs):
            msg = "SiLA2_test_error_message"
            raise DefinedExecutionError.create(identifier="TestError", display_name="TestError")(msg)

        unobservable_property.function = function

        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await unobservable_property.read()

    async def test_should_raise_undefined_execution_error(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseUndefinedExecutionErrorOnGet"
        )

        with pytest.raises(UndefinedExecutionError, match=r"SiLA2_test_error_message"):
            await unobservable_property.read()

    async def test_should_catch_exceptions(self, server: Server):
        # Read unobservable property
        feature = Feature(identifier="TestFeature", display_name="TestFeature")
        server.register_feature(feature)
        unobservable_property = UnobservableProperty(
            identifier="UnobservableProperty",
            display_name="Unobservable Property",
            function=unittest.mock.Mock(side_effect=ValueError("Invalid value received")),
            feature=feature,
        )

        with pytest.raises(UndefinedExecutionError, match=r"Invalid value received"):
            await unobservable_property.read()

    async def test_should_intercept_metadata(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/test/MetadataConsumerTest/v1/Property/ReceivedStringMetadata"
        )
        response = await unobservable_property.read(
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String("C").encode(
                    number=1
                )
            }
        )

        # Assert that the method returns the correct value
        assert response == String("C").encode(number=1)

    async def test_should_ignore_additional_metadata(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/test/UnobservablePropertyTest/v1/Property/AnswerToEverything"
        )
        response = await unobservable_property.read(
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String().encode(number=1)
            }
        )

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_raise_on_unallowed_metadata(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/core/SiLAService/v1/Property/ServerName"
        )

        with pytest.raises(NoMetadataAllowed, match=r"No metadata allowed for the SiLA Service feature\."):
            await unobservable_property.read(
                metadata={"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": b""}
            )

    async def test_should_raise_on_invalid_metadata(self, server: Server):
        # Read unobservable property
        unobservable_property = server.get_unobservable_property(
            "org.silastandard/test/MetadataConsumerTest/v1/Property/ReceivedStringMetadata"
        )

        with pytest.raises(
            InvalidMetadata,
            match=r"Missing metadata 'StringMetadata' in UnobservableProperty 'ReceivedStringMetadata'\.",
        ):
            await unobservable_property.read(
                metadata={"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": b""}
            )


class TestReadRpcHandler:
    async def test_should_return_unobservable_property(self):
        # Read unobservable property
        unobservable_property = UnobservableProperty(
            identifier="UnobservableProperty", display_name="Unobservable Property"
        )
        unobservable_property.read = unittest.mock.AsyncMock(return_value=Integer(42).encode(number=1))
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        response = await unobservable_property.read_rpc_handler(b"", context)

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_ignore_parameters(self):
        # Read unobservable property
        unobservable_property = UnobservableProperty(
            identifier="UnobservableProperty", display_name="Unobservable Property"
        )
        unobservable_property.read = unittest.mock.AsyncMock()
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        await unobservable_property.read_rpc_handler(String("Hello, World!").encode(number=1), context)

        # Assert that the method returns the correct value
        unobservable_property.read.assert_awaited_once_with({})

    async def test_should_forward_metadata(self):
        # Read unobservable property
        unobservable_property = UnobservableProperty(
            identifier="UnobservableProperty", display_name="Unobservable Property"
        )
        unobservable_property.read = unittest.mock.AsyncMock()
        context = unittest.mock.Mock(
            invocation_metadata=unittest.mock.Mock(
                return_value=[
                    (
                        "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin",
                        String().encode(number=1),
                    )
                ]
            )
        )
        await unobservable_property.read_rpc_handler(b"", context)

        # Assert that the method returns the correct value
        unobservable_property.read.assert_awaited_once_with(
            {"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String().encode(number=1)}
        )

    async def test_should_raise_sila_error(self):
        # Read unobservable property
        unobservable_property = UnobservableProperty(
            identifier="UnobservableProperty", display_name="Unobservable Property"
        )
        unobservable_property.read = unittest.mock.AsyncMock(
            side_effect=UndefinedExecutionError("ValueError: Invalid value received")
        )

        with raises(SiLAError, match=r"ValueError: Invalid value received") as servicer_context:
            await unobservable_property.read_rpc_handler(b"", servicer_context)
