import textwrap
import unittest.mock

from sila.framework.data_types.void import Void
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.serializer import Serializer


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Void.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Void()

    async def test_should_convert_from_native_with_custom_value(self):
        # Create data type
        context = unittest.mock.Mock()
        assert await Void.from_native(context, None) == Void()


class TestToNative:
    async def test_should_convert_to_native(self):
        # Convert data type
        context = unittest.mock.Mock()
        assert await Void().to_native(context) is None


class TestDecode:
    async def test_should_decode(self):
        # Decode data type
        message = Void.decode(b"")

        # Assert that the method returns the correct value
        assert message == Void()


class TestEncode:
    async def test_should_encode(self):
        # Encode data type
        message = Void().encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x00"


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Void.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == (
            "<DataType>"
            "<Constrained>"
            "<DataType>"
            "<Basic>String</Basic>"
            "</DataType>"
            "<Constraints>"
            "<Length>0</Length>"
            "</Constraints>"
            "</Constrained>"
            "</DataType>"
        )

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Void.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Constrained>
                <DataType>
                  <Basic>String</Basic>
                </DataType>
                <Constraints>
                  <Length>0</Length>
                </Constraints>
              </Constrained>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = (
            "<Constrained>"
            "<DataType>"
            "<Basic>String</Basic>"
            "</DataType>"
            "<Constraints>"
            "<Length>0</Length>"
            "</Constraints>"
            "</Constrained>"
        )

        # Deserialize
        data_type = Deserializer.deserialize(xml, Void.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Void

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Constrained>
          <DataType>
            <Basic>String</Basic>
          </DataType>
          <Constraints>
            <Length>0</Length>
          </Constraints>
        </Constrained>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Void.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Void


class TestEquality:
    def test_should_be_true_on_void(self):
        # Create data type
        data_type_0 = Void()
        data_type_1 = Void()

        # Compare equality
        assert data_type_0 == data_type_1

    def test_should_be_false_on_non_void(self):
        # Create data type
        data_type = Void()

        # Compare equality
        assert data_type != unittest.mock.Mock()


class TestTruthiness:
    async def test_should_return_true(self):
        # Create data type
        data_type = Void()

        # Check truthiness
        truthiness = bool(data_type)

        # Assert that the method returns the correct value
        assert truthiness is True


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Void()
        data_type_1 = Void()

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
