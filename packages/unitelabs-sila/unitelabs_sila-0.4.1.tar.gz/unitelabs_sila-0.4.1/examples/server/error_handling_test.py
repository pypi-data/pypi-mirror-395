import asyncio
import collections.abc
import dataclasses

from sila.server import (
    CommandExecution,
    DefinedExecutionError,
    Feature,
    Integer,
    ObservableCommand,
    ObservableProperty,
    UndefinedExecutionError,
    UnobservableCommand,
    UnobservableProperty,
)

TestError = DefinedExecutionError.create(
    identifier="TestError",
    display_name="Test Error",
    description="An error exclusively used for testing purposes",
)


@dataclasses.dataclass
class ErrorHandlingTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "ErrorHandlingTest"
    display_name: str = "Error Handling Test"
    description: str = "Tests that errors are propagated correctly"

    def __post_init__(self):
        UnobservableProperty(
            identifier="RaiseDefinedExecutionErrorOnGet",
            display_name="Raise Defined Execution Error On Get",
            description=(
                "A property that raises a \"Test Error\" on get with the error message 'SiLA2_test_error_message'"
            ),
            data_type=Integer,
            errors={TestError.identifier: TestError},
            function=self.raise_defined_execution_error_on_get,
            feature=self,
        )

        ObservableProperty(
            identifier="RaiseDefinedExecutionErrorOnSubscribe",
            display_name="Raise Defined Execution Error On Subscribe",
            description=(
                "A property that raises a \"Test Error\" on subscribe with the error message 'SiLA2_test_error_message'"
            ),
            data_type=Integer,
            errors={TestError.identifier: TestError},
            function=self.raise_defined_execution_error_on_subscribe,
            feature=self,
        )

        UnobservableProperty(
            identifier="RaiseUndefinedExecutionErrorOnGet",
            display_name="Raise Undefined Execution Error On Get",
            description=(
                "A property that raises an Undefined Execution Error on get with the error message "
                "'SiLA2_test_error_message'"
            ),
            data_type=Integer,
            function=self.raise_undefined_execution_error_on_get,
            feature=self,
        )

        ObservableProperty(
            identifier="RaiseUndefinedExecutionErrorOnSubscribe",
            display_name="Raise Undefined Execution Error On Subscribe",
            description=(
                "A property that raises an Undefined Execution Error on subscribe with the error message "
                "'SiLA2_test_error_message'"
            ),
            data_type=Integer,
            function=self.raise_undefined_execution_error_on_subscribe,
            feature=self,
        )

        ObservableProperty(
            identifier="RaiseDefinedExecutionErrorAfterValueWasSent",
            display_name="Raise Defined Execution Error After Value Was Sent",
            description=(
                "A property that first sends the integer value 1 and then raises a Defined Execution Error with the "
                "error message 'SiLA2_test_error_message'"
            ),
            data_type=Integer,
            errors={TestError.identifier: TestError},
            function=self.raise_defined_execution_error_after_value_was_sent,
            feature=self,
        )

        ObservableProperty(
            identifier="RaiseUndefinedExecutionErrorAfterValueWasSent",
            display_name="Raise Undefined Execution Error After Value Was Sent",
            description=(
                "A property that first sends the integer value 1 and then raises a Undefined Execution Error with the "
                "error message 'SiLA2_test_error_message'"
            ),
            data_type=Integer,
            function=self.raise_undefined_execution_error_after_value_was_sent,
            feature=self,
        )

        UnobservableCommand(
            identifier="RaiseDefinedExecutionError",
            display_name="Raise Defined Execution Error",
            description="Raises the \"Test Error\" with the error message 'SiLA2_test_error_message'",
            errors={TestError.identifier: TestError},
            function=self.raise_defined_execution_error,
            feature=self,
        )

        ObservableCommand(
            identifier="RaiseDefinedExecutionErrorObservably",
            display_name="Raise Defined Execution Error Observably",
            description="Raises the \"Test Error\" with the error message 'SiLA2_test_error_message'",
            errors={TestError.identifier: TestError},
            function=self.raise_defined_execution_error_observably,
            feature=self,
        )

        UnobservableCommand(
            identifier="RaiseUndefinedExecutionError",
            display_name="Raise Undefined Execution Error",
            description="Raises an Undefined Execution Error with the error message 'SiLA2_test_error_message'",
            function=self.raise_undefined_execution_error,
            feature=self,
        )

        ObservableCommand(
            identifier="RaiseUndefinedExecutionErrorObservably",
            display_name="Raise Undefined Execution Error Observably",
            description="Raises an Undefined Execution Error with the error message 'SiLA2_test_error_message'",
            function=self.raise_undefined_execution_error_observably,
            feature=self,
        )

    def raise_defined_execution_error_on_get(self, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise TestError(msg)

    def raise_defined_execution_error_on_subscribe(self, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise TestError(msg)

    def raise_undefined_execution_error_on_get(self, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise UndefinedExecutionError(msg)

    def raise_undefined_execution_error_on_subscribe(self, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise UndefinedExecutionError(msg)

    async def raise_defined_execution_error_after_value_was_sent(
        self, metadata
    ) -> collections.abc.AsyncIterator[dict[str, int]]:
        yield {"RaiseDefinedExecutionErrorAfterValueWasSent": 1}

        await asyncio.sleep(0)

        msg = "SiLA2_test_error_message"
        raise TestError(msg)

    async def raise_undefined_execution_error_after_value_was_sent(
        self, metadata
    ) -> collections.abc.AsyncIterator[dict[str, int]]:
        yield {"RaiseUndefinedExecutionErrorAfterValueWasSent": 1}

        await asyncio.sleep(0)

        msg = "SiLA2_test_error_message"
        raise UndefinedExecutionError(msg)

    def raise_defined_execution_error(self, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise TestError(msg)

    def raise_defined_execution_error_observably(self, command_execution: CommandExecution, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise TestError(msg)

    def raise_undefined_execution_error(self, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise UndefinedExecutionError(msg)

    def raise_undefined_execution_error_observably(self, command_execution: CommandExecution, metadata) -> None:
        msg = "SiLA2_test_error_message"
        raise UndefinedExecutionError(msg)
