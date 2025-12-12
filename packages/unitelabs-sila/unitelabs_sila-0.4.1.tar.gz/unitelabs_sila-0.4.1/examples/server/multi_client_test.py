import asyncio
import dataclasses

from sila.server import CommandExecution, Constrained, Element, Feature, ObservableCommand, Real, Unit


@dataclasses.dataclass
class MultiClientTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "MultiClientTest"
    display_name: str = "Multi Client Test"
    description: str = (
        "This is a feature to test different server behaviors when multiple clients request execution of the same "
        "command."
    )

    def __post_init__(self):
        ObservableCommand(
            identifier="RunInParallel",
            display_name="Run In Parallel",
            description="Multiple invocations of this command will be running in parallel",
            parameters={
                "duration": Element(
                    identifier="Duration",
                    display_name="Duration",
                    description="The duration of the command execution",
                    data_type=Constrained.create(
                        data_type=Real, constraints=[Unit(label="s", components=[Unit.Component("Second")])]
                    ),
                ),
            },
            function=self.run_in_parallel,
            feature=self,
        )

        ObservableCommand(
            identifier="RunQueued",
            display_name="Run Queued",
            description="Multiple invocations of this command will be queued",
            parameters={
                "duration": Element(
                    identifier="Duration",
                    display_name="Duration",
                    description="The duration of the command execution",
                    data_type=Constrained.create(
                        data_type=Real, constraints=[Unit(label="s", components=[Unit.Component("Second")])]
                    ),
                ),
            },
            function=self.run_qeued,
            feature=self,
        )

        ObservableCommand(
            identifier="RejectParallelExecution",
            display_name="Reject Parallel Execution",
            description="Invocations will be rejected, if there is another command instance already running",
            parameters={
                "duration": Element(
                    identifier="Duration",
                    display_name="Duration",
                    description="The duration of the command execution",
                    data_type=Constrained.create(
                        data_type=Real, constraints=[Unit(label="s", components=[Unit.Component("Second")])]
                    ),
                ),
            },
            function=self.reject_parallel_execution,
            feature=self,
        )

    async def run_in_parallel(self, duration: float, metadata, command_execution: CommandExecution) -> None:
        await asyncio.sleep(duration)

    async def run_qeued(self, duration: float, metadata, command_execution: CommandExecution) -> None:
        # TODO
        await asyncio.sleep(duration)

    async def reject_parallel_execution(self, duration: float, metadata, command_execution: CommandExecution) -> None:
        # TODO
        await asyncio.sleep(duration)
