# Change Log

All notable changes to the "auto-translate-readmes" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [Unreleased]

---

## [1.0.9] - 2025-10-17

### Changed

- **Refined Translation Engine (Final Revision)**  
  Perfected the translation process to preserve the _exact_ structure, spacing, and newline count of the original `README.md`.
  - Introduced newline-preserving logic (`split(/(\n)/)`) ensuring identical layout across all translated files.
  - Improved Markdown recognition to safely skip translation for lists, tables, code blocks, headings, links, and images.
  - Removed formatting normalization (e.g., newline trimming, spacing regex) to maintain 1:1 line mapping with the source file.
  - Enhanced handling for mixed-content lines (text with inline code, emojis, or list markers).
  - Ensured output is written using consistent UTF-8 encoding and preserved EOL format (Windows `\r\n` or Unix `\n`).

### Fixed

- **Exact Markdown Fidelity** – The translated files now visually and structurally match the source `README.md` exactly.
- **Indentation Restoration** – Fixed issues where sub-list or nested list items lost their indentation after translation.
- **Empty Line Preservation** – Fixed disappearing blank lines between paragraphs and lists.
- **Bold & Inline Code Handling** – Fixed cases where `**bold**` and `inline code` at line starts were misformatted.
- **Table Line Integrity** – Fixed corrupted separator lines in complex Markdown tables across non-Latin languages (e.g., Chinese, Korean).

---

## [1.0.8] - 2025-10-17

### Changed

- **Finalized Translation Logic**: Improved precision for list-item spacing and formatting integrity.
- Enhanced Markdown preservation and refined translation context handling.

### Fixed

- Preserved sub-list indentation and newlines between paragraphs.
- Fixed formatting of bold text and tables during translation.

---

## [1.0.7] - 2025-10-17

### Added

- **User Feedback**: The "Generate" button now shows a spinning icon and is disabled during translation.  
  The process also triggers an info message and opens the output panel automatically.

### Changed

- **Implemented Bundling**: Now uses **esbuild** to bundle all code into one file.
- **Improved Translation Logic**: Rewritten to translate line-by-line while protecting all Markdown structures.

### Fixed

- Publishing bug due to missing dependencies.
- Formatting errors including missing spaces, broken list markers, and lost emojis.
- Duplicate language switcher header.
- Added missing type dependencies for build success.

---

## [1.0.6]

_(Internal development build, superseded by 1.0.7.)_

---

## [1.0.5] - 2025-10-17

### Changed

- Replaced unstable `googletrans` library with `deep-translator` for better reliability.

### Fixed

- Fixed Markdown corruption involving bold, inline code, and tables.
- Fixed list marker merging (`-Text` → `- Text`).
- Moved `node-fetch` to dependencies to prevent runtime failure.

---

## [1.0.4] - 2025-10-15

### Added

- Automatically adds a multilingual switcher block to `README.md` if missing.

### Fixed

- Fixed broken Markdown table separators during translation.

---

## [1.0.3] - 2025-10-14

### Changed

- Optimized packaging for smaller size and faster installation.

---

## [1.0.2] - 2025-10-14

### Added

- Initial public release.
