import unittest.mock

import pytest

from sila.framework.common.feature import Feature
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.framework_error import InvalidMetadata
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.server.observable_property import ObservableProperty
from sila.server.server import Server
from sila.testing.raises import raises


class TestSubscribe:
    async def test_should_subscribe_observable_property(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/ObservablePropertyTest/v1/Property/FixedValue"
        )
        response = [item async for item in observable_property.subscribe()]

        # Assert that the method returns the correct value
        assert response == [Integer(42).encode(number=1)]

    async def test_should_raise_defined_execution_error(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseDefinedExecutionErrorOnSubscribe"
        )

        iterator = observable_property.subscribe()
        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await iterator.__anext__()

    async def test_should_attach_defined_execution_error_to_feature(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseDefinedExecutionErrorOnSubscribe"
        )

        def function(**kwargs):
            msg = "SiLA2_test_error_message"
            raise DefinedExecutionError.create(identifier="TestError", display_name="TestError")(msg)

        observable_property.function = function

        iterator = observable_property.subscribe()
        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await iterator.__anext__()

    async def test_should_raise_undefined_execution_error(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseUndefinedExecutionErrorOnSubscribe"
        )

        iterator = observable_property.subscribe()
        with pytest.raises(UndefinedExecutionError, match=r"SiLA2_test_error_message"):
            await iterator.__anext__()

    async def test_should_raise_defined_execution_error_after_value_was_sent(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseDefinedExecutionErrorAfterValueWasSent"
        )

        iterator = observable_property.subscribe()
        await iterator.__anext__()
        with pytest.raises(DefinedExecutionError, match=r"SiLA2_test_error_message"):
            await iterator.__anext__()

    async def test_should_raise_undefined_execution_error_after_value_was_sent(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/ErrorHandlingTest/v1/Property/RaiseUndefinedExecutionErrorAfterValueWasSent"
        )

        iterator = observable_property.subscribe()
        await iterator.__anext__()
        with pytest.raises(UndefinedExecutionError, match=r"SiLA2_test_error_message"):
            await iterator.__anext__()

    async def test_should_catch_exceptions(self, server: Server):
        # Subscribe observable property
        feature = Feature(identifier="TestFeature", display_name="TestFeature")
        server.register_feature(feature)
        observable_property = ObservableProperty(
            identifier="ObservableProperty",
            display_name="Observable Property",
            function=unittest.mock.Mock(side_effect=ValueError("Invalid value received")),
            feature=feature,
        )

        with pytest.raises(UndefinedExecutionError, match=r"Invalid value received"):
            await observable_property.subscribe().__anext__()

    async def test_should_intercept_metadata(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/MetadataConsumerTest/v1/Property/ReceivedStringMetadataAsCharacters"
        )
        response = await observable_property.subscribe(
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String("C").encode(
                    number=1
                )
            }
        ).__anext__()

        # Assert that the method returns the correct value
        assert response == String("C").encode(number=1)

    async def test_should_ignore_additional_metadata(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/ObservablePropertyTest/v1/Property/FixedValue"
        )
        response = await observable_property.subscribe(
            metadata={
                "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String().encode(number=1)
            }
        ).__anext__()

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_raise_on_invalid_metadata(self, server: Server):
        # Subscribe observable property
        observable_property = server.get_observable_property(
            "org.silastandard/test/MetadataConsumerTest/v1/Property/ReceivedStringMetadataAsCharacters"
        )

        with pytest.raises(
            InvalidMetadata,
            match=r"Missing metadata 'StringMetadata' in ObservableProperty 'ReceivedStringMetadataAsCharacters'\.",
        ):
            await observable_property.subscribe(
                metadata={"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": b""}
            ).__anext__()


class TestSubscribeRpcHandler:
    async def test_should_return_observable_property(self):
        async def iterator():
            yield Integer(42).encode(number=1)

        # Subscribe observable property
        observable_property = ObservableProperty(identifier="ObservableProperty", display_name="Observable Property")
        observable_property.subscribe = unittest.mock.Mock(return_value=iterator())
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        response = await observable_property.subscribe_rpc_handler(b"", context).__anext__()

        # Assert that the method returns the correct value
        assert response == Integer(42).encode(number=1)

    async def test_should_ignore_parameters(self):
        async def iterator():
            yield Integer(42).encode(number=1)

        # Subscribe observable property
        observable_property = ObservableProperty(identifier="ObservableProperty", display_name="Observable Property")
        observable_property.subscribe = unittest.mock.Mock(return_value=iterator())
        context = unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        await observable_property.subscribe_rpc_handler(String("Hello, World!").encode(number=1), context).__anext__()

        # Assert that the method returns the correct value
        observable_property.subscribe.assert_called_once_with({})

    async def test_should_forward_metadata(self):
        async def iterator():
            yield Integer(42).encode(number=1)

        # Subscribe observable property
        observable_property = ObservableProperty(identifier="ObservableProperty", display_name="Observable Property")
        observable_property.subscribe = unittest.mock.Mock(return_value=iterator())
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
        await observable_property.subscribe_rpc_handler(b"", context).__anext__()

        # Assert that the method returns the correct value
        observable_property.subscribe.assert_called_once_with(
            {"sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin": String().encode(number=1)}
        )

    async def test_should_raise_sila_error(self):
        async def iterator():
            msg = "Invalid value received"
            raise UndefinedExecutionError(msg)
            yield Integer(42).encode(number=1)

        # Subscribe observable property
        observable_property = ObservableProperty(identifier="ObservableProperty", display_name="Observable Property")
        observable_property.subscribe = unittest.mock.Mock(return_value=iterator())

        with raises(SiLAError, match=r"Invalid value received") as servicer_context:
            await observable_property.subscribe_rpc_handler(b"", servicer_context).__anext__()
