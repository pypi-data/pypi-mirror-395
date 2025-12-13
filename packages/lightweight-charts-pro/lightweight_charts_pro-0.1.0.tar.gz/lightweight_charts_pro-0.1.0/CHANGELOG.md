# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-12-02

### Added
- Initial release of lightweight-charts-pro (renamed from lightweight-charts-core)
- Framework-agnostic Python core library for TradingView Lightweight Charts
- Data models for all chart types (Line, Area, Candlestick, Bar, Histogram, Baseline)
- Comprehensive chart configuration options
- Base classes (`BaseChart`, `BaseChartManager`) for framework extensions
- Type-safe data validation and type checking
- Standardized exception handling
- Complete type definitions with enums and hints

### Changed
- Package renamed from `lightweight-charts-core` to `lightweight-charts-pro`
- Updated all internal imports to use new package name
- Updated logger names to use new package name

### Fixed
- Corrected import references throughout codebase
- Fixed LineOptions default values for markers (pointMarkersVisible and crosshairMarkerVisible default to False)

[unreleased]: https://github.com/nandkapadia/lightweight-charts-pro-python/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nandkapadia/lightweight-charts-pro-python/releases/tag/v0.1.0
