"""Test the 4-phase lifecycle system."""

import click
from click.testing import CliRunner
from conftest import SimpleChild, ValidatingChild, assert_error, assert_success

from click_extended.core.decorators.command import command
from click_extended.core.decorators.option import option
from click_extended.core.nodes.child_node import ChildNode
from click_extended.core.other.context import Context


class TestPhase1Collection:
    """Test Phase 1: Decorator application and node queueing."""

    def test_decorators_queue_nodes(self, cli_runner: CliRunner) -> None:
        """Test that decorators queue nodes without immediate registration."""

        @command()
        @option("--name", type=str, default="World")
        def hello(name: str) -> None:
            click.echo(f"Hello {name}")

        result = cli_runner.invoke(hello, ["--name", "Test"])  # type: ignore
        assert_success(result, "Hello Test")

    def test_child_decorator_queues_child(self, cli_runner: CliRunner) -> None:
        """Test that child decorators queue child nodes."""

        @command()
        @option("--name", type=str, default="test")
        @SimpleChild.as_decorator()
        def cmd(name: str) -> None:
            click.echo(f"Name: {name}")

        result = cli_runner.invoke(cmd, ["--name", "hello"])  # type: ignore
        assert_success(result, "Name: HELLO")


class TestPhase2ContextInit:
    """Test Phase 2: Context initialization with metadata."""

    def test_context_metadata_injected(self, cli_runner: CliRunner) -> None:
        """Test that Click context receives click_extended metadata."""
        context_meta: dict[str, object] = {}

        @command()
        @option("--value", type=str, default="test")
        def cmd(value: str) -> None:
            ctx = click.get_current_context()
            context_meta.update(ctx.meta.get("click_extended", {}))
            click.echo("ok")

        result = cli_runner.invoke(cmd)  # type: ignore
        assert_success(result, "ok")
        assert "current_scope" in context_meta
        assert "root_node" in context_meta


class TestPhase3Validation:
    """Test Phase 3: Tree building and validation."""

    def test_validates_type_mismatch(self, cli_runner: CliRunner) -> None:
        """Test that type mismatches are caught during runtime."""

        class IntChild(ChildNode):
            def handle_int(self, value: int, context: Context) -> int:
                return value * 2

        @command()
        @option("--value", type=str)
        @IntChild.as_decorator()
        def cmd(value: int) -> None:
            click.echo(f"Value: {value}")

        result = cli_runner.invoke(cmd, ["--value", "test"])  # type: ignore
        assert_error(result)


class TestPhase4Runtime:
    """Test Phase 4: Processing with scope tracking and exception wrapping."""

    def test_processes_value_through_child(self, cli_runner: CliRunner) -> None:
        """Test that values are processed through child nodes."""

        @command()
        @option("--name", type=str, default="test")
        @SimpleChild.as_decorator()
        def cmd(name: str) -> None:
            click.echo(f"Name: {name}")

        result = cli_runner.invoke(cmd, ["--name", "hello"])  # type: ignore
        assert_success(result, "Name: HELLO")

    def test_wraps_user_exceptions(self, cli_runner: CliRunner) -> None:
        """Test that user exceptions are wrapped with context."""

        @command()
        @option("--value", type=int, default=5)
        @ValidatingChild.as_decorator()
        def cmd(value: int) -> None:
            click.echo(f"Value: {value}")

        result = cli_runner.invoke(cmd, ["--value", "10"])  # type: ignore
        assert_success(result, "Value: 10")

        result = cli_runner.invoke(cmd, ["--value", "-5"])  # type: ignore
        assert_error(result)

        error_text = (
            result.output.lower()
            if result.output
            else str(result.exception).lower()
        )
        assert "must be positive" in error_text

    def test_scope_tracking_during_processing(
        self, cli_runner: CliRunner
    ) -> None:
        """Test that scope is tracked as execution moves through nodes."""

        scopes: list[str] = []

        class TrackingChild(SimpleChild):
            def handle_str(self, value: str, context: Context) -> str:
                ctx = click.get_current_context()
                scope = ctx.meta["click_extended"]["current_scope"]
                scopes.append(scope)
                return super().handle_str(value, context)

        @command()
        @option("--name", type=str, default="test")
        @TrackingChild.as_decorator()
        def cmd(name: str) -> None:
            click.echo(f"Name: {name}")

        result = cli_runner.invoke(cmd, ["--name", "hello"])  # type: ignore
        assert_success(result, "Name: HELLO")
        assert "child" in scopes


class TestFullLifecycle:
    """Test complete lifecycle from decoration to execution."""

    def test_simple_command_lifecycle(self, cli_runner: CliRunner) -> None:
        """Test a simple command through all phases."""

        @command()
        @option("--count", type=int, default=1)
        def repeat(count: int) -> None:
            for i in range(count):
                click.echo(f"Line {i + 1}")

        result = cli_runner.invoke(repeat, ["--count", "3"])  # type: ignore
        assert_success(result)
        assert "Line 1" in result.output
        assert "Line 2" in result.output
        assert "Line 3" in result.output

    def test_command_with_processing(self, cli_runner: CliRunner) -> None:
        """Test command with value processing through child node."""

        @command()
        @option("--text", type=str, default="hello")
        @SimpleChild.as_decorator()
        def echo_upper(text: str) -> None:
            click.echo(text)

        result = cli_runner.invoke(echo_upper, ["--text", "world"])  # type: ignore
        assert_success(result, "WORLD")

    def test_command_with_validation(self, cli_runner: CliRunner) -> None:
        """Test command with validation that can fail."""

        @command()
        @option("--number", type=int, default=5)
        @ValidatingChild.as_decorator()
        def check_positive(number: int) -> None:
            click.echo(f"Valid: {number}")

        result = cli_runner.invoke(check_positive, ["--number", "10"])  # type: ignore
        assert_success(result, "Valid: 10")

        result = cli_runner.invoke(check_positive, ["--number", "0"])  # type: ignore
        assert_error(result)
