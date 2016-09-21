# Change Log

All notable changes to this project will be documented in this file.

The versioning process follows a scheme somewhat based on [Semantic Versioning](http://semver.org/), and the CHANGELOG.md format is based on [Keep a Changelog](http://keepachangelog.com/).

## [Unreleased]

### Added
- Added a link to th GitHub page in case people want to report issues -- bugs happen and I'm not always paying attention ([issue #10](https://github.com/liviu-/crosslink-ml-hn/issues/10)).

### Changed
- **BREAKING** Not an immediately breaking change, but only Python3.5 will be tested for by Travis ([issue #17](https://github.com/liviu-/crosslink-ml-hn/issues/17))
- Changed where shell arguments are parsed (at the moment, just `--version`). This makes it slower, but avoids a bug with interactin with `pytest`'s own arguments.

## [0.2.0] - 2016-09-15

### Changed
- Simplified the URL matching scheme. The only exception right now is arXiv as DeepMind updated their blog and adding too many exceptions makes for cumbersome code. If more false positives arise, I'll try to improve then.
- Config file is now stored in YAML format, and the path to the file is by default `$HOME/.crosslinking_config.yaml`, but it may be provided by the user via the `CROSSLINKING_CONFIG` environment variable.

## [0.1.2] - 2016-09-07

### Fixed
- Added anoter exception for PLOS journals because they also encode the article ID in GET params (issue [#16](https://github.com/liviu-/crosslink-ml-hn/issues/16))

## [0.1.1] - 2016-08-29

### Fixed
-- Added `config.py` back to pass CI tests

## [0.1.0] - 2016-08-29

### Fixed
- If the path is simply 'blog', then the URL fragments are considered when differentiating between the links. This accommodates DeepMind URL scheme and hopefully others as well.

### Added
- Added a `--version` CLI argument to the tool
- Added some special rules for arXiv URLs to match slightly different links

## [0.0.2] - 2016-08-29

### Fixed
- Fragment identifiers were not normalized out when comparing 2 URLs (see [issue #8](https://github.com/liviu-/crosslink-ml-hn/issues/8)), causing an issue where `site.com/path#fragment` was not marked as being the same resource as `site.com/path`.

## 0.0.1 - 2016-08-20

Initial release


[1.0.0]: https://github.com/liviu-/crosslink-ml-hn/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/liviu-/crosslink-ml-hn/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/liviu-/crosslink-ml-hn/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/liviu-/crosslink-ml-hn/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/liviu-/crosslink-ml-hn/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/liviu-/crosslink-ml-hn/compare/v0.0.1...v0.0.2
