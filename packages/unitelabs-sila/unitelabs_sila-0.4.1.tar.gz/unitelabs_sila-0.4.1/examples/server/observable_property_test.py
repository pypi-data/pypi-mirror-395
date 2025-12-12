import asyncio
import dataclasses

from sila.server import Boolean, Element, Feature, Integer, ObservableProperty, UnobservableCommand


@dataclasses.dataclass
class ObservablePropertyTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "ObservablePropertyTest"
    display_name: str = "Observable Property Test"
    description: str = "This is a test feature to test observable properties."

    editable: int = dataclasses.field(init=False, default=0)
    editable_event: asyncio.Event = dataclasses.field(init=False, default_factory=asyncio.Event)

    def __post_init__(self):
        ObservableProperty(
            identifier="FixedValue",
            display_name="Fixed Value",
            description="Always returns 42 and never changes.",
            data_type=Integer,
            function=self.subscribe_fixed_value,
            feature=self,
        )

        ObservableProperty(
            identifier="Alternating",
            display_name="Alternating",
            description="Switches every second between true and false",
            data_type=Boolean,
            function=self.subscribe_alternating,
            feature=self,
        )

        ObservableProperty(
            identifier="Editable",
            display_name="Editable",
            description="Can be set through SetValue command",
            data_type=Integer,
            function=self.subscribe_editable,
            feature=self,
        )

        UnobservableCommand(
            identifier="SetValue",
            display_name="Set Value",
            description="Changes the value of Editable",
            parameters={
                "value": Element(
                    identifier="Value",
                    display_name="Value",
                    description="The new value",
                    data_type=Integer,
                ),
            },
            function=self.set_value,
            feature=self,
        )

    def subscribe_fixed_value(self, metadata):
        yield {"FixedValue": 42}

    async def subscribe_alternating(self, metadata):
        alternating = True

        while True:
            yield {"Alternating": alternating}
            alternating = not alternating
            await asyncio.sleep(1)

    async def subscribe_editable(self, metadata):
        while True:
            self.editable_event.clear()

            yield {"Editable": self.editable}

            await self.editable_event.wait()

    def set_value(self, value: int, metadata) -> None:
        self.editable = value
        self.editable_event.set()
