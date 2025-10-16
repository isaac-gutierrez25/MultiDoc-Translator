# Change Log

All notable changes to the "auto-translate-readmes" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [1.0.6] - 2025-10-17

### Changed

- **Switched Python Translation Library**: Replaced the unstable `googletrans` library with `deep-translator` in the Python script (`auto_translate_readmes.py`) to permanently fix persistent connection errors (`JSONDecodeError`) and improve stability.
- **Implemented Bundling**: The VS Code extension now uses `esbuild` to bundle all necessary code into a single file. This fixes a critical issue where the extension would not run after being published to the Marketplace.
- **Refined Translation Logic**: The core logic was reverted to a more stable single-request-per-language model. This method uses a robust placeholder system to protect all Markdown structures (code blocks, bold text, newlines, etc.) ensuring that the translated file's formatting is identical to the source file.

### Fixed

- **Complete Formatting Integrity**: Fixed numerous formatting bugs that occurred during translation, including:
  - Incorrect spacing inside and around **bold** and `inline code` elements.
  - Disappearing newlines, which caused an incorrect line count in translated files.
  - Corrupted list markers (e.g., `-Text` instead of `- Text`), particularly in the French translation.
  - Disappearing emojis from list items.
- **Header Duplication**: Fixed a bug that caused the language switcher block to be duplicated in the headers of translated files.

## [1.0.5]

_(This version contained various unsuccessful attempts to fix formatting and was superseded by the more stable logic in 1.0.6.)_

## [1.0.4] - 2025-10-15

### Added

- The language switcher block (`> 🌐 Available in other languages:...`) is now automatically added to the root `README.md` if it is missing, making the initial setup easier.

### Fixed

- Fixed a critical bug where Markdown table structures would break in some translations (e.g., Chinese) due to corrupted separator lines.
- Resolved an issue where placeholders for protected content (like code blocks) were being incorrectly translated in certain languages (e.g., Polish), causing parts of the README to not render correctly.
- Corrected multiple Markdown list formatting errors where spaces after list item markers (`-`) were removed or unwanted indentation was added, ensuring lists render correctly across all languages.

## [1.0.3] - 2025-10-14

### Changed

- Optimized the extension by excluding unnecessary files from the package, resulting in a smaller size and faster installation.

## [1.0.2] - 2025-10-14

### Added

- Initial public release.

## [Unreleased]

- Initial release
