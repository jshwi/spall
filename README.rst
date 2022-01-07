spall
======
.. image:: https://github.com/jshwi/spall/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/spall/actions/workflows/ci.yml
    :alt: ci
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/pypi/v/spall
    :target: https://img.shields.io/pypi/v/spall
    :alt: pypi
.. image:: https://codecov.io/gh/jshwi/spall/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/spall
    :alt: codecov.io
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: mit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

Object oriented commandline


Install
-------

``pip install spall``

Development

``poetry install``

Example Usage
-------------

.. code-block:: python

    from spall import Subprocess

    cmd = str(...)  # any command here e.g. git

    proc = Subprocess(cmd)  # instantiate executable as object

    passing = ...  # insert passing command here

    returncode = proc.call(passing)  # this will print to console
    print(returncode)  # -> 0

    proc.call(passing, capture=True)  # this will record the output
    proc.stdout()  # -> [...]

    # stdout is consumed
    proc.stdout()  # -> []

    # this will record the output twice
    proc.call(passing, capture=True)
    proc.call(passing, capture=True)
    proc.stdout()  # -> [..., ...]
    proc.stdout()  # -> []

     # this will redirect stdout to /dev/null
    proc.call(passing, devnull=True)

    # this will pipe stdout to file
    proc.call(file="~/example.txt")

    failing = ...  # insert failing command here

    # will raise a ``subprocess.CalledProcessError``
    returncode = proc.call(failing)
    print(returncode)  # -> > 0

    # this, however, will not
    returncode = proc.call(failing, suppress=True)
    print(returncode)  # -> > 0

    # all the keyword arguments above can be set as the default for the
    # instantiated object
    proc = Subprocess(cmd, capture=True)

    proc.call(passing)
    proc.stdout()  # -> [...]

    # but they will be overridden through the method
    proc.call(passing, capture=False)
    proc.stdout()  # -> []

