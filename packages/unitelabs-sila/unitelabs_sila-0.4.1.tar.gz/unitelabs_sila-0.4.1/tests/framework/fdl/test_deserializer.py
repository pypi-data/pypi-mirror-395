import re
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.data_types.boolean import Boolean
from sila.framework.data_types.date import Date
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.real import Real
from sila.framework.data_types.time import Time
from sila.framework.data_types.timestamp import Timestamp
from sila.framework.data_types.timezone import Timezone
from sila.framework.fdl.deserializer import Characters, Deserializer, EndDocument, EndElement, StartElement, Token
from sila.framework.fdl.parse_error import ParseError


class TestRunning:
    def test_should_not_run_on_default(self):
        # Create deserializer
        deserializer = Deserializer()

        # Assert that the method returns the correct value
        assert deserializer.running is False

    def test_should_run_on_start_document(self):
        # Create deserializer
        deserializer = Deserializer()

        # Start document
        deserializer.startDocument()

        # Assert that the method returns the correct value
        assert deserializer.running is True

    def test_should_not_run_on_end_document(self):
        # Create deserializer
        deserializer = Deserializer()

        # Start document
        deserializer.startDocument()
        deserializer.endDocument()

        # Assert that the method returns the correct value
        assert deserializer.running is False

    def test_should_call_handlers_on_end_document(self):
        # Create deserializer
        deserializer = Deserializer()
        token = None

        def handler():
            nonlocal token
            token = yield from deserializer.read()

        generator = handler()
        deserializer.register(generator)

        # Start document
        deserializer.startDocument()
        deserializer.endDocument()

        # Assert that the method returns the correct value
        assert token == EndDocument()


class TestResult:
    def test_should_not_be_done_by_default(self):
        # Create deserializer
        deserializer = Deserializer()

        # Check if done
        done = deserializer.done()

        # Assert that the method returns the correct value
        assert done is False

    def test_should_raise_without_result(self):
        # Create deserializer
        deserializer = Deserializer()

        # Assert that the method returns the correct value
        with pytest.raises(RuntimeError, match=re.escape("Result is not set.")):
            deserializer.result()

    def test_should_set_result(self):
        # Create deserializer
        deserializer = Deserializer()
        value = unittest.mock.sentinel.result

        # Set result
        deserializer.set_result(value)

        # Assert that the method returns the correct value
        assert deserializer.done() is True
        assert deserializer.result() == value

    def test_should_set_exception(self):
        # Create deserializer
        deserializer = Deserializer()
        exception = RuntimeError()

        # Set result
        deserializer.set_exception(exception)

        # Assert that the method returns the correct value
        assert deserializer.done() is True
        with pytest.raises(RuntimeError):
            deserializer.result()


class TestStartDocument:
    async def test_should_set_running(self):
        # Create deserializer
        deserializer = Deserializer()

        # Start document
        deserializer.startDocument()

        # Assert that the method returns the correct value
        assert deserializer.running is True


class TestEndDocument:
    async def test_should_set_running(self):
        # Create deserializer
        deserializer = Deserializer()

        # End document
        deserializer.endDocument()

        # Assert that the method returns the correct value
        assert deserializer.running is False

    async def test_should_close_handlers(self):
        # Create deserializer
        deserializer = Deserializer()

        def handler():
            token = yield

            return token

        generator = handler()
        deserializer.register(generator)

        # End document
        deserializer.endDocument()

        # Assert that the method returns the correct value
        assert deserializer.result() == EndDocument()


class TestStartElement:
    def test_should_raise_without_handler(self):
        # Create deserializer
        deserializer = Deserializer()

        # Detect next token
        with pytest.raises(
            ValueError, match=re.escape("Received start element with name 'Root', but no handler registered.")
        ):
            deserializer.startElement("Root")

    def test_should_read_start_element(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read start element
        generator = deserializer.read_start_element("Root")
        deserializer.register(generator)

        # Detect next token
        deserializer.startElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == StartElement("Root")

    def test_should_raise_on_unexpected_name(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read start element
        generator = deserializer.read_start_element("AnotherName")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'AnotherName', received start element with name 'Root'."),
        ) as error:
            deserializer.startElement("Root")

        assert error.value.path == ["Root"]

    def test_should_raise_on_characters(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read start element
        generator = deserializer.read_start_element("Element")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'Element', received characters '['Hello, World!']'."),
        ) as error:
            deserializer.characters("Hello, World!")
            deserializer.endElement("Root")

        assert error.value.path == ["Root"]

    def test_should_raise_on_end_element(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read start element
        generator = deserializer.read_start_element("Element")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ParseError,
            match=re.escape("Expected start element with name 'Element', received end element with name 'Root'."),
        ) as error:
            deserializer.endElement("Root")

        assert error.value.path == ["Root"]

    def test_should_raise_on_unexpected_token(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read start element
        generator = deserializer.read_start_element("Root")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ValueError, match=re.escape("Expected start element with name 'Root', received token 'Token()'.")
        ):
            generator.send(Token())


class TestEndElement:
    def test_should_raise_without_handler(self):
        # Create deserializer
        deserializer = Deserializer()

        # Detect next token
        with pytest.raises(
            ValueError, match=re.escape("Received end element with name 'Root', but no handler registered.")
        ):
            deserializer.endElement("Root")

    def test_should_raise_on_invalid_order(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read end element
        generator = deserializer.read_end_element("Root")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ValueError, match=re.escape("Did not expect an end element, received end element with name 'Root'.")
        ):
            deserializer.endElement("Root")

    def test_should_raise_on_invalid_name(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read end element
        generator = deserializer.read_end_element("Ignored")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ValueError,
            match=re.escape("Expected end element with name 'Root', received end element with name 'Element'."),
        ):
            deserializer.endElement("Element")

    def test_should_read_end_element(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read end element
        generator = deserializer.read_end_element("Root")
        deserializer.register(generator)

        # Detect next token
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == EndElement("Root")

    def test_should_raise_on_unexpected_name(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read end element
        generator = deserializer.read_end_element("Element")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ParseError,
            match=re.escape("Expected end element with name 'Element', received end element with name 'Root'."),
        ) as error:
            deserializer.endElement("Root")

        assert error.value.path == ["Root"]

    def test_should_raise_on_characters(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read end element
        generator = deserializer.read_end_element("Root")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ParseError,
            match=re.escape("Expected end element with name 'Root', received characters '['Hello, World!']'."),
        ) as error:
            deserializer.characters("Hello, World!")
            deserializer.endElement("Root")

        assert error.value.path == ["Root"]

    def test_should_raise_on_start_element(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read end element
        generator = deserializer.read_end_element("Root")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ParseError,
            match=re.escape("Expected end element with name 'Root', received start element with name 'Element'."),
        ) as error:
            deserializer.startElement("Element")

        assert error.value.path == ["Root", "Element"]

    def test_should_raise_on_unexpected_token(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read end element
        generator = deserializer.read_end_element("Root")
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ValueError, match=re.escape("Expected end element with name 'Root', received token 'Token()'.")
        ):
            generator.send(Token())


class TestCharacters:
    def test_should_read_characters(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read characters
        def handler():
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Root")

            return characters

        generator = handler()
        deserializer.register(generator)

        # Detect next token
        deserializer.characters("Hello, World!")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == Characters(["Hello, World!"])

    def test_should_read_consecutive_characters(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read characters
        def handler():
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Root")

            return characters

        generator = handler()
        deserializer.register(generator)

        # Detect next token
        deserializer.characters("Hello,")
        deserializer.characters("World!")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == Characters(["Hello,", "World!"])

    def test_should_read_empty_characters(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read characters
        def handler():
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Root")

            return characters

        generator = handler()
        deserializer.register(generator)

        # Detect next token
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == Characters([])

    def test_should_raise_on_start_element(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read characters
        def handler():
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Root")

            return characters

        generator = handler()
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(
            ParseError,
            match=re.escape("Expected characters, received start element with name 'Element'."),
        ) as error:
            deserializer.startElement("Element")

        assert error.value.path == ["Root", "Element"]

    def test_should_raise_on_unexpected_token(self):
        # Create deserializer
        deserializer = Deserializer()
        deserializer._names = ["Root"]

        # Read characters
        def handler():
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Root")

            return characters

        generator = handler()
        deserializer.register(generator)

        # Detect next token
        with pytest.raises(ValueError, match=re.escape("Expected characters, received token 'Token()'.")):
            generator.send(Token())


class TestPeek:
    def test_should_peek_start_element(self):
        # Create deserializer
        deserializer = Deserializer()

        # Peek element
        def handler():
            token = yield from deserializer.peek()

            yield from deserializer.read_start_element("Root")
            yield from deserializer.read_start_element("Element")
            yield from deserializer.read_end_element("Element")
            yield from deserializer.read_end_element("Root")

            return token

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.startElement("Element")
        deserializer.endElement("Element")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == StartElement("Root")

    def test_should_peek_nested_start_element(self):
        # Create deserializer
        deserializer = Deserializer()

        # Peek element
        def handler():
            yield from deserializer.read_start_element("Root")

            token = yield from deserializer.peek()

            yield from deserializer.read_start_element("Element")
            yield from deserializer.read_end_element("Element")
            yield from deserializer.read_end_element("Root")

            return token

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.startElement("Element")
        deserializer.endElement("Element")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == StartElement("Element")

    def test_should_peek_characters(self):
        # Create deserializer
        deserializer = Deserializer()

        # Peek element
        def handler():
            yield from deserializer.read_start_element("Root")
            yield from deserializer.read_start_element("Element")

            token = yield from deserializer.peek()
            yield from deserializer.read_characters()

            yield from deserializer.read_end_element("Element")
            yield from deserializer.read_end_element("Root")

            return token

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.startElement("Element")
        deserializer.characters("Hello, World!")
        deserializer.endElement("Element")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == Characters(["Hello, World!"])

    def test_should_peek_end_element(self):
        # Create deserializer
        deserializer = Deserializer()

        # Peek element
        def handler():
            yield from deserializer.read_start_element("Root")
            yield from deserializer.read_start_element("Element")

            token = yield from deserializer.peek()
            yield from deserializer.read_end_element("Element")

            yield from deserializer.read_end_element("Root")

            return token

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.startElement("Element")
        deserializer.endElement("Element")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == EndElement("Element")


class TestReadString:
    def test_should_read_string(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_str()
            yield from deserializer.read_end_element("Root")

            return value.value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Hello, World!")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == "Hello, World!"

    def test_should_read_long_string(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_str()
            yield from deserializer.read_end_element("Root")

            return value.value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters(
            "  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor\n"
        )
        deserializer.characters(
            "  invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et\n"
        )
        deserializer.characters("  accusam et justo duo dolores et ea rebum.\n")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == (
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor\n"
            "invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et\n"
            "accusam et justo duo dolores et ea rebum."
        )


class TestReadBoolean:
    @pytest.mark.parametrize(["xml", "data_type"], [("Yes", Boolean(True)), ("No", Boolean(False))])
    def test_should_read_boolean(self, xml: str, data_type: Boolean):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_boolean()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters(xml)
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == data_type

    def test_should_raise_on_invalid_boolean(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_boolean()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Invalid")

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Root' with value 'Invalid' to Boolean.")):
            deserializer.endElement("Root")


class TestReadInteger:
    @pytest.mark.parametrize(
        ["xml", "data_type"], [("5124", Integer(5124)), ("-1000", Integer(-1000)), ("123000", Integer(123000))]
    )
    def test_should_write_integer(self, xml: str, data_type: Integer):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_integer()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters(xml)
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == data_type

    def test_should_raise_on_invalid_integer(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_integer()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Invalid")

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Root' with value 'Invalid' to Integer.")):
            deserializer.endElement("Root")


class TestReadFloat:
    @pytest.mark.parametrize(
        ["xml", "data_type"],
        [
            ("3.1415926", Real(3.1415926)),
            ("-1e3", Real(-1000)),
            ("1.23e-3", Real(0.00123)),
            ("1.23456e2", Real(123.456)),
            ("1.23e5", Real(123000)),
        ],
    )
    def test_should_read_float(self, xml: str, data_type: Real):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_float()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters(xml)
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == data_type

    def test_should_raise_on_invalid_float(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_float()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Invalid")

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Root' with value 'Invalid' to Real.")):
            deserializer.endElement("Root")


class TestReadDate:
    @pytest.mark.parametrize(
        ["xml", "data_type"],
        [
            ("2022-08-05", Date(2022, 8, 5)),
            ("2022-08-05Z", Date(2022, 8, 5, Timezone())),
            ("2022-08-05-02:30", Date(2022, 8, 5, Timezone(hours=-3, minutes=30))),
        ],
    )
    def test_should_read_date(self, xml: str, data_type: Date):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_date()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters(xml)
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == data_type

    def test_should_raise_on_invalid_date(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_date()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Invalid")

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Root' with value 'Invalid' to Date.")):
            deserializer.endElement("Root")


class TestReadTime:
    @pytest.mark.parametrize(
        ["xml", "data_type"],
        [
            ("12:34:56.789", Time(12, 34, 56, 789)),
            ("12:34:56.789Z", Time(12, 34, 56, 789, Timezone())),
            ("12:34:56.789-02:30", Time(12, 34, 56, 789, Timezone(hours=-3, minutes=30))),
        ],
    )
    def test_should_read_time(self, xml: str, data_type: Time):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_time()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters(xml)
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == data_type

    def test_should_raise_on_invalid_time(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_time()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Invalid")

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Root' with value 'Invalid' to Time.")):
            deserializer.endElement("Root")


class TestReadTimestamp:
    @pytest.mark.parametrize(
        ["xml", "data_type"],
        [
            ("2022-08-05T12:34:56.789", Timestamp(2022, 8, 5, 12, 34, 56, 789)),
            (
                "2022-08-05T12:34:56.789Z",
                Timestamp(2022, 8, 5, 12, 34, 56, 789, Timezone()),
            ),
            (
                "2022-08-05T12:34:56.789-02:30",
                Timestamp(2022, 8, 5, 12, 34, 56, 789, Timezone(hours=-3, minutes=30)),
            ),
        ],
    )
    def test_should_read_timestamp(self, xml: str, data_type: Timezone):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_timestamp()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters(xml)
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == data_type

    def test_should_raise_on_invalid_timestamp(self):
        # Create deserializer
        deserializer = Deserializer()

        # Read characters
        def handler():
            yield from deserializer.read_start_element("Root")
            value = yield from deserializer.read_timestamp()
            yield from deserializer.read_end_element("Root")

            return value

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Invalid")

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Could not convert 'Root' with value 'Invalid' to Timestamp.")):
            deserializer.endElement("Root")


class TestHandlers:
    def test_should_handle_elements(self):
        # Create deserializer
        deserializer = Deserializer()

        # Handle elements
        def handler():
            yield from deserializer.read_start_element("Root")
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Root")

            return characters

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.characters("Hello,")
        deserializer.characters("World!")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == Characters(["Hello,", "World!"])

    def test_should_handle_nested_elements(self):
        # Create deserializer
        deserializer = Deserializer()

        # Handle elements
        def handler():
            yield from deserializer.read_start_element("Root")
            yield from deserializer.read_start_element("Element")
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Element")
            yield from deserializer.read_end_element("Root")

            return characters

        deserializer.register(handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.startElement("Element")
        deserializer.characters("Hello, World!")
        deserializer.endElement("Element")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == Characters(["Hello, World!"])

    def test_should_handle_nested_elements_with_nested_handlers(self):
        # Create deserializer
        deserializer = Deserializer()

        # Handle elements
        def element_handler(deserializer: Deserializer, context: typing.Optional[dict] = None):
            yield from deserializer.read_start_element("Element")
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Element")

            return characters

        def root_handler():
            yield from deserializer.read_start_element("Root")
            token = yield from deserializer.read(element_handler)
            yield from deserializer.read_end_element("Root")

            return token

        deserializer.register(root_handler())

        # Detect next token
        deserializer.startElement("Root")
        deserializer.startElement("Element")
        deserializer.characters("Hello, World!")
        deserializer.endElement("Element")
        deserializer.endElement("Root")

        # Assert that the method returns the correct value
        assert deserializer.result() == Characters(["Hello, World!"])

    def test_should_raise_on_exception(self):
        # Create deserializer
        deserializer = Deserializer()

        # Handle elements
        def handler():
            msg = "Runtime Error"
            raise RuntimeError(msg)
            yield from deserializer.read_start_element("Root")
            characters = yield from deserializer.read_characters()
            yield from deserializer.read_end_element("Root")

            return characters

        with pytest.raises(ParseError, match=re.escape("Runtime Error")):
            deserializer.register(handler())


class TestErrorHandler:
    def test_should_handle_error(self):
        # Create deserializer
        deserializer = Deserializer()
        error = RuntimeError("Runtime Error")

        # Handle error
        with pytest.raises(ParseError, match=re.escape("Runtime Error")):
            deserializer.error(error)

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Runtime Error")):
            deserializer.result()

    def test_should_handle_fatal_error(self):
        # Create deserializer
        deserializer = Deserializer()
        error = RuntimeError("Runtime Error")

        # Handle fatal error
        with pytest.raises(ParseError, match=re.escape("Runtime Error")):
            deserializer.fatalError(error)

        # Assert that the method returns the correct value
        with pytest.raises(ParseError, match=re.escape("Runtime Error")):
            deserializer.result()

    def test_should_handle_warning(self):
        # Create deserializer
        deserializer = Deserializer()
        error = RuntimeError("Runtime Error")

        # Handle warning
        deserializer.warning(error)


class TestDeserialize:
    def test_should_handle_elements(self):
        # Create handler
        def handler(deserializer: Deserializer, context: typing.Optional[dict] = None):
            yield from deserializer.read_start_element("Root")
            characters = yield from deserializer.read_str()
            yield from deserializer.read_end_element("Root")

            return characters.value

        # Deserialize
        result = Deserializer.deserialize("<Root>Hello, World!</Root>", handler)

        # Assert that the method returns the correct value
        assert result == "Hello, World!"

    def test_should_handle_nested_elements(self):
        # Create handler
        def handler(deserializer: Deserializer, context: typing.Optional[dict] = None):
            yield from deserializer.read_start_element("Root")
            yield from deserializer.read_start_element("Element")
            characters = yield from deserializer.read_str()
            yield from deserializer.read_end_element("Element")
            yield from deserializer.read_end_element("Root")

            return characters.value

        # Deserialize
        result = Deserializer.deserialize("<Root><Element>Hello, World!</Element></Root>", handler)

        # Assert that the method returns the correct value
        assert result == "Hello, World!"

    def test_should_handle_nested_elements_with_nested_handlers(self):
        # Create handler
        def element_handler(deserializer: Deserializer, context: typing.Optional[dict] = None):
            yield from deserializer.read_start_element("Element")
            characters = yield from deserializer.read_str()
            yield from deserializer.read_end_element("Element")

            return characters.value

        def root_handler(deserializer: Deserializer, context: typing.Optional[dict] = None):
            yield from deserializer.read_start_element("Root")
            token = yield from deserializer.read(element_handler)
            yield from deserializer.read_end_element("Root")

            return token

        # Deserialize
        result = Deserializer.deserialize("<Root><Element>Hello, World!</Element></Root>", root_handler)

        # Assert that the method returns the correct value
        assert result == "Hello, World!"
