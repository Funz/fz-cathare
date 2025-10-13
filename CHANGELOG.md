# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-10-13

### Added
- Initial port of [plugin-cathare](https://github.com/Funz/plugin-cathare) to new fz framework
- Python-based output parser for CATHARE FORT07 files
- Support for EVOLUTION data extraction with TIME and Z coordinates
- Model definition in `.fz/models/Cathare.json`
- Calculator configuration in `.fz/calculators/Localhost_Cathare.json`
- Comprehensive README with usage examples
- Example scripts demonstrating:
  - Basic output parsing (`example.py`)
  - Complete parametric study workflow (`example_parametric_study.py`)
  - Input template with variables (`tests/example_parametric.txt`)
- Test suite with validation against known values (`tests/test_output_parsing.py`)
- Test case files from original plugin (CNV22)

### Changed
- Ported Java `CathareIOPlugin.readOutput()` method to Python
- Adapted to new fz plugin architecture using JSON configuration
- Output parsing now returns dictionary format compatible with fz framework

### Technical Details
- Variable prefix: `$` (e.g., `$temperature`)
- Formula prefix: `@` (e.g., `@($temp + 273.15)`)
- Comment line marker: `*`
- Delimiter: `()` for variable and formula names

### Original Plugin
This is a port of the Java-based plugin created by IRSN/Yann Richet.
Original repository: https://github.com/Funz/plugin-cathare
