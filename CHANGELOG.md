# Change Log

All notable changes to the "auto-translate-readmes" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [1.0.7] - 2025-10-17

### Added

- **User Feedback**: The "Generate" button in the sidebar now shows a spinning icon and is disabled during the translation process to provide clear visual feedback. An initial notification is also shown, and the output panel appears immediately.

### Changed

- **Implemented Bundling**: The extension now uses **esbuild** to bundle all necessary code into a single file. This is a critical change that fixes the issue where the extension would not run after being installed from the Marketplace.
- **Improved Translation Logic**: The core translation logic has been rewritten to be more robust. It now processes files line-by-line while protecting all Markdown structures (code blocks, bold text, newlines, indentation, etc.), ensuring translated files have a structure identical to the source file.

### Fixed

- **Publishing Bug**: Fixed the critical bug where the extension was not functional after being published due to missing dependencies in the final package.
- **Complete Formatting Integrity**: Fixed numerous formatting bugs that occurred during translation, including:
  - Incorrect spacing inside and around **bold** and `inline code` elements.
  - Disappearing newlines and incorrect line counts in translated files.
  - Corrupted list markers (e.g., `-Text` instead of `- Text`).
  - Disappearing emojis from list items.
- **Header Duplication**: Fixed a bug that caused the language switcher block to be duplicated in the headers of translated files.
- **Build Configuration**: Added missing `@types/mocha` and `@types/node-fetch` to `devDependencies` to resolve build-time errors.

## [1.0.6]

_(This version was an internal development build with various attempts to fix formatting and was superseded by the more stable logic in 1.0.7.)_

## [1.0.5] - 2025-10-17

### Changed

- **Switched Python Translation Library**: Replaced the unstable `googletrans` library with `deep-translator` in the Python script (`auto_translate_readmes.py`) to permanently fix persistent connection errors (`JSONDecodeError`) and improve stability.

### Fixed

- **Markdown Integrity**:
  - Fixed a critical bug where various Markdown elements like **bold text** (`**text**`), `inline code`, sub-list indentation, and table structures were being corrupted or altered during translation.
  - Corrected a bug where list markers (`-`) would merge with text (e.g., `-Text` instead of `- Text`), particularly in the French translation.
- **Build & Configuration**:
  - Moved `node-fetch` to `dependencies` to resolve runtime errors in the packaged extension.

_(Note: Some changes from 1.0.5 were re-iterated and finalized in 1.0.7)_

## [1.0.4] - 2025-10-15

### Added

- The language switcher block (`> 🌐 Available in other languages:...`) is now automatically added to the root `README.md` if it is missing, making the initial setup easier.

### Fixed

- Fixed a critical bug where Markdown table structures would break in some translations (e.g., Chinese) due to corrupted separator lines.

## [1.0.3] - 2025-10-14

### Changed

- Optimized the extension by excluding unnecessary files from the package, resulting in a smaller size and faster installation.

## [1.0.2] - 2025-10-14

### Added

- Initial public release.

## [Unreleased]

- Initial release
