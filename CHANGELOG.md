# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-10

### Added
- Initial release of Samaya CLI timer
- Three preset session modes: short (5 min), medium (15 min), long (25 min)
- Custom duration support with `--time` flag
- Background brown noise during sessions
- Bell notification when sessions complete
- Cross-platform support (macOS, Linux, Windows)
- Keyboard interruption with Ctrl+C
- MIT License
- Basic test suite
- Command-line interface with argparse

### Features
- Minimal dependencies (Python standard library only)
- Audio playback for ambient noise and notifications
- Clean terminal-based interface
- Session mode listing with `--list-modes`
- Version information with `--version`