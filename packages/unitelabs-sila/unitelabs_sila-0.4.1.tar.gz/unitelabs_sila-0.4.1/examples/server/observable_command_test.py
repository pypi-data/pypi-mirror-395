import asyncio
import dataclasses

from sila import datetime
from sila.server import CommandExecution, Constrained, Element, Feature, Integer, ObservableCommand, Real, Unit


@dataclasses.dataclass
class ObservableCommandTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "ObservableCommandTest"
    display_name: str = "Observable Command Test"
    description: str = """
            This is a test feature to test observable commands.
            It specifies various observable commands and returns defined answers to validate against.
        """

    def __post_init__(self):
        ObservableCommand(
            identifier="Count",
            display_name="Count",
            description="Count from 0 to N-1 and return the current number as intermediate response.",
            parameters={
                "n": Element(
                    identifier="N",
                    display_name="N",
                    description="Number to count to",
                    data_type=Integer,
                ),
                "delay": Element(
                    identifier="Delay",
                    display_name="Delay",
                    description="The delay for each iteration",
                    data_type=Constrained.create(
                        data_type=Real, constraints=[Unit(label="s", components=[Unit.Component("Second")])]
                    ),
                ),
            },
            responses={
                "iteration_response": Element(
                    identifier="IterationResponse",
                    display_name="Iteration Response",
                    description="The last number (N-1)",
                    data_type=Integer,
                ),
            },
            intermediate_responses={
                "current_iteration": Element(
                    identifier="CurrentIteration",
                    display_name="Current Iteration",
                    description="The current number, from 0 to N-1 (excluded).",
                    data_type=Integer,
                ),
            },
            function=self.count,
            feature=self,
        )

        ObservableCommand(
            identifier="EchoValueAfterDelay",
            display_name="Echo Value After Delay",
            description=(
                'Echo the given value after the specified delay. The command state must be "waiting" until the delay '
                "has passed."
            ),
            parameters={
                "value": Element(
                    identifier="Value",
                    display_name="Value",
                    description="The value to echo",
                    data_type=Integer,
                ),
                "delay": Element(
                    identifier="Delay",
                    display_name="Delay",
                    description="The delay before the command execution starts",
                    data_type=Constrained.create(
                        data_type=Real, constraints=[Unit(label="s", components=[Unit.Component("Second")])]
                    ),
                ),
            },
            responses={
                "received_value": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The Received Value",
                    data_type=Integer,
                ),
            },
            function=self.echo_value_after_delay,
            feature=self,
        )

    async def count(self, n: int, delay: float, metadata, command_execution: CommandExecution):
        for i in range(n):
            command_execution.update_execution_info(
                progress=i / (n - 1),
                remaining_time=datetime.timedelta(seconds=delay * (n - i - 1)),
            )
            command_execution.send_intermediate_responses({"current_iteration": i})

            await asyncio.sleep(delay)

        return {"iteration_response": n - 1}

    async def echo_value_after_delay(self, value, delay, metadata, command_execution: CommandExecution):
        seconds, rest = divmod(delay, 1)
        for i in range(int(seconds)):
            await asyncio.sleep(1)
            command_execution.update_execution_info(
                progress=i / delay, remaining_time=datetime.timedelta(seconds=delay - i)
            )

        await asyncio.sleep(rest)
        return {"received_value": value}
