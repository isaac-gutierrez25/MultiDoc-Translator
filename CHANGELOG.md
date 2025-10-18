# Change Log

All notable changes to the "auto-translate-readmes" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [Unreleased]

---

## [1.1.0] – 2025-10-18

### ✨ Added

- **Smart Paragraph Grouping Engine**  
  Added intelligent paragraph grouping to translate multi-line paragraphs as cohesive blocks while preserving the original Markdown layout.  
  → Produces more accurate, context-aware translations without changing line alignment.

- **Diff Preview Mode (Experimental)**  
  Users can now preview translation diffs before saving output using  
  `auto-translate-readmes.previewDiff` command in VS Code Output Panel.

- **Auto-Detect README Charset**  
  Automatically detects and preserves source file encoding (`UTF-8`, `UTF-16`, or `UTF-8-BOM`) for cross-platform consistency.

---

### 🔧 Changed

- **Inline Markdown Tokenizer v3**  
  Updated tokenizer to protect complex Markdown combinations:

  - `**bold + _italic_ mix**`
  - `[Click _here_](url)`
  - Inline HTML elements like `<span>` or `<img>`

- **Code Block Consistency**  
  Code blocks are now perfectly preserved with original indentation and spacing (no trimming or extra newlines).

- **Improved Language Switcher Formatting**  
  The multilingual switcher now automatically adjusts punctuation and spacing style for each target language (e.g., Japanese full-width colons, French spaces before colons).

- **More Stable Google API Integration**  
  Now includes automatic fallback to a secondary endpoint when `translate.googleapis.com` hits rate limits or network errors.

---

### 🐞 Fixed

- **Bold Handling (Edge Case)**  
  Fixed cases where `**Before:**` or `**After (Absolute):**` were split into `* *Before:**`.

- **Non-breaking Space in Lists**  
  Prevented issues where hyphens `-` in list items merged directly with text in some languages (e.g., French or Russian).

- **Preserve Trailing Newlines**  
  Translation output now retains the same number of blank lines as the source file — none are trimmed.

- **Emoji Stability**  
  Fixed encoding issues where emojis or special characters were dropped during translation.

- **Cross-Platform EOL Consistency**  
  Ensures consistent end-of-line characters (`\r\n` for Windows, `\n` for Unix) according to the source file.

---

### 🚀 Developer Notes

- Translation logic is now modularized under `translateBlock()` with async batching for ~30% faster translation.
- Each generated README includes a metadata comment:  
  `<!-- Auto-Translated v1.1.0 -->`  
  to track build versions automatically.
- Ready for **VS Code Marketplace v1.1 stable release**.

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
