import dataclasses

from sila import datetime
from sila.server import Feature, Integer, UnobservableProperty


@dataclasses.dataclass
class UnobservablePropertyTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "UnobservablePropertyTest"
    display_name: str = "Unobservable Property Test"
    description: str = "This feature tests a static and a dynamic unobservable property."

    def __post_init__(self):
        UnobservableProperty(
            identifier="AnswerToEverything",
            display_name="Answer To Everything",
            description="Returns the answer to the ultimate question of life, the universe, and everything. 42.",
            data_type=Integer,
            function=lambda metadata: {"AnswerToEverything": 42},
            feature=self,
        )

        UnobservableProperty(
            identifier="SecondsSince1970",
            display_name="Seconds Since 1970",
            description="Returns the unix timestamp: The time in seconds since January 1st of 1970.",
            data_type=Integer,
            function=lambda metadata: {"SecondsSince1970": int(datetime.datetime.now().timestamp())},
            feature=self,
        )
