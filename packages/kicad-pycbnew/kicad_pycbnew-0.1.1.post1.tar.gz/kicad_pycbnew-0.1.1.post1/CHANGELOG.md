# Changelog

All notable changes for this project will be documented here.

## [0.1.1] - 2025-11-11

### Added
- This `CHANGELOG.md` file.
- A new example file (`examples/08_graphics_and_edge_cuts.py`) showing how to use graphical classes (texts, lines, arcs,
  rectangle, dimensions) on silkscreen and edge-cuts layers.

### Fixed
- `KGrDimension` class: the `sexp_tree` method was returning a malformed S-expression, preventing KiCad from opening the board file.
- `Arc.from_center_radius` class method did not correctly handle arcs where `angle2 > angle1`.

## [0.1.0] - 2025-11-10

### Added
- First public release of kicad-pycbnew.

