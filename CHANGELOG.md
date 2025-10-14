# Change Log

All notable changes to the "auto-translate-readmes" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [1.0.4] - 2025-10-15

### Added

- The language switcher block (`> 🌐 Available in other languages:...`) is now automatically added to the root `README.md` if it is missing, making the initial setup easier.

### Fixed

- Fixed a critical bug where Markdown table structures would break in some translations (e.g., Chinese) due to corrupted separator lines.
- Resolved an issue where placeholders for protected content (like code blocks) were being incorrectly translated in certain languages (e.g., Polish), causing parts of the README to not render correctly.
- Corrected multiple Markdown list formatting errors where spaces after list item markers (`-`) were removed or unwanted indentation was added, ensuring lists render correctly across all languages.
- Improved the overall robustness of the translation process by adding better protection for various Markdown syntax elements.

## [Unreleased]

- Initial release

---

## [1.0.3] - 2025-10-14

### Changed

- Optimized the extension by excluding unnecessary files from the package, resulting in a smaller size and faster installation.

## [1.0.2] - 2025-10-14

### Added

- Initial public release.
