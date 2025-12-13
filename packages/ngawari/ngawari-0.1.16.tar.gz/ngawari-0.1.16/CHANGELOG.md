# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.1.16] - 2025-12-08

### Added
- NIfTI file compression functionality (`nii_to_niigz`)
- NIfTI file writing functionality (`writeNifti`) (also via `writeVTKFile` for nii and nii.gz)


### Changed
- Updated documentation
## [0.1.15] - 2025-11-25

### Fixed
- Bug fixes in `filterNullOutsideSurface` and `filterNullInsideSurface`
- Bug fixes in `filterGetEnclosedPts`
- Bug fixes in `filterGetPointsInsideSurface`
- Bug fixes in `filterGetPointIDsInsideSurface`
- Bug fixes in `filterGetPolydataInsideSurface`
- Bug fixes in `filterGetArrayValuesWithinSurface`
- Bug fixes in `filterNullOutsideSurface`
- Bug fixes in `filterNullInsideSurface`

### Added
- Comprehensive test suite for `vtkfilters.py` covering all major functions and edge cases

## [0.1.14] - 2025-10-15

### Added
- Ellipse fitting functionality (`fit_ellipse_2d` and `fit_ellipse_3d` in `ftk`)

### Changed
- Improved functionality on enclosed points filter
- Added checks on limits for VOI extraction
- Cleaned up comments and parameter checking

## [0.1.13] - 2025-09-01

### Added
- Point reduction helper function
- Gradient filter for image data (`filterImageGradient`)
- Image-based merge functionality (`mergeSurfsByPointsInsideVti`)

### Changed
- Updated quickstart documentation
- Improved documentation formatting

## [0.1.12] - 2025-06-23

### Added
- ROI to ROI plane algorithm (`roi_line_to_roi_plane`)
- Default extent (full) to extract VOI function

### Changed
- Updated documentation strings
- Improved GitHub Pages deployment workflow
- Updated GitHub Actions to use v4 artifact actions
- Simplified docs workflow
- Updated README with new documentation links

## [0.1.11] - 2025-04-02

### Added
- TIFF reader support (`readTIFF` in `fIO`)

### Fixed
- Fixed deprecated NumPy feature bugs (multiple fixes)
- Fixed JSON serializable errors

### Changed
- Small helpers and efficiency improvements
- Fixed typo bug
- Fixed point-to-point distance error

## [0.1.10] - 2025-03-25

### Added
- Pathlib support in `fIO` module
- Updated VTS to VTI conversion algorithms

### Changed
- Updated project configuration to use TOML format (`pyproject.toml`)
- Updated `getDimensions` method to pass pointer (VTK 9.3 compatibility)

## [0.1.9] - 2025-03-07

### Added
- Count points in VTI filter (`countPointsInVti`)
- Help documentation for image mask filters

## [0.1.8] - 2025-02-11

### Added
- NIfTI (.nii.gz) reader support
- Polydata to stencil filter (`filterSurfaceToImageStencil`)
- Edges filter (`filterExtractEdges`, `getBoundaryEdges`, `getEdges`)

### Changed
- Code cleanup and refactoring

## [0.1.7] - 2025-01-07

### Added
- Polydata volume calculation (`getVolumeSurfaceAreaOfPolyData`)

### Changed
- Updated documentation strings
- Switched to Python module for tar operations

## [0.1.6] - 2024-12-20

### Changed
- Updated docstrings

## [0.1.5] - 2024-11-26

### Added
- Comprehensive tests for `fIO` module

### Fixed
- Small error catching improvements
- Formatting improvements

## [0.1.4] - 2024-11-22

### Fixed
- Small bug fixes

## [0.1.3] - 2024-11-08

### Added
- Tube filter can now vary radius by scalar values

## [0.1.2] - 2024-10-30

### Added
- Iterative Closest Points (ICP) transform filter (`iterativeClosestPointsTransform`, `transformPolydataA_to_B_ICP`)

## [0.1.1] - 2024-10-25

### Added
- Point to cell data filter (`pointToCellData`)
- Cell to point data filter (`cellToPointData`)

### Fixed
- Bug fix in `getIdOfPointClosestToX`

## [0.1.0] - 2024-10-21

### Added
- Tube filter (`tubeFilter`)
- Boolean filter for polydata (`filterBoolean`)

## [0.0.9] - 2024-10-11

### Added
- Additional VTK filters

## [0.0.8] - 2024-10-09

### Changed
- Added documentation strings throughout codebase

## [0.0.7] - 2024-10-07

### Fixed
- Fixed named parameter errors

## [0.0.6] - 2024-10-02

### Changed
- Major refactoring and code organization
- Cleaned up imports
- Fixed missing functions

## [0.0.5] - 2024-09-27

### Changed
- Code refactoring

## [0.0.4] - 2024-09-25

### Changed
- Code organization and refactoring

## [0.0.3] - 2024-09-24

### Added
- Initial documentation strings
- Test suite foundation

### Changed
- Code cleanup

## [0.0.2] - 2024-09-18

### Added
- Initial project setup

## [0.0.1] - 2024-09-17

### Added
- Initial commit
- Core functionality:
  - `ftk` module: Geometric and mathematical utilities
  - `fIO` module: File I/O operations for VTK formats
  - `vtkfilters` module: VTK filter wrappers and utilities

---

## How to Update This Changelog

When making changes:

1. **For new features**: Add to "Added" section under [Unreleased]
2. **For bug fixes**: Add to "Fixed" section under [Unreleased]
3. **For changes**: Add to "Changed" section under [Unreleased]
4. **For deprecations**: Add to "Deprecated" section under [Unreleased]
5. **For removals**: Add to "Removed" section under [Unreleased]

When releasing a new version:

1. Move all items from [Unreleased] to a new version section
2. Update the version number and date
3. Commit with message: "Update CHANGELOG for version X.Y.Z"

