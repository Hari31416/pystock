# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Added the changelog.
- Added `style` module. Printing is now colorful! Also, text in portfolio summary and model optimization are more aligned.

### Fixed

- Chnaged the `Model.expected_return_of_stock` so that it does not calculate the expected return of the benchmark if it is already calculated. Portfolio optimization will now be faster.

### Changed

- `Model.expected_return_of_stock` now does not prints warning messages about FFF parameters not calculated. Instead it raises exception if FFF parameters are not calculated but "fff3" or "fff5" is passed as `model` argument.

### Removed

- The `Model.portfolio_frontier` is removed. Future version will add a feature for plotting efficient frontier for arbitrary number of stocks.

## [0.2.2] - 2023-01-14

### Added

- Added tests for all the modules.
- Added Gihub Python Package workflow badge to README.
- A new directory tests/data containing the data during the tests.
- Added new attribute `_all_set` to `Portfolio` to avoid unnecessary computations.

### Changed

- `docs` folder is now in the main branch too.
- `tests` directory was changed to a module for eay importing.
- `Model.calculate_fff_params` now accepts a parameter `download` which makes it easy to download FFF parameters directly from `Model`.

### Fixed

- Fixed issue where `Portfolio.remove_stocks()` was throwing errors sometimes.
- FIxed issue so that calling `calculate_fff_params` method from `Model` or `Portfolio` does not give "file already exist" warning.

## [0.2.1] - 2023-01-11

### Added

- Added some sample data files to the `Data` folder.
- `Portfolio.remove_stocks()` now removes the calculated parameters too.
- `Portfolio.stock_params` for FFF parameters is changed to `Portfolio.stock_fff_params`.
- `Portfolio.portfolio_return` is changed to `Portfolio.get_portfolio_return` for consistancy.
- Calculated FFF parameters now have the index column designating what the corresponding coefficients are for.
- Fama-French factors can now be downloaded directly from `Portfolio`

### Changed

- Fixed some typos.
- Removed unncessary imports.
- Fixed typos in docstring.
- Added argument `print_summary` in `summary` method to avoid unncessary prints.

### Fixed

- Fixed issue where `PortfolioExists` was raised after `add_portfolio` failed to add `Portfolio` to `Model`.
- Fixed issue where an error was raised while calling `add_portfolio` with default parameters.

## [0.2.0] - 2023-01-02

### Added

- Added documenation using sphinx.
- Added download number and version badges.

## [0.1.0] - 2023-01-02

Initial release.

### Added

- Added MIT license.
- Added the modules.
