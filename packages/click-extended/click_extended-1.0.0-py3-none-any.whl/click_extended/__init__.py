"""Initialization file for the 'click_extended' module."""

from click_extended.core.decorators.argument import argument
from click_extended.core.decorators.command import command
from click_extended.core.decorators.env import env
from click_extended.core.decorators.group import group
from click_extended.core.decorators.option import option
from click_extended.core.decorators.prompt import prompt
from click_extended.core.decorators.selection import selection
from click_extended.core.decorators.tag import tag

__all__ = [
    "argument",
    "command",
    "env",
    "group",
    "option",
    "prompt",
    "selection",
    "tag",
]
