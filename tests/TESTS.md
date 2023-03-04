<!--
This file is auto-generated and any changes made to it will be overwritten
-->
# tests

## tests._test


### _class_ tests._test.TestHandleStderr()
Bases: `object`

Test varying ways of handling stderr.


#### EXPECTED(_ = 'stderr_ )

#### OUTPUT(_ = b'stderr_ )

#### RETURNCODE(_ = _ )

#### test_capture(mocksp: Callable[[...], [spall._subprocess.Subprocess](spall.md#spall.Subprocess)])
Test stderr when captured.


### Command not found error

Test `CommandNotFoundError` warning with `Subprocess`.


### Pipe(capsys:  pytest.capture.capturefixture, mocksp: callable[[...], [spall. subprocess.subprocess]

Test piping of stderr to stdout.


### Repr

Test `Subprocess`’s repr.


### Set positionals

Test setting of subprocesses with heavy use of positionals.


### Std capture(capsys:  pytest.capture.capturefixture, mocksp: callable[[...], [spall. subprocess.subprocess]

Test additional kwargs to control stdout and stderr with capture.


### Std kwargs(tmp path: pathlib.path, capsys:  pytest.capture.capturefixture, mocksp: callable[[...], [spall. subprocess.subprocess]

Test additional kwargs to control stdout and stderr to file.


### With contextlib

Test using None with `contextlib.redirect_`.


