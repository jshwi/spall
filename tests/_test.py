"""
tests._test
===========
"""
# pylint: disable=too-few-public-methods,too-many-arguments
import contextlib
import os
import typing as t
from datetime import datetime
from pathlib import Path
from subprocess import CalledProcessError

import pytest

import spall as sp

from . import CAPTURE, CMD, EMPTY_BYTE, STDERR, STDOUT, MockSubprocessType


def test_command_not_found_error() -> None:
    """Test ``CommandNotFoundError`` warning with ``Subprocess``."""
    unique = datetime.now().strftime("%d%m%YT%H%M%S")
    proc = sp.Subprocess(unique)
    with pytest.raises(sp.exceptions.CommandNotFoundError) as err:
        proc.call()

    assert str(err.value) == f"{unique}: command not found..."


def test_set_positionals() -> None:
    """Test setting of subprocesses with heavy use of positionals."""
    git = sp.Subprocess("git", positionals=["add", "init"])
    assert hasattr(git, "add")
    assert hasattr(git, "init")


def test_repr(capsys: pytest.CaptureFixture) -> None:
    """Test ``Subprocess``'s repr.

    :param capsys: Capture sys output.
    """
    proc = sp.Subprocess(CMD)
    print(proc)
    output = capsys.readouterr()
    assert output.out.strip() == f"<Subprocess ({CMD})>"


def test_with_contextlib(capsys: pytest.CaptureFixture) -> None:
    """Test using None with ``contextlib.redirect_``.

    :param capsys: Capture sys output.
    """
    subprocess = sp.Subprocess("echo")
    with contextlib.redirect_stdout(None):
        subprocess.call()

    assert capsys.readouterr()[0] == ""


class TestHandleStdout:
    """Test varying ways of handling stdout."""

    OUTPUT = STDOUT.encode()
    EXPECTED = STDOUT
    RETURNCODE = 0

    def test_default(
        self, capsys: pytest.CaptureFixture, mocksp: MockSubprocessType
    ) -> None:
        """Test stdout to console.

        :param capsys: Capture sys output.
        :param mocksp: Mock and return ``spall.Subprocess`` instance.
        """
        subprocess = mocksp(
            CMD, [self.OUTPUT, EMPTY_BYTE], [EMPTY_BYTE], self.RETURNCODE
        )
        subprocess.call()
        assert capsys.readouterr().out == self.EXPECTED

    def test_file(self, tmp_path: Path, mocksp: MockSubprocessType) -> None:
        """Test stdout when piped to file.

        :param tmp_path: Create and return temporary directory.
        :param mocksp: Mock and return ``spall.Subprocess`` instance.
        """
        file = tmp_path / "piped.txt"
        subprocess = mocksp(
            CMD,
            [self.OUTPUT, EMPTY_BYTE],
            [EMPTY_BYTE],
            self.RETURNCODE,
            file=str(file),
        )
        subprocess.call()
        assert file.read_text(encoding="utf-8") == self.EXPECTED

    def test_capture(self, mocksp: MockSubprocessType) -> None:
        """Test stdout when captured.

        :param mocksp: Mock and return ``spall.Subprocess`` instance.
        """
        subprocess = mocksp(
            CMD,
            [self.OUTPUT, EMPTY_BYTE],
            [EMPTY_BYTE],
            self.RETURNCODE,
            capture=True,
        )
        subprocess.call()
        assert subprocess.stdout() == [self.EXPECTED]

    def test_devnull(
        self, capsys: pytest.CaptureFixture, mocksp: MockSubprocessType
    ) -> None:
        """Test stdout when sent to /dev/null.

        :param capsys: Capture sys output.
        :param mocksp: Mock and return ``spall.Subprocess`` instance.
        """
        subprocess = mocksp(
            CMD,
            [self.OUTPUT, EMPTY_BYTE],
            [EMPTY_BYTE],
            self.RETURNCODE,
            file=os.devnull,
        )
        subprocess.call()
        assert not subprocess.stdout()
        assert capsys.readouterr().out == ""


class TestHandleStderr:
    """Test varying ways of handling stderr."""

    OUTPUT = STDERR.encode()
    EXPECTED = STDERR
    RETURNCODE = 1

    def test_default(self, mocksp: MockSubprocessType) -> None:
        """Test stderr to console.

        :param mocksp: Mock and return ``spall.Subprocess`` instance.
        """
        subprocess = mocksp(
            CMD, [EMPTY_BYTE], [self.OUTPUT, EMPTY_BYTE], self.RETURNCODE
        )
        with pytest.raises(CalledProcessError) as err:
            subprocess.call(file=os.devnull)

        assert str(
            err.value
        ) == "Command '{}' returned non-zero exit status {}.".format(
            CMD, self.RETURNCODE
        )

    def test_default_suppress(
        self, capsys: pytest.CaptureFixture, mocksp: MockSubprocessType
    ) -> None:
        """Test stderr when suppress is active.

        :param capsys: Capture sys output.
        :param mocksp: Mock and return ``spall.Subprocess`` instance.
        """
        subprocess = mocksp(
            CMD,
            [EMPTY_BYTE],
            [self.OUTPUT, EMPTY_BYTE],
            self.RETURNCODE,
            suppress=True,
        )
        subprocess.call()
        assert self.EXPECTED in capsys.readouterr()[1]

    def test_capture(self, mocksp: MockSubprocessType) -> None:
        """Test stderr when captured.

        :param mocksp: Mock and return ``spall.Subprocess`` instance.
        """
        subprocess = mocksp(
            CMD,
            [EMPTY_BYTE],
            [self.OUTPUT, EMPTY_BYTE],
            self.RETURNCODE,
            capture=True,
        )
        with pytest.raises(CalledProcessError):
            subprocess.call()

        assert subprocess.stderr() == [self.EXPECTED]


@pytest.mark.parametrize(
    "kwargs,sys_stdout,sys_stderr,stdout_capture,stderr_capture",
    [
        ({CAPTURE: False, "stdout_capture": True}, "", STDERR, [STDOUT], []),
        ({CAPTURE: True, "stdout_capture": True}, "", "", [STDOUT], [STDERR]),
        ({CAPTURE: False, "stderr_capture": True}, STDOUT, "", [], [STDERR]),
        ({CAPTURE: True, "stderr_capture": True}, "", "", [STDOUT], [STDERR]),
    ],
    ids=[
        "stdout-capture",
        "stdout-capture,capture",
        "stderr-capture",
        "stderr-capture,capture",
    ],
)
def test_std_capture(
    capsys: pytest.CaptureFixture,
    mocksp: MockSubprocessType,
    kwargs: t.Dict[str, bool],
    sys_stdout: str,
    sys_stderr: str,
    stdout_capture: t.List[str],
    stderr_capture: t.List[str],
) -> None:
    """Test additional kwargs to control stdout and stderr with capture.

    :param capsys: Capture sys output.
    :param mocksp: Mock and return ``spall.Subprocess`` instance.
    :param kwargs: Kwargs to pass to ``spall.Subprocess.call``.
    :param sys_stdout: Expected stdout to console.
    :param sys_stderr: Expected stderr to console.
    :param stdout_capture: Expected captured stdout.
    :param stderr_capture: Expected captured stderr:
    """
    stdout = STDOUT.encode()
    stderr = STDERR.encode()
    subprocess = mocksp(CMD, [stdout, EMPTY_BYTE], [stderr, EMPTY_BYTE], 0)
    subprocess.call(**kwargs)
    output = capsys.readouterr()
    assert output.out == sys_stdout
    assert output.err == sys_stderr
    assert subprocess.stdout() == stdout_capture
    assert subprocess.stderr() == stderr_capture


@pytest.mark.parametrize(
    "key,sys_stdout,sys_stderr,contents",
    [("stdout_file", "", STDERR, STDOUT), ("stderr_file", STDOUT, "", STDERR)],
    ids=[STDOUT, STDERR],
)
def test_std_kwargs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    mocksp: MockSubprocessType,
    key: str,
    sys_stdout: str,
    sys_stderr: str,
    contents: str,
) -> None:
    """Test additional kwargs to control stdout and stderr to file.

    :param tmp_path: Create and return temporary directory.
    :param capsys: Capture sys output.
    :param mocksp: Mock and return ``spall.Subprocess`` instance.
    :param key: Kwarg keyword.
    :param sys_stdout: Expected stdout to console.
    :param sys_stderr: Expected stderr to console.
    :param contents: Expected file contents.
    """
    stdout = STDOUT.encode()
    stderr = STDERR.encode()

    subprocess = mocksp(CMD, [stdout, EMPTY_BYTE], [stderr, EMPTY_BYTE], 0)
    file_1 = tmp_path / "file_1.txt"
    subprocess.call(**{key: file_1})
    output = capsys.readouterr()
    assert output.out == sys_stdout
    assert output.err == sys_stderr
    assert file_1.read_text() == contents

    subprocess = mocksp(CMD, [stdout, EMPTY_BYTE], [stderr, EMPTY_BYTE], 0)
    file_2 = tmp_path / "file_2.txt"
    subprocess.call(**{"file": file_2, key: file_2})
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err == ""
    assert file_2.read_text() == f"{STDOUT}{STDERR}"


def test_pipe(
    capsys: pytest.CaptureFixture, mocksp: MockSubprocessType
) -> None:
    """Test piping of stderr to stdout.

    :param capsys: Capture sys output.
    :param mocksp: Mock and return ``spall.Subprocess`` instance.
    """
    stdout = STDOUT.encode()
    stderr = STDERR.encode()
    subprocess = mocksp(CMD, [stdout, EMPTY_BYTE], [stderr, EMPTY_BYTE], 0)
    subprocess.call(pipe=True)
    output = capsys.readouterr()
    assert output.out == f"{STDOUT}{STDERR}"
    assert output.err == ""
