"""
tests.conftest
==============
"""
import typing as t

import pytest

import spall

from . import MockSubprocessType
from ._utils import Patch


@pytest.fixture(name="mocksp")
def fixture_mocksp(monkeypatch: pytest.MonkeyPatch) -> MockSubprocessType:
    """Fixture for mocking ``spall.Subprocess``.

    :param monkeypatch: Mock patch environment and attributes.
    :return: Function for using this fixture.
    """

    def _subproc(
        cmd: str,
        stdout: t.List[bytes],
        stderr: t.List[bytes],
        returncode: int,
        **kwargs: t.Any,
    ) -> spall.Subprocess:
        patch = Patch(stdout, stderr, returncode)
        monkeypatch.setattr("spall.Subprocess._sanity_check", lambda _: None)
        monkeypatch.setattr("spall._subprocess._sp.Popen", patch)
        return spall.Subprocess(cmd, **kwargs)

    return _subproc
