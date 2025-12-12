# Changelog

## [v1.3.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v1.3.0) - 2025-12-05

### Added

- Added slugified keys support in Dictionary ([#55](https://github.com/XaviArnaus/pyxavi/pull/55)).
- Added a pull request template ([#55](https://github.com/XaviArnaus/pyxavi/pull/55)).

### Fixed

- Fixed `set()` not creating defined missing keys ([#55](https://github.com/XaviArnaus/pyxavi/pull/55))

## [v1.2.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v1.2.0) - 2025-11-13

### Changed

- Added color support for Logger into stdout ([#54](https://github.com/XaviArnaus/pyxavi/pull/54)). Missing Unit Tests for it.


## [v1.1.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v1.1.0) - 2025-10-30

### Added

- New `Stopwatch` and `Text` classes ([#52](https://github.com/XaviArnaus/pyxavi/pull/52))

### Changed

- Added multiprocess support for Logger into file and stdout ([#53](https://github.com/XaviArnaus/pyxavi/pull/53))
- Update some tooling version

## [v1.0.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v1.0.0) - 2025-06-16

### Added

- Ability to import directly from the `pyxavi` package without specifying the file ([#51](https://github.com/XaviArnaus/pyxavi/pull/51))

### Changed

- ⚠️ Breaking Change: Abstracting ActivityPub classes to the `pyxavi-activitypub` package ([#51](https://github.com/XaviArnaus/pyxavi/pull/51))

### Fixed

- Solved a DeprecationWarning from BeautifulSoap4 ([#51](https://github.com/XaviArnaus/pyxavi/pull/51))

## [v0.8.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.8.0) - 2024-02-19

### Added

- New `get_parent_path` and `get_last_key` methods in `Dictionary` module ([#33](https://github.com/XaviArnaus/pyxavi/pull/33))
- New `MastodonHelper` class and the related `MastodonConnectionParams` and `StatusPost` objects, to post to Mastodon APIs ([#35](https://github.com/XaviArnaus/pyxavi/pull/35))
- The `Config` module now supports also `TimeRotatingFileHandler` via Config parameters ([#34](https://github.com/XaviArnaus/pyxavi/pull/34))
- Added a `Dictionary.remove_none()` to clean keys with `None` values ([#34](https://github.com/XaviArnaus/pyxavi/pull/34))
- New `MastodonPublisher` class to help on publishing to Mastodon APIs ([#38](https://github.com/XaviArnaus/pyxavi/pull/38))
- Added a logger into the `Firefish` API wrapper ([#38](https://github.com/XaviArnaus/pyxavi/pull/38))
- The `Queue` class now is able to work stateless ([#43](https://github.com/XaviArnaus/pyxavi/pull/43))
- The `Config` class now is able to work without a file but a given dict ([#45](https://github.com/XaviArnaus/pyxavi/pull/45))
- First iteration to support slugified keys ([#46](https://github.com/XaviArnaus/pyxavi/pull/46))
- Added URL validation ([#47](https://github.com/XaviArnaus/pyxavi/pull/47))
- Discover the Feed URL from a given Site URL ([#48](https://github.com/XaviArnaus/pyxavi/pull/48))

### Changed

- Iterated the `Dictionary.merge()` so that now it performs a recursive merge for dict values ([#34](https://github.com/XaviArnaus/pyxavi/pull/34))
- Filename for class `Queue` is renamed ([#44](https://github.com/XaviArnaus/pyxavi/pull/44))

### Fixed

- Bug that made a wrong identification when the old config was used for `Logger` ([#37](https://github.com/XaviArnaus/pyxavi/pull/37))
- Bug that made `Firefish` status posting to fail with language codes containing an underscore ([#39](https://github.com/XaviArnaus/pyxavi/pull/39))
- Bad types in variables and method returns in the `Queue` class ([#40](https://github.com/XaviArnaus/pyxavi/pull/40))
- Bug that made Queue to not initialise its elements when loading ([#41](https://github.com/XaviArnaus/pyxavi/pull/41))
- Bug that made Queue to not deduplicate correctly complex items ([#42](https://github.com/XaviArnaus/pyxavi/pull/42))

## [v0.7.7](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.7) - 2023-11-11

### Added

- New `Queue` module ([#29](https://github.com/XaviArnaus/pyxavi/pull/29))

### Changed

- `Firefish.status_post` returns now a proper dict, with the ID in the first level ([#30](https://github.com/XaviArnaus/pyxavi/pull/30))

## [v0.7.6](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.6) - 2023-11-10

### Fixed

- Fixed a bug where the Storage will initialize wrong if the file exists but has Null content ([#28](https://github.com/XaviArnaus/pyxavi/pull/28))

## [v0.7.5](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.5) - 2023-11-10

### Added

- `Firefish` wrapper class now is able to post media ([#27](https://github.com/XaviArnaus/pyxavi/pull/27))

### Changed

- `Firefish.status_post` wrapper method now returns a dict with the response ([#27](https://github.com/XaviArnaus/pyxavi/pull/27))

## [v0.7.4](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.4) - 2023-11-06

### Changed

- Made `needs_resolving` static ([#26](https://github.com/XaviArnaus/pyxavi/pull/26))

## [v0.7.3](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.3) - 2023-11-06

### Added

- `Dictionary` has now list indexes wildcard support ([#25](https://github.com/XaviArnaus/pyxavi/pull/25))

## [v0.7.2](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.2) - 2023-11-06

### Added

- `Dictionary` class now can perform merges ([#24](https://github.com/XaviArnaus/pyxavi/pull/24))

## [v0.7.1](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.1) - 2023-11-05

### Added

- `Dictionary` class now can go through lists ([#23](https://github.com/XaviArnaus/pyxavi/pull/23))

## [v0.7.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.7.0) - 2023-10-30

### Added

- Added a `Dictionary` class to handle work with `dict` objects ([#22](https://github.com/XaviArnaus/pyxavi/pull/22))

### Changed

- Dict functionality is moved from `Storage` to `Dictionary`
- Changed the way the Fixes are identified in the Changelog, and it is updated.

## [v0.6.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.6.0) - 2023-10-27

### Added

- Added a `storage.get_keys_in()` ([#18](https://github.com/XaviArnaus/pyxavi/pull/18))
- Added a `Url` class for operations over URLs. At this point, just a shorthand for URL cleaning

### Fixed

- Fixed a Dependant bot spotted issue ([#20](https://github.com/XaviArnaus/pyxavi/pull/20))

## [v0.5.5](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.5.5) - 2023-10-23

### Fixed

- Fixed a wrong behaviour introduced in the previous version

## [v0.5.4](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.5.4) - 2023-10-23

### Added

- The ability for `Config` to merge dicts into the current instance. This enables to enrich the configs on the fly

## [v0.5.3](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.5.3) - 2023-10-18

### Added

- The ability for `Config` to merge config files into the current instance. This enables to use several config files under a single Config instance.

## [v0.5.2](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.5.2) - 2023-10-13

### Added

- The ability for `Logger` to receive a `base_path` so that the path can be correctly set, beyond what is said in the config.

## [v0.5.1](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.5.1) - 2023-10-06

### Fixed

- Corrected links in version titles in the Changelog

## [v0.5.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.5.0) - 2023-10-06

### Added

- New `Network` class to gather and validate some data

### Changed

- Changelog iterated to adhere to [Common Changelog](https://common-changelog.org). Will start from this version on.

### Removed

- **Breaking:** Removed `logger.getLogger()` as defined in previous version

## [v0.4.1](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.4.1)

- Added missing documentation

## [v0.4.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.4.0)

- Add `firefish` class as a wrapper for the Firefish API calls that I need
- Add a `logger.get_logger()` and mark `logger.getLogger()` as deprecated, to be removed in v0.5.0

## [v0.3.3](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.3.3)

- Bump PyYaml to version 6.0.1 as 6.0 is broken

## [v0.3.2](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.3.2)

- Make non built-in objects inspection depth controlable in `dd` recurdive call

## [v0.3.1](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.3.1)

- Iterate over the `pyproject.toml` and the `README.md` to make them more appealing in pypi.org

## [v0.3.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.3.0)

- Rewrite the `debugger.dd`.
- New `terminal_color` class for printing with colors.

## [v0.2.1](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.2.1)

- Add traceback function to debugger lib.

## [v0.2.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.2.0)

- Add *Janitor* API wrapper

## [v0.1.5](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.1.5)

- Bugfix in Storage when set needs to identify empty dictionaries

## [v0.1.4](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.1.4)

- Initialize in-memory stack for Storage when the file is just touched

## [v0.1.3](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.1.3)

- Make Logger to create the log file in case it does not exist yet

## [v0.1.2](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.1.2)

- Bump Poetry required version to 1.2.0

## [v0.1.1](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.1.1)

- Minor fix in `Media`.

## [v0.1.0](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.1.0)

- Move from `setup.py` to `pyproject.toml`
- Apply Flake8 & Yapf
- Add some basic tests
- Some fixes thanks to tests
- Rename the project from `python-bundle` to `pyxavi`
- Add some Docstrings
- Merge together `Media` and `Downloader` into `Media`
- `Media` methods renamed

## [v0.0.6](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.0.6)

- Added `Downloader`

## [v0.0.5](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.0.5)

- Added `Media`

# [v0.0.4](https://github.com/XaviArnaus/pyxavi/releases/tag/v0.0.4)

- Created package
- Added `Config`, `Logger`, `Storage` and `Debugger`