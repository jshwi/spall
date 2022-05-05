"""
tests._test
===========
"""
# pylint: disable=too-few-public-methods
import typing as t
from datetime import datetime
from pathlib import Path
from subprocess import CalledProcessError

import pytest

import spall as sp

from ._utils import CMD, Patch


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


class TestHandleStdout:
    """Test varying ways of handling stdout."""

    OUTPUT = b"stdout"
    EXPECTED = OUTPUT.decode()
    RETURNCODE = 0

    def _subproc(
        self, monkeypatch: pytest.MonkeyPatch, **kwargs: t.Any
    ) -> sp.Subprocess:
        patch = Patch([self.OUTPUT, b""], [b""], self.RETURNCODE)
        monkeypatch.setattr("spall.Subprocess._sanity_check", lambda _: None)
        monkeypatch.setattr("spall._subprocess._sp.Popen", patch)
        return sp.Subprocess(CMD, **kwargs)

    def test_default(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
    ) -> None:
        """Test stdout to console.

        :param monkeypatch: Mock patch environment and attributes.
        :param capsys: Capture sys output.
        """
        self._subproc(monkeypatch).call()
        assert capsys.readouterr().out == self.EXPECTED

    def test_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test stdout when piped to file.

        :param tmp_path: Create and return temporary directory.
        :param monkeypatch: Mock patch environment and attributes.
        """
        file = tmp_path / "piped.txt"
        self._subproc(monkeypatch, file=str(file)).call()
        assert file.read_text(encoding="utf-8") == self.EXPECTED

    def test_capture(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test stdout when captured.

        :param monkeypatch: Mock patch environment and attributes.
        """
        subproc = self._subproc(monkeypatch, capture=True)
        subproc.call()
        assert subproc.stdout() == [self.EXPECTED]

    def test_devnull(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
    ) -> None:
        """Test stdout when sent to /dev/null.

        :param monkeypatch: Mock patch environment and attributes.
        :param capsys: Capture sys output.
        """
        subproc = self._subproc(monkeypatch, devnull=True)
        subproc.call()
        assert not subproc.stdout()
        assert capsys.readouterr().out == ""


class TestHandleStderr:
    """Test varying ways of handling stderr."""

    OUTPUT = b"stderr"
    EXPECTED = OUTPUT.decode()
    RETURNCODE = 1

    def _subproc(
        self, monkeypatch: pytest.MonkeyPatch, **kwargs: t.Any
    ) -> sp.Subprocess:
        patch = Patch([b""], [self.OUTPUT, b""], self.RETURNCODE)
        monkeypatch.setattr("spall.Subprocess._sanity_check", lambda _: None)
        monkeypatch.setattr("spall._subprocess._sp.Popen", patch)
        return sp.Subprocess(CMD, **kwargs)

    def test_default(
        self, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test stderr to console.

        :param monkeypatch: Mock patch environment and attributes.
        :param caplog: Capture log output.
        """
        with pytest.raises(CalledProcessError) as err:
            self._subproc(monkeypatch).call()

        assert str(
            err.value
        ) == "Command '{}' returned non-zero exit status {}.".format(
            CMD, self.RETURNCODE
        )
        assert self.EXPECTED in caplog.text

    def test_default_suppress(
        self, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test stderr when suppress is active.

        :param monkeypatch: Mock patch environment and attributes.
        :param caplog: Capture log output.
        """
        self._subproc(monkeypatch, suppress=True).call()
        assert self.EXPECTED in caplog.text
        assert (
            f"returned non-zero exit status {self.RETURNCODE}" in caplog.text
        )
