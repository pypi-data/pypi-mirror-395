import builtins
import collections.abc
import dataclasses
import enum

import typing_extensions as typing

from ..data_types.binary import Binary
from ..data_types.string import String
from ..fdl import Characters, Deserializer, EndElement, Serializer, StartElement
from .constraint import Constraint

if typing.TYPE_CHECKING:
    from ..data_types import BasicType, List

T = typing.TypeVar("T", String, Binary)


class SchemaType(str, enum.Enum):
    """
    Enumeration of schema types used in the Schema constraint.

    This enumeration defines the types of schemas that can be used
    for validation. It currently supports XML and JSON.
    """

    XML = "Xml"
    """Represents the XML schema type."""

    JSON = "Json"
    """Represents the JSON schema type."""


@dataclasses.dataclass
class Schema(Constraint[T]):
    """A constraint that enforces the structure of a value to match a specific schema, either XML or JSON."""

    Type: typing.ClassVar[builtins.type[SchemaType]] = SchemaType
    """
    Enumeration of schema types used in the Schema constraint.
    """

    type: typing.Union[typing.Literal["Xml", "Json"], SchemaType]
    """
    The schema type, either 'Xml' or 'Json'.
    """

    url: typing.Optional[str] = None
    """
    An optional URL pointing to the schema.
    """

    inline: typing.Optional[str] = None
    """
    Optional inline content representing the schema.
    """

    def __post_init__(self):
        if self.url is None and self.inline is None:
            msg = "Either 'url' or 'inline' must be provided."
            raise ValueError(msg)

        if self.url is not None and self.inline is not None:
            msg = "'url' and 'inline' cannot both be provided."
            raise ValueError(msg)

        self.type = self.type.value if isinstance(self.type, SchemaType) else self.type

    @typing.override
    async def validate(self, value: T) -> bool:
        if not isinstance(value, (String, Binary)):
            msg = f"Expected value of type 'String' or 'Binary', received '{type(value).__name__}'."
            raise TypeError(msg)

        # TODO: Load xml or json schema to validate whether `value` follows that schema

        return True

    @typing.override
    def serialize(self, serializer: Serializer) -> None:
        serializer.start_element("Schema")
        serializer.write_str("Type", self.type)
        if self.url is not None:
            serializer.write_str("Url", self.url)
        if self.inline is not None:
            serializer.write_str("Inline", self.inline)
        serializer.end_element("Schema")

    @typing.override
    @classmethod
    def deserialize(
        cls, deserializer: Deserializer, context: typing.Optional[dict] = None
    ) -> collections.abc.Generator[None, typing.Any, typing.Self]:
        data_type: typing.Union[None, type["BasicType"], type["List"]] = (context or {}).get("data_type", None)

        if data_type is None:
            msg = "Missing 'data_type' in context."
            raise ValueError(msg)

        if not issubclass(data_type, (String, Binary)):
            msg = f"Expected constraint's data type to be 'String' or 'Binary', received '{data_type.__name__}'."
            raise ValueError(msg)

        yield from deserializer.read_start_element(name="Schema")

        # Type
        yield from deserializer.read_start_element(name="Type")
        schema_type = yield from deserializer.read_str()
        try:
            schema_type = SchemaType(schema_type.value).value
        except ValueError:
            msg = f"Expected a valid 'Type' value, received '{schema_type}'."
            raise ValueError(msg) from None
        yield from deserializer.read_end_element(name="Type")

        url: typing.Optional[String] = None
        inline: typing.Optional[String] = None

        token = yield
        if isinstance(token, StartElement):
            if token.name == "Url":
                # Url
                url = yield from deserializer.read_str()
                yield from deserializer.read_end_element(name="Url")
            elif token.name == "Inline":
                # Inline
                inline = yield from deserializer.read_str()
                yield from deserializer.read_end_element(name="Inline")
            else:
                msg = (
                    f"Expected start element with name 'Url' or 'Inline', "
                    f"received start element with name '{token.name}'."
                )
                raise ValueError(msg)
        elif isinstance(token, Characters):
            msg = f"Expected start element with name 'Url' or 'Inline', received characters '{token.value}'."
            raise ValueError(msg)
        elif isinstance(token, EndElement):
            msg = f"Expected start element with name 'Url' or 'Inline', received end element with name '{token.name}'."
            raise ValueError(msg)

        yield from deserializer.read_end_element(name="Schema")

        return cls(
            schema_type, url=url.value if url is not None else None, inline=inline.value if inline is not None else None
        )
