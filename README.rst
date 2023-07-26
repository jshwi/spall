spall
=====
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/spall
    :target: https://pypi.org/project/spall/
    :alt: PyPI
.. image:: https://github.com/jshwi/spall/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/jshwi/spall/actions/workflows/build.yaml
    :alt: Build
.. image:: https://github.com/jshwi/spall/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/spall/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://results.pre-commit.ci/badge/github/jshwi/spall/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/spall/master
   :alt: pre-commit.ci status
.. image:: https://codecov.io/gh/jshwi/spall/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/spall
    :alt: codecov.io
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort
.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
    :alt: docformatter
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint
.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
.. image:: https://snyk.io/test/github/jshwi/spall/badge.svg
    :target: https://snyk.io/test/github/jshwi/spall/badge.svg
    :alt: Known Vulnerabilities
.. image:: https://snyk.io/advisor/python/spall/badge.svg
    :target: https://snyk.io/advisor/python/spall
    :alt: spall

Object-oriented commandline
---------------------------


Install
-------

.. code-block:: console

    $ pip install spall

Development
-----------

.. code-block:: console

    $ pip install spall

Usage
-----

Import ``Subprocess`` from ``spall``

.. code-block:: python

    >>> from spall import Subprocess

Instantiate individual executables

.. code-block:: python

    >>> cat = Subprocess("cat")
    >>> echo = Subprocess("echo")
    >>> fails = Subprocess("false")


Default is to return returncode and print stdout and stderr to console

.. code-block:: python

    >>> returncode = echo.call("Hello, world")
    Hello, world
    >>> returncode
    0

Capture stdout with the ``capture`` keyword argument

.. code-block:: python

    >>> echo.call("Hello, world", capture=True)
    0

Stdout is consumed by calling ``stdout()`` which returns a list

.. code-block:: python

    >>> echo.stdout()
    ['Hello, world']
    >>> echo.stdout()
    []

Stdout is accrued until ``stdout()`` is called

.. code-block:: python

    >>> echo.call("Hello, world", capture=True)
    0
    >>> echo.call("Goodbye, world", capture=True)
    0
    >>> echo.stdout()
    ['Hello, world', 'Goodbye, world']
    >>> echo.stdout()
    []

Pipe stdout to file with the ``file`` keyword argument

.. code-block:: python

    >>> import os
    >>> import tempfile
    >>>
    >>> tmp = tempfile.NamedTemporaryFile(delete=False)
    >>> echo.call("Hello, world", file=tmp.name)
    0
    >>> returncode = cat.call(tmp.name)
    Hello, world
    >>> returncode
    0
    >>> os.remove(tmp.name)

    # redirect to /dev/null
    >>> echo.call("Hello, world", file=os.devnull)
    0

Failing command will raise a ``subprocess.CalledProcessError``

.. code-block:: python

    >>> import contextlib
    >>> from subprocess import CalledProcessError
    >>>
    >>> with contextlib.redirect_stderr(None):
    ...     try:
    ...         returncode = fails.call()
    ...     except CalledProcessError as err:
    ...         str(err)
    "Command 'false' returned non-zero exit status 1."
    >>> returncode
    0

This, however, will not

.. code-block:: python

    >>> with contextlib.redirect_stderr(None):
    ...     fails.call(suppress=True)
    1

All the keyword arguments above can be set as the default for the instantiated object

.. code-block:: python

    >>> echo = Subprocess("echo", capture=True)
    >>> echo.call("Hello, world")
    0
    >>> echo.stdout()
    ['Hello, world']

Which can then be overridden

.. code-block:: python

    >>> returncode = echo.call("Hello, world", capture=False)
    Hello, world
    >>> returncode
    0
    >>> echo.stdout()
    []
