"""
test._utils
===========
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

import typing as t

CMD = "cmd"


class Output:
    """Mock stdout and stderr iterable.

    :param iterable: Mock output as bytes.
    """

    def __init__(self, iterable: t.List[bytes]) -> None:
        self._iterable = iter(iterable)

    def readline(self) -> bytes:
        """Mock output's readline method to be passed to iter.

        :return: Line of output as bytes.
        """
        return next(self._iterable)


class Patch:
    """Mock ``spall.Subprocess`` object.

    :param stdout: Mock list of stdout as bytes.
    :param stderr: Mock list of stderr as bytes:
    :param returncode: Mock returncode.
    """

    def __init__(
        self, stdout: t.List[bytes], stderr: t.List[bytes], returncode: int
    ) -> None:
        self.stdout = Output(stdout)
        self.stderr = Output(stderr)
        self._returncode = returncode

    def __enter__(self) -> Patch:
        return self

    def __exit__(self, exc_type: t.Any, exc_val: t.Any, exc_tb: t.Any) -> None:
        """Nothing to do.."""

    def __call__(self, *_: t.Any, **__: t.Any) -> Patch:
        return self

    def wait(self) -> int:
        """Mock ``subprocess.Popen.wait()``

        :return: Mocked returncode.
        """
        return self._returncode
