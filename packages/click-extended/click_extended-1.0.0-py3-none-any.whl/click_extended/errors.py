"""Error module for the `click_extended` library."""

import sys
from typing import Any

import click
from click.utils import echo

from click_extended.utils.humanize import humanize_iterable


class ClickExtendedError(Exception):
    """Base exception for all click-extended errors."""

    def __init__(self, message: str, tip: str | None = None) -> None:
        """
        Initialize a ClickExtendedError.

        Args:
            message (str):
                The error message describing what went wrong.
            tip (str):
                Optional helpful guidance for resolving the error.
        """
        self.message = message
        self.tip = tip
        super().__init__(message)

    def show(self, file: Any = None) -> None:
        """
        Display the error message.

        Subclasses should override this to provide custom formatting.

        Args:
            file (Any, optional):
                The file to write to (defaults to sys.stderr).
        """
        if file is None:
            file = sys.stderr

        echo(f"Error: {self.message}", file=file)

        if self.tip:
            echo(f"\nTip: {self.tip}", file=file)


class ContextAwareError(ClickExtendedError):
    """
    Base exception for errors that occur within Click context.

    These errors have access to the full node hierarchy and are formatted
    with Click-style usage information and node context.

    It can only be raised during `phase 3` or `phase 4`.
    """

    context: click.Context | None

    def __init__(self, message: str, tip: str | None = None) -> None:
        """
        Initialize a new `ContextAwareError` instance.

        Args:
            message (str):
                The error message describing what went wrong.
            tip (str):
                Optional helpful guidance for resolving the error.
        """
        super().__init__(message, tip)
        try:
            self.context = click.get_current_context()
            self._node_name = self._resolve_node_name()
        except RuntimeError:
            self.context = None
            self._node_name = "unknown"

    def _resolve_node_name(self) -> str:
        """
        Get the most specific node name from context.

        If inside a child node, that will be used, otherwise it checks if a
        parent is defined, and if not that, the root node will be used.

        Returns:
            str:
                The name of the most specific node in the current scope.
        """
        if self.context is None:
            return "unknown"

        meta = self.context.meta.get("click_extended", {})

        if meta.get("child_node"):
            return str(meta["child_node"].name)
        if meta.get("parent_node"):
            return str(meta["parent_node"].name)
        if meta.get("root_node"):
            return str(meta["root_node"].name)

        return "unknown"

    def show(self, file: Any = None) -> None:
        """
        Display the error with Click-style formatting.

        Format:
            Usage: cli [OPTIONS] COMMAND [ARGS]...
            Try 'cli --help' for help.

            Error (node_name): message
            Tip: helpful guidance

        Args:
            file (Any, optional):
                The file to write to (defaults to `sys.stderr`).
        """
        if file is None:
            file = sys.stderr

        if self.context is None:
            super().show(file)
            return

        echo(self.context.get_usage(), file=file, color=self.context.color)

        if self.context.command.get_help_option(self.context) is not None:
            hint = f"Try '{self.context.command_path} --help' for help."
            echo(hint, file=file, color=self.context.color)

        echo("", file=file)

        exception_name = self.__class__.__name__
        echo(
            f"{exception_name} ({self._node_name}): {self.message}",
            file=file,
            color=self.context.color,
        )

        if self.tip:
            echo(f"Tip: {self.tip}", file=file, color=self.context.color)


class MissingValueError(ContextAwareError):
    """
    Exception raised when a value is missing.

    This exception is context-aware and can only be raised during `phase 3` or
    `phase 4`.
    """

    def __init__(self) -> None:
        """Initialize a new `MissingValueError` instance."""
        super().__init__(
            message="Value not provided.", tip=self._generate_tip()
        )

    def _generate_tip(self) -> str:
        """Generate a context-aware tip based on the parent node type."""
        try:
            ctx = click.get_current_context()
            meta = ctx.meta.get("click_extended", {})

            parent = meta.get("parent_node")

            if parent is not None:
                return self._tip_for_parent(parent)
        except (RuntimeError, AttributeError):
            pass

        return (
            "Provide a value or set the default parameter to make it optional."
        )

    # pylint: disable=too-many-return-statements
    def _tip_for_parent(self, parent: Any) -> str:
        """Generate tip based on parent type."""
        parent_type = parent.__class__.__name__
        parent_name = parent.name

        if parent_type == "Option":
            return "".join(
                f"Use --{parent_name.replace('_', '-')} to specify a value, "
                "or set the default parameter to make it optional."
            )
        if parent_type == "Argument":
            return "".join(
                f"Provide the {parent_name} argument, or set the default "
                "parameter to make it optional."
            )
        if parent_type == "Env":
            env_var = getattr(parent, "env_name", parent_name.upper())
            return "".join(
                f"Set the {env_var} environment variable, or set the "
                f"default parameter to make it optional."
            )
        return "".join(
            "Provide a value or set the default parameter to "
            "make it optional."
        )


class NoRootError(ContextAwareError):
    """Exception raised when no root node has been defined."""

    def __init__(self, tip: str | None = None) -> None:
        """
        Initialize a new `NoRootError` instance.

        Args:
            tip (str):
                Optional helpful guidance (defaults to standard tip).
        """
        super().__init__(
            "No root node has been defined",
            tip=tip or "Use @click_extended.root() decorator first",
        )


class NoParentError(ContextAwareError):
    """Exception raised when a child node has no parent to attach to."""

    def __init__(self, child_name: str, tip: str | None = None) -> None:
        """
        Initialize a new `NoParentError` instance.

        Args:
            child_name (str):
                The name of the child node.
            tip (str):
                Optional helpful guidance (defaults to standard tip).
        """
        tip_msg = (
            tip
            or "Ensure a parent node (option/argument) is defined "
            "before child nodes"
        )
        super().__init__(
            f"Cannot register child node '{child_name}' "
            f"as no parent is defined",
            tip=tip_msg,
        )


class RootExistsError(ContextAwareError):
    """Exception raised when attempting to define multiple root nodes."""

    def __init__(self, tip: str | None = None) -> None:
        """
        Initialize a new `RootExistsError` instance.

        Args:
            tip (str, optional):
                Optional helpful guidance (defaults to standard tip).
        """
        super().__init__(
            "A root node has already been defined",
            tip=tip or "Only one @root() decorator is allowed per command",
        )


class ParentExistsError(ContextAwareError):
    """Exception raised when attempting to register duplicate parent names."""

    def __init__(self, name: str, tip: str | None = None) -> None:
        """
        Initialize a new `ParentExistsError` instance.

        Args:
            name (str):
                The name of the duplicate parent node.
            tip (str | None, optional):
                Optional helpful guidance (defaults to standard tip).
        """
        super().__init__(
            f"Parent node '{name}' already exists",
            tip=tip or "Parent node names must be unique within a command",
        )


class TypeMismatchError(ContextAwareError):
    """
    Exception raised when a child's process() signature is incompatible
    with the parent's type.
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        child_name: str,
        parent_name: str,
        parent_type: str,
        supported_types: list[str],
        tip: str | None = None,
    ) -> None:
        """
        Initialize a new `TypeMismatchError` instance.

        Args:
            child_name (str):
                The name of the child node.
            parent_name (str):
                The name of the parent node.
            parent_type (str):
                The type of the parent (as string).
            supported_types (list[str]):
                List of supported type names.
            tip (str | None, optional):
                Optional helpful guidance (defaults to supported types).
        """
        message = (
            f"Child '{child_name}' does not support parent '{parent_name}' "
            f"with type '{parent_type}'"
        )

        if tip is None:
            types_str = ", ".join(f"<{t}>" for t in supported_types)
            tip = f"Supported types: {types_str}"

        super().__init__(message, tip=tip)


class NameExistsError(ContextAwareError):
    """Exception raised when a name collision is detected."""

    def __init__(self, name: str, tip: str | None = None) -> None:
        """
        Initialize a new `NameExistsError` instance.

        Args:
            name (str):
                The conflicting name.
            tip (str | None, optional):
                Optional helpful guidance (defaults to standard tip).
        """
        super().__init__(
            f"The name '{name}' is already used",
            tip=tip or "All names must be unique within a command",
        )


class UnhandledTypeError(ContextAwareError):
    """
    Exception raised when a child node doesn't implement a handler
    for the value type.
    """

    def __init__(
        self,
        child_name: str,
        value_type: str,
        implemented_handlers: list[str],
        tip: str | None = None,
    ) -> None:
        """
        Initialize a new `UnhandledTypeError` instance.

        Args:
            child_name (str):
                The name of the child node.
            value_type (str):
                The type of value that couldn't be handled.
            implemented_handlers (list[str]):
                List of handler names that are implemented.
            tip (str, optional):
                Optional helpful guidance (defaults to list of handlers).
        """
        message = "Child '{}' does not handle values of type '{}'."
        message = message.format(child_name, value_type)

        if tip is None:
            if implemented_handlers:
                tip = (
                    f"Missing handler for '{value_type}', only "
                    + humanize_iterable(
                        implemented_handlers,
                        wrap="'",
                        suffix_singular=" is supported.",
                        suffix_plural=" are supported.",
                    )
                )
            else:
                tip = "".join(
                    "No handlers are implemented. Override handle_all() "
                    "or a specific handler method."
                )

        super().__init__(message, tip=tip)


class ProcessError(ContextAwareError):
    """
    Exception raised when user code in `child.process()` raises an exception.

    This error wraps standard Python exceptions (ValueError, TypeError, etc.)
    raised by user code and adds node context for better error messages.
    """

    def __init__(self, message: str, tip: str | None = None) -> None:
        """
        Initialize a new `ProcessError` instance.

        Args:
            message (str):
                The error message from the wrapped exception.
            tip (str | None, optional):
                Optional helpful guidance for resolving the error.
        """
        super().__init__(message, tip=tip)


class InvalidHandlerError(ContextAwareError):
    """Exception raised when a handler returns an invalid value."""

    def __init__(self, message: str, tip: str | None = None) -> None:
        """
        Initialize an new `InvalidHandlerError` instance.

        Args:
            message (str):
                Description of the invalid handler behavior.
            tip (str | None, optional):
                Optional helpful guidance for correcting the handler.
        """
        super().__init__(message, tip=tip)


class InternalError(ContextAwareError):
    """
    Exception raised for unexpected errors in framework code.

    This indicates a bug in `click-extended` or an unreachable code path.
    """

    def __init__(self, message: str, tip: str | None = None) -> None:
        """
        Initialize a new `InternalError` instance.

        Args:
            message (str):
                Description of the internal error.
            tip (str | None, optional):
                Optional helpful guidance (defaults to bug report message).
        """
        super().__init__(
            message,
            tip=tip
            or "This is likely a bug in click-extended. Please report it.",
        )
