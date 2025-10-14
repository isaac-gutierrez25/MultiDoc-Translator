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

> 🌐 In anderen Sprachen verfügbar: [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

Eine Visual Studio Code-Erweiterung, die mithilfe der **kostenlosen Google Translate-API** automatisch mehrsprachige `README.md`-Dateien generiert – kein API-Schlüssel erforderlich.

- --

## ✨ Funktionen

- 🌍 Übersetzen Sie `README.md` automatisch in **10+ Sprachen**.
- 🔒 Schützt Codeblöcke, Inline-Code und URLs vor der Übersetzung.
- 💬 Fügt automatisch einen Sprachumschaltblock (`🌐 Available in other languages:`) hinzu.
- 💾 Ermöglicht optionale **benutzerdefinierte API-Schlüsseleingabe** (z. B. Google Cloud, DeepL).
- 🧠 Verwendet das integrierte Google Translate (kein Konto erforderlich).
- ⚙️ Einfache 1-Klick-Seitenleistenoberfläche.

- --

## ✅ Unterstützte VS-Codeversionen

- Mindestversion: **1.85.0**
- Getestet unter **Windows**, **macOS** und **Linux**.

- --

## 🧩 Installation

1. Klonen Sie dieses Repository oder laden Sie es herunter:
```bash
   git clone https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git
   cd Auto-Translate-Readmes
   npm install
   ```
2. Öffnen Sie den Ordner in VS Code.
3. Drücken Sie **F5**, um den **Extension Development Host** zu starten.
4. Öffnen Sie Ihr Projekt, das ein `README.md` enthält.
5. Öffnen Sie die Seitenleiste → klicken Sie auf **⚙️ Mehrsprachige READMEs generieren**.

- --

## ⌨️ Befehle und Verknüpfungen

|Befehlsname |Befehls-ID |Verknüpfung |
|-------------- |------------- |-------- |
|Generieren Sie mehrsprachige READMEs |`auto-translate-readmes.run` |_N/A_ |

- --

## 🧠 Beispiel

**Vor:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**Nachher (übersetzt):**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

- --

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

- --

## 🧠 Seitenleistenoberfläche

Mit der Seitenleiste können Sie:

- 🗝️ Geben Sie Ihren eigenen API-Schlüssel ein und speichern Sie ihn (optional)
- ⚙️ Klicken Sie auf eine einzelne Schaltfläche, um alle übersetzten README-Dateien zu generieren
- 📁 Ausgabe im Ordner `docs/lang/` gespeichert

- --

## 🛠️ Entwicklung

TypeScript kompilieren:

```bash
npm run compile
```

Lint-Code:

```bash
npm run lint
```

Führen Sie Tests durch:

```bash
npm test
```

- --

## 🧑‍💻 Mitwirken

1. Forken Sie das Repository.
2. Führen Sie `npm install` aus, um Abhängigkeiten zu installieren.
3. Nehmen Sie Ihre Änderungen vor.
4. TypeScript kompilieren: `npm run compile`.
5. Testen Sie im VS-Code (drücken Sie **F5** → Extension Development Host).
6. Senden Sie eine Pull-Anfrage.

- --

## 🐞 Fehler und Probleme

Melden Sie Probleme auf dem [GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

- --

## 🧾 Lizenz

MIT-Lizenz © [Fatony Ahmad Fauzi](../../LICENSE)
