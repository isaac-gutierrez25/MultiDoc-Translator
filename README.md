# 🌍 Auto Translate Readmes

[![VS Code](https://img.shields.io/badge/VS%20Code-1.85.0+-blue.svg)](https://code.visualstudio.com/)
[![Version](https://img.shields.io/github/v/release/fatonyahmadfauzi/Auto-Translate-Readmes?color=blue.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/releases)
[![License: MIT](https://img.shields.io/github/license/fatonyahmadfauzi/Auto-Translate-Readmes?color=green.svg)](LICENSE)
[![Build Status](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/actions/workflows/main.yml/badge.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/actions)
[![Repo Size](https://img.shields.io/github/repo-size/fatonyahmadfauzi/Auto-Translate-Readmes?color=yellow.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes)
[![Last Commit](https://img.shields.io/github/last-commit/fatonyahmadfauzi/Auto-Translate-Readmes?color=brightgreen.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/commits/main)
[![Installs](https://vsmarketplacebadges.dev/installs-short/fatonyahmadfauzi.auto-translate-readmes.svg)](https://marketplace.visualstudio.com/items?itemName=fatonyahmadfauzi.auto-translate-readmes)
[![Downloads](https://vsmarketplacebadges.dev/downloads-short/fatonyahmadfauzi.auto-translate-readmes.svg)](https://marketplace.visualstudio.com/items?itemName=fatonyahmadfauzi.auto-translate-readmes)
[![Rating](https://vsmarketplacebadges.dev/rating-short/fatonyahmadfauzi.auto-translate-readmes.svg)](https://marketplace.visualstudio.com/items?itemName=fatonyahmadfauzi.auto-translate-readmes)

---

Visual Studio Code extension that automatically generates multilingual `README.md` files using the **free Google Translate API** — no API key required.

---

## ✨ Features

- 🌍 Automatically translate `README.md` into **10+ languages**.
- 🔒 Protects code blocks, inline code, and URLs from being translated.
- 💬 Adds a language switcher block (`🌐 Available in other languages: [Bahasa Indonesia](docs/lang/README-ID.md)`)
- 💾 Allows optional **custom API key input** (e.g., Google Cloud, DeepL).
- 🧠 Uses built-in Google Translate (no account needed).
- ⚙️ Simple 1-click sidebar interface.

---

## ✅ Supported VS Code Versions

- Minimum version: **1.85.0**
- Tested on **Windows**, **macOS**, and **Linux**.

---

## 🧩 Installation

### From Marketplace (Recommended)

1.  Open **Visual Studio Code**.
2.  Go to the **Extensions** view (`Ctrl+Shift+X`).
3.  Search for `Auto Translate Readmes`.
4.  Click **Install**.

### For Development (from Source Code)

1.  Clone this repository:
    ```bash
    git clone [https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git)
    cd Auto-Translate-Readmes
    npm install
    ```
2.  Open the folder in VS Code.
3.  Press **F5** to launch the **Extension Development Host**.
4.  In the new window, open your project containing a `README.md`.
5.  Open the sidebar → click **⚙️ Generate Multilingual READMEs**.

---

## ⌨️ Commands & Shortcuts

| Command Name                  | Command ID                   | Shortcut |
| ----------------------------- | ---------------------------- | -------- |
| Generate Multilingual READMEs | `auto-translate-readmes.run` | _N/A_    |

---

## 🧠 Example

**Before:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**After (Translated):**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

---

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

---

## 🧠 Sidebar Interface

The sidebar allows you to:

- 🗝️ Enter and save your own API key (optional)
- ⚙️ Click a single button to generate all translated README files
- 📁 Output stored in `docs/lang/` folder

---

## 🛠️ Development

Compile TypeScript:

```bash
npm run compile
```

Lint code:

```bash
npm run lint
```

Run tests:

```bash
npm test
```

---

## 🧑‍💻 Contributing

1. Fork the repository.
2. Run `npm install` to install dependencies.
3. Make your changes.
4. Compile TypeScript: `npm run compile`.
5. Test in VS Code (press **F5** → Extension Development Host).
6. Submit a Pull Request.

---

## 🐞 Bugs & Issues

Report issues on the [GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

---

## 🧾 Changelog

See all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.

> 📦 You can also view release notes directly on the [GitHub Releases page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/releases).

---

## 🧾 License

MIT License © [Fatony Ahmad Fauzi](LICENSE)
