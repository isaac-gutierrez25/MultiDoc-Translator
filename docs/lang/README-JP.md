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

> 🌐 他の言語でも利用可能: [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

**無料の Google Translate API** を使用して多言語の `README.md` ファイルを自動的に生成する Visual Studio Code 拡張機能 — API キーは必要ありません。

---

## ✨ 特徴

- 🌍 `README.md` を **10 以上の言語**に自動的に翻訳します。
- 🔒 コード ブロック、インライン コード、URL が翻訳されないように保護します。
- 💬 言語切り替えブロック (`🌐 Available in other languages:`) を自動的に追加します。
- 💾 オプションの **カスタム API キー入力** (例: Google Cloud、DeepL) を許可します。
- 🧠 内蔵の Google 翻訳を使用します (アカウントは必要ありません)。
- ⚙️ シンプルな 1 クリックのサイドバー インターフェイス。

---

## ✅ サポートされている VS コードのバージョン

- 最小バージョン: **1.85.0**
- **Windows**、**macOS**、**Linux** でテスト済み。

---

## 🧩 インストール

1. このリポジトリを複製またはダウンロードします。

```bash
   git clone https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git
   cd Auto-Translate-Readmes
   npm install
```

2. VS Code でフォルダーを開きます。
3. **F5** を押して **Extension Development Host** を起動します。
4. `README.md` を含むプロジェクトを開きます。
5. サイドバーを開き、[**⚙️ 多言語 README の生成**] をクリックします。

---

## ⌨️ コマンドとショートカット

| コマンド名                 | コマンド ID                  | ショートカット |
| -------------------------- | ---------------------------- | -------------- |
| 多言語の README を生成する | `auto-translate-readmes.run` | _該当なし_     |

---

## 🧠 例

**前に：**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**後（翻訳後）：**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

---

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

---

## 🧠 サイドバーインターフェイス

サイドバーを使用すると、次のことができます。

- 🗝️ 独自の API キーを入力して保存します (オプション)
- ⚙️ ボタン 1 つをクリックすると、翻訳されたすべての README ファイルが生成されます
- 📁 出力は `docs/lang/` フォルダーに保存されます

---

## 🛠️ 開発

TypeScript をコンパイルします。

```bash
npm run compile
```

lint コード:

```bash
npm run lint
```

テストを実行します。

```bash
npm test
```

---

## 🧑‍💻 貢献しています

1. リポジトリをフォークします。
2. `npm install` を実行して依存関係をインストールします。
3. 変更を加えます。
4. TypeScript をコンパイルします: `npm run compile`。
5. VS Code でテストします (**F5** を押して → 拡張機能開発ホスト)。
6. プルリクエストを送信します。

---

## 🐞 バグと問題

[GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues) で問題を報告してください。

---

## 🧾 ライセンス

MIT ライセンス © [Fatony Ahmad Fauzi](../../LICENSE)
