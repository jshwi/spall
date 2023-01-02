"""
spall.exceptions
================

Exceptions for use within the module.

All exceptions made public for if they need to be reraised or excepted.
"""
# noinspection PyUnresolvedReferences
from subprocess import CalledProcessError  # noqa pylint: disable=unused-import


class CommandNotFoundError(OSError):
    """Raise when subprocess called is not on system.

    :param cmd: Name of command that was not found.
    """

    def __init__(self, cmd: str) -> None:
        super().__init__(f"{cmd}: command not found...")
