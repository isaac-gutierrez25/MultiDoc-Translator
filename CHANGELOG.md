# Change Log

All notable changes to the "auto-translate-readmes" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [1.0.5] - 2025-10-17

### Changed

- **Improved Translation Logic**: The translation process now preserves all original Markdown formatting, including newlines, indentation, and spacing, ensuring translated files have the exact same structure as the source file.

### Fixed

- **Markdown Integrity**:
  - Fixed a critical bug where various Markdown elements like **bold text** (`**text**`), `inline code`, sub-list indentation, and table structures were being corrupted or altered during translation.
  - Resolved an issue where emojis were being removed from translated files.
  - Corrected a bug where list markers (`-`) would merge with text (e.g., `-Text` instead of `- Text`), particularly in the French translation.
- **Header Duplication**: Fixed a bug that caused the language switcher block to be duplicated in the headers of translated files.
- **Build & Configuration**:
  - Moved `node-fetch` to `dependencies` to resolve runtime errors in the packaged extension.
  - Added missing `@types/mocha` and `@types/node-fetch` to `devDependencies` to fix build-time errors.

## [1.0.4] - 2025-10-15

### Added

- The language switcher block (`> 🌐 Available in other languages:...`) is now automatically added to the root `README.md` if it is missing, making the initial setup easier.

### Fixed

- Fixed a critical bug where Markdown table structures would break in some translations (e.g., Chinese) due to corrupted separator lines.
- Resolved an issue where placeholders for protected content (like code blocks) were being incorrectly translated in certain languages (e.g., Polish), causing parts of the README to not render correctly.
- Corrected multiple Markdown list formatting errors where spaces after list item markers (`-`) were removed or unwanted indentation was added, ensuring lists render correctly across all languages.
- Improved the overall robustness of the translation process by adding better protection for various Markdown syntax elements.

## [1.0.3] - 2025-10-14

### Changed

- Optimized the extension by excluding unnecessary files from the package, resulting in a smaller size and faster installation.

## [1.0.2] - 2025-10-14

### Added

- Initial public release.

## [Unreleased]

- Initial release
