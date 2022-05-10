"""
spall.exceptions
================

Exceptions for use within the module.

All exceptions made public for if they need to be reraised or excepted.
"""
# noinspection PyUnresolvedReferences
from subprocess import CalledProcessError  # pylint: disable=unused-import


class CommandNotFoundError(OSError):
    """Raise when subprocess called is not on system."""

    def __init__(self, cmd: str) -> None:
        super().__init__(f"{cmd}: command not found...")
