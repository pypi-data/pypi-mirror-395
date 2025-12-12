# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-12-04

### Added
- **Song Logo Display System**: Render official song or artist logos with full customization
  - Auto overlay of song logo with fallback to artist avatar
  - Custom logo positioning, opacity (0.0–1.0), and blend modes (normal, multiply, overlay, screen)
  - Automatic background contrast detection and glow/shadow effects
  - URL and local file support with auto-resize to fit layout
  - Per-template logo rules
- **Advanced Visual Effects**: Background blur effects, advanced gradient editor (linear/radial/diagonal), multi-layer shadow engine, per-layer opacity control, smart stroke & outline system, dynamic corner radius, advanced mask editor, noise & texture overlays, glassmorphism effects, hue/saturation/exposure filters
- **Engine Upgrades**: Smart auto-layout engine, Ultra HD 8K export mode, progressive rendering, adaptive font spacing, improved text anti-aliasing, template-level performance optimization, parallel rendering for batch jobs
- **Automation & Metadata**: Automatic metadata loading from JSON/API, EXIF + PNG metadata embedding, watermark system with optional toggles, automatic file naming rules, template-aware metadata formatting
- **Enhanced CLI & Workflows**: Interactive CLI mode, live terminal ASCII preview, profiles system via profiles.json, preset switcher, batch queue processing, template validation, preview-only mode, dry-run execution
- **New API Methods**: `set_song_logo()`, `set_logo_position()`, `set_logo_opacity()`, `set_logo_blend_mode()`, `enable_auto_logo()`, `enable_watermark()`, `set_watermark_text()`, `use_profile()`, `enable_background_blur()`, `set_export_quality()`
- **New CLI Commands**: `musicard logo set/auto`, `musicard profile use`, `musicard queue add/start`, `musicard preview live`, `musicard render dry-run`, `musicard export 8k`

### Changed
- Improved rendering engine performance (30-40% speed increase)
- Enhanced memory optimization and smarter cache invalidation
- Better async batch stability
- Updated type hints and Google-style docstrings throughout
- Cross-platform compatibility improvements (Windows, Linux, macOS)

### Fixed
- Weak architectural areas auto-fixed for better maintainability

## [2.1.0] - 2025-01-01

### Added
- **SVG Export Support**: Export music cards as SVG files using `export_svg()` method
- **Caching System**: Intelligent caching for images, fonts, and generated cards using diskcache
- **Batch Processing**: Generate multiple cards at once with `batch_generate()` and `async_batch_generate()`
- **Theme Presets**: Save and load theme configurations as JSON presets
- **Enhanced CLI**: Support for SVG export, batch processing, and multiple formats
- **Multiple Output Formats**: Support for PNG, JPEG, and SVG export
- **Cache Management**: View cache statistics and clear cache via CLI and API

### Changed
- Updated dependencies to include cairosvg and diskcache
- Improved error handling and validation
- Enhanced documentation with new features

### Fixed
- Import issues and package structure improvements
- Better type hints throughout the codebase

## [2.0.0] - 2024-12-01

### Added
- Complete rewrite with 100% feature parity to musicard NPM package
- All 5 themes: Classic, Classic Pro, Dynamic, Mini, Upcoming
- Async support for card generation
- CLI tool for command-line usage
- Comprehensive test suite
- Type hints throughout

### Changed
- New modular architecture with separate core, templates, and utils
- Improved API design with better method names
- Enhanced font management system

### Removed
- Old MusicCard class (replaced with Musicard)

## [1.1.0] - 2024-11-01

### Added
- Initial release of musicard-py
- Support for three themes: Classic, Modern, and Mini
- MusicCard class for generating beautiful music card images
- Progress bar visualization with customizable colors
- Thumbnail image support (URLs and local paths)
- Customizable colors, sizes, and theme-specific options
- Easy-to-use API for Discord bots and other applications
- Asynchronous generation method (currently synchronous)
- Export to PNG bytes or save to file
- Comprehensive test suite
- Example scripts and documentation

### Features
- 🎨 Multiple Themes: Classic (dark, elegant), Modern (gradient), Mini (compact)
- 🖼️ Image Support: Load thumbnails from URLs or local files
- 📊 Progress Bars: Visual progress indicators
- 🎯 Simple API: Class-based interface
- 🔧 Customizable: Colors, sizes, fonts
- 📦 Lightweight: Minimal dependencies (Pillow + requests)
- ⚡ Fast: Generate images in milliseconds

### Credits
- Inspired by [unburn/musicard](https://github.com/unburn/musicard) JavaScript project
