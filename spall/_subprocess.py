"""
spall._subprocess
=================
"""
from __future__ import annotations

import functools as _functools
import os as _os
import subprocess as _sp
import sys as _sys
import typing as _t

from . import exceptions as _exceptions


class _Stream:
    def __init__(self) -> None:
        self._list: _t.List[str] = []

    def consume(self) -> _t.List[str]:
        """Consume and return accrued output.

        :return: List of captured output.
        """
        captured, self._list = self._list, []
        return captured

    def append(self, item: str) -> None:
        """Append to ``_list``.

        :param item: Output as str.
        """
        self._list.append(item)


class Subprocess:
    """Create a new ``Subprocess`` object.

    ``cmd`` is a mandatory argument used to construct the subprocess
    executable.

    Default ``file``, ``suppress``, and ``capture`` values can be set
    when instantiating the object to be overridden later when using
    ``call``, or simply set through the ``call`` method alone.

    :param cmd: Subprocess executable.
    :param positionals: List of positional arguments to set as
        attributes if not None.
    :key file: File path to write stdout and stderr to if not None.
    :key file_stdout: File path to write stdout to if not None.
    :key file_stderr: File path to write stderr to if not None.
    :key capture: Collect stdout and stderr array.
    :key capture_stdout: Collect stdout array.
    :key capture_stderr: Collect stderr array.
    :key pipe: Pipe stderr to stdout.
    :key suppress: Suppress errors and continue running.
    """

    def __init__(
        self,
        cmd: str,
        positionals: _t.Iterable[str] | None = None,
        **kwargs: bool | str | _os.PathLike,
    ) -> None:
        self._cmd = cmd
        self._kwargs = kwargs
        self._stdout = _Stream()
        self._stderr = _Stream()
        if positionals is not None:
            self._set_positionals(positionals)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ({self._cmd})>"

    def __setattr__(self, key: str, value: _t.Any) -> None:
        # pylint: disable=useless-super-delegation
        # not useless; silences `mypy` with `_t.Any` and dynamic attrs
        super().__setattr__(key, value)

    def __getattribute__(self, key: str) -> _t.Any:
        # pylint: disable=useless-super-delegation
        # not useless; silences `mypy` with `_t.Any` and dynamic attrs
        return super().__getattribute__(key)

    def _set_positionals(self, positionals: _t.Iterable[str]) -> None:
        for positional in positionals:
            setattr(
                self,
                positional.replace("-", "_"),
                _functools.partial(self.call, positional),
            )

    def _handle_stream(
        self, popen: _sp.Popen, std: str, **kwargs: bool | str | _os.PathLike
    ) -> None:
        std_pipe = getattr(popen, std)
        if std_pipe is not None:
            for line in iter(std_pipe.readline, b""):
                if kwargs.get("pipe", self._kwargs.get("pipe", False)):
                    std = "stdout"

                line = line.decode("utf-8", "ignore")
                file = kwargs.get(
                    f"{std}_file",
                    self._kwargs.get(
                        f"{std}_file",
                        kwargs.get("file", self._kwargs.get("file")),
                    ),
                )
                capture = kwargs.get(
                    f"{std}_capture",
                    self._kwargs.get(
                        f"{std}_capture",
                        kwargs.get(
                            "capture", self._kwargs.get("capture", False)
                        ),
                    ),
                )
                if file is not None:
                    with open(file, "a+", encoding="utf-8") as fout:
                        fout.write(line)

                elif capture:
                    getattr(self, f"_{std}").append(line.strip())

                else:
                    sys_std = getattr(_sys, std)
                    if sys_std is not None:
                        sys_std.write(line)

    def _open_process(
        self, *args: str, **kwargs: bool | str | _os.PathLike
    ) -> int:
        cmd = [self._cmd, *args]
        with _sp.Popen(cmd, stdout=_sp.PIPE, stderr=_sp.PIPE) as popen:
            for std in ("stdout", "stderr"):
                self._handle_stream(popen, std, **kwargs)

            return popen.wait()

    def call(self, *args: _t.Any, **kwargs: bool | str | _os.PathLike) -> int:
        """Call command.

        Open process with ``subprocess.Popen``.

        Pipe stream depending on the keyword arguments provided to
        instance constructor or overridden through this method.

        If a file path is provided it will take precedence over
        ``capture``.

        :param args: Positional str arguments.
        :key file: File path to write stdout and stderr to if not None.
        :key file_stdout: File path to write stdout to if not None.
        :key file_stderr: File path to write stderr to if not None.
        :key capture: Collect stdout and stderr array.
        :key capture_stdout: Collect stdout array.
        :key capture_stderr: Collect stderr array.
        :key pipe: Pipe stderr to stdout.
        :key suppress: Suppress errors and continue running.
        :raises CommandNotFoundError: If instantiated executable is not
            in path.
        :raises CalledProcessError: If error occurs in subprocess.
        :return: Exit status.
        """
        args = tuple(str(i) for i in args)
        try:
            returncode = self._open_process(*args, **kwargs)
        except FileNotFoundError as err:
            raise _exceptions.CommandNotFoundError(self._cmd) from err

        if returncode and not kwargs.get(
            "suppress", self._kwargs.get("suppress", False)
        ):
            raise _exceptions.CalledProcessError(
                returncode, " ".join([self._cmd, *args])
            )

        return returncode

    def stdout(self) -> _t.List[str]:
        """Consume accrued stdout by returning the lines of output.

        Assign new container to ``_stdout``.

        :return: List of captured stdout.
        """
        return self._stdout.consume()

    def stderr(self) -> _t.List[str]:
        """Consume accrued stderr by returning the lines of output.

        Assign new container to ``_stderr``.

        :return: List of captured stderr.
        """
        return self._stderr.consume()
