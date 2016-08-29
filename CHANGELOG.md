# Change Log

All notable changes to this project will be documented in this file.

The versioning process follows a scheme based on [Semantic Versioning](http://semver.org/), and the CHANGELOG.md format is based on [Keep a Changelog](http://keepachangelog.com/).

## [Unreleased] - 2016-08-29

### Fixed
- Fragment identifiers were not normalized out when comparing 2 URLs (see issue #8), causing an issue where `site.com/path#fragment` was not marked as being the same resource as `site.com/path`.

## 0.0.1 - 2016-08-20

Initial release


[Unreleased]: https://github.com/liviu-/average-pixels/compare/v0.0.1...HEAD
