"""Register tests as a package."""
import typing as t

import spall

MockSubprocessType = t.Callable[..., spall.Subprocess]
