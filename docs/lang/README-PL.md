# 🌍 Auto Translate Readmes

[![VS Code](https://img.shields.io/badge/VS%20Code-1.85.0+-blue.svg)](https://code.visualstudio.com/)
[![Version](https://img.shields.io/github/v/release/fatonyahmadfauzi/Auto-Translate-Readmes?color=blue.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/releases)
[![License: MIT](https://img.shields.io/github/license/fatonyahmadfauzi/Auto-Translate-Readmes?color=green.svg)](../../LICENSE)
[![Build Status](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/actions/workflows/main.yml/badge.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/actions)
[![Repo Size](https://img.shields.io/github/repo-size/fatonyahmadfauzi/Auto-Translate-Readmes?color=yellow.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes)
[![Last Commit](https://img.shields.io/github/last-commit/fatonyahmadfauzi/Auto-Translate-Readmes?color=brightgreen.svg)](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/commits/main)
[![Installs](https://vsmarketplacebadges.dev/installs-short/fatonyahmadfauzi.auto-translate-readmes.svg)](https://marketplace.visualstudio.com/items?itemName=fatonyahmadfauzi.auto-translate-readmes)
[![Downloads](https://vsmarketplacebadges.dev/downloads-short/fatonyahmadfauzi.auto-translate-readmes.svg)](https://marketplace.visualstudio.com/items?itemName=fatonyahmadfauzi.auto-translate-readmes)
[![Rating](https://vsmarketplacebadges.dev/rating-short/fatonyahmadfauzi.auto-translate-readmes.svg)](https://marketplace.visualstudio.com/items?itemName=fatonyahmadfauzi.auto-translate-readmes)

> 🌐 Dostępne w innych językach: [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

Rozszerzenie Visual Studio Code, które automatycznie generuje wielojęzyczne pliki `README.md` przy użyciu **bezpłatnego interfejsu API Tłumacza Google** — nie jest wymagany żaden klucz API.

---

## ✨ Funkcje

- 🌍 Automatycznie przetłumacz `README.md` na **ponad 10 języków**.
- 🔒 Chroni bloki kodu, kod wbudowany i adresy URL przed tłumaczeniem.
- 💬 Dodaje blok zmiany języka (`🌐 Available in other languages: [Bahasa Indonesia](docs/lang/README-ID.md)`)
- 💾 Umożliwia opcjonalne **wprowadzanie niestandardowego klucza API** (np. Google Cloud, DeepL).
- 🧠 Korzysta z wbudowanego Tłumacza Google (nie wymaga konta).
- ⚙️ Prosty interfejs paska bocznego jednym kliknięciem.

---

## ✅ Obsługiwane wersje kodu VS

- Wersja minimalna: **1.85.0**
- Testowano na **Windows**, **macOS** i **Linux**.

---

## 🧩 Instalacja

### Z Marketplace (zalecane)

1. Otwórz **Kod Visual Studio**.
2. Przejdź do widoku **Rozszerzenia** (`Ctrl+Shift+X`).
3. Wyszukaj `Auto Translate Readmes`.
4. Kliknij **Zainstaluj**.

### Dla rozwoju (z kodu źródłowego)

1. Sklonuj to repozytorium:
    ```bash
    git clone [https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git)
    cd Auto-Translate-Readmes
    npm install
    ```
2. Otwórz folder w VS Code.
3. Naciśnij **F5**, aby uruchomić **Host rozwoju rozszerzeń**.
4. W nowym oknie otwórz projekt zawierający plik `README.md`.
5. Otwórz pasek boczny → kliknij **⚙️ Generuj wielojęzyczne pliki README**.

---

## ⌨️ Polecenia i skróty

| Nazwa polecenia | Identyfikator polecenia | Skrót |
| ----------------------------- | ---------------------------- | -------- |
| Generate Multilingual READMEs | `auto-translate-readmes.run` | _N/A_    |

---

## 🧠 Przykład

**Zanim:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**Po (przetłumaczone):**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

---

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

---

## 🧠 Interfejs paska bocznego

Pasek boczny umożliwia:

- 🗝️ Wprowadź i zapisz własny klucz API (opcjonalnie)
- ⚙️ Kliknij jeden przycisk, aby wygenerować wszystkie przetłumaczone pliki README
- 📁 Dane wyjściowe zapisane w folderze `docs/lang/`

---

## 🛠️Rozwój

Kompiluj TypeScript:

```bash
npm run compile
```

Lint kod:

```bash
npm run lint
```

Uruchom testy:

```bash
npm test
```

---

## 🧑‍💻 Współtworzenie

1. Forkuj repozytorium.
2. Uruchom `npm install`, aby zainstalować zależności.
3. Wprowadź zmiany.
4. Skompiluj TypeScript: `npm run compile`.
5. Przetestuj kod VS (naciśnij **F5** → Host rozwoju rozszerzenia).
6. Prześlij żądanie ściągnięcia.

---

## 🐞 Błędy i problemy

Zgłaszaj problemy na [stronie problemów z GitHubem](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

---

## 🧾 Licencja

MIT License © [Fatony Ahmad Fauzi](../../LICENSE)
