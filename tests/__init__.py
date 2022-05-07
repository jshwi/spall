"""
tests
=====

Test package for ``spall``.
"""
import typing as t

import spall

MockSubprocessType = t.Callable[..., spall.Subprocess]
