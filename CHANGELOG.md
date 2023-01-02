Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[Unreleased](https://github.com/jshwi/spall/compare/v0.5.0...HEAD)
------------------------------------------------------------------------
### Added
- Add py.typed

[0.5.0](https://github.com/jshwi/spall/releases/tag/v0.5.0) - 2022-05-10
------------------------------------------------------------------------
### Added
- add: Adds `pipe` keyword argument to pipe stderr to stdout
- Adds additional keyword arguments to control stdout and stderr
- Includes `CalledProcessError` in `spall.exceptions`

[0.4.0](https://github.com/jshwi/spall/releases/tag/v0.4.0) - 2022-05-09
------------------------------------------------------------------------
### Removed
- Removes `devnull` keyword argument

[0.3.0](https://github.com/jshwi/spall/releases/tag/v0.3.0) - 2022-05-07
------------------------------------------------------------------------
### Added
- Checks that `sys.stdout/sys.stderr` is not None

[0.2.0](https://github.com/jshwi/spall/releases/tag/v0.2.0) - 2022-05-06
------------------------------------------------------------------------
### Changed
- Changes stderr to behave the same way as stdout

### Removed
- Removes logger

[0.1.1](https://github.com/jshwi/spall/releases/tag/v0.1.1) - 2022-01-09
------------------------------------------------------------------------
### Fixed
- Fixes `poetry` packaging

[0.1.0](https://github.com/jshwi/spall/releases/tag/v0.1.0) - 2022-01-09
------------------------------------------------------------------------
Initial Release
