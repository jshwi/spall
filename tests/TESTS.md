<!--
This file is auto-generated and any changes made to it will be overwritten
-->
# tests

## tests._test


### _class_ tests._test.TestHandleStderr()
Bases: `object`

Test varying ways of handling stderr.


#### EXPECTED( = `'stderr'`)

#### OUTPUT( = `b'stderr'`)

#### RETURNCODE( = `1`)

#### test_capture(mocksp: )
Test stderr when captured.


### Command not found error

Test `CommandNotFoundError` warning with `Subprocess`.


### Pipe

Test piping of stderr to stdout.


### Repr

Test `Subprocess`’s repr.


### Set positionals

Test setting of subprocesses with heavy use of positionals.


### Std capture

Test additional kwargs to control stdout and stderr with capture.


### Std kwargs

Test additional kwargs to control stdout and stderr to file.


### With contextlib

Test using None with `contextlib.redirect_`.


