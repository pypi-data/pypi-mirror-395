# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.5] - 2025-12-07

### Fixed
- Suppressed plyer internal error messages from stderr while maintaining notification functionality
- Improved user experience by hiding irrelevant import errors

## [1.0.4] - 2025-12-07

### Fixed
- Fixed notification fallback logic to properly handle plyer import errors
- Ensured osascript fallback works correctly on macOS

## [1.0.3] - 2025-12-07

### Changed
- Made `pyobjus` an optional dependency to avoid build issues
- macOS users can install with `pip install pomodoro-multiplatform[macos]` for native notifications
- Falls back to osascript on macOS without pyobjus

## [1.0.2] - 2025-12-07

### Fixed
- Added `pyobjus` dependency for macOS notification support

## [1.0.1] - 2025-12-07

### Changed
- Package name changed to `pomodoro-multiplatform`
- Added linting/type checking cache to gitignore

## [1.0.0] - 2025-12-07

### Added
- Initial release
- Cross-platform support (Windows, macOS, Linux)
- Desktop notifications using plyer
- Sound notifications
- Customizable work/break durations
- Long break confirmation dialog
- Command-line interface with argparse
- Comprehensive test suite
- CI/CD with GitHub Actions
- PyPI package support

### Features
- Default Pomodoro timings (25/5/15 minutes)
- Keyboard interrupt handling (Ctrl+C)
- Platform-specific notification fallbacks
- Multi-platform sound support

[1.0.0]: https://github.com/Rito0421/pomodoro/releases/tag/v1.0.0
