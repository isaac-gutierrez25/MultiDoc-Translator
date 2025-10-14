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

> 🌐 Disponible dans d'autres langues : [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

Extension Visual Studio Code qui génère automatiquement des fichiers `README.md` multilingues à l'aide de l'**API gratuite de Google Translate** — aucune clé API requise.
- --

## ✨ Caractéristiques
- 🌍 Traduisez automatiquement `README.md` en **10+ langues**.
- 🔒 Protège les blocs de code, le code en ligne et les URL contre la traduction.
- 💬 Ajoute automatiquement un bloc de changement de langue (`🌐 Available in other languages:`).
- 💾 Permet la **saisie facultative de clé API personnalisée** (par exemple, Google Cloud, DeepL).
- 🧠 Utilise Google Translate intégré (aucun compte requis).
- ⚙️ Interface de barre latérale simple en 1 clic.
- --

## ✅ Versions de code VS prises en charge
- Version minimale : **1.85.0**
- Testé sur **Windows**, **macOS** et **Linux**.
- --

## 🧩Installation

1. Clonez ou téléchargez ce référentiel :
```bash
   git clone https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git
   cd Auto-Translate-Readmes
   npm install
   ```
2. Ouvrez le dossier dans VS Code.
3. Appuyez sur **F5** pour lancer **Extension Development Host**.
4. Ouvrez votre projet contenant un `README.md`.
5. Ouvrez la barre latérale → cliquez sur **⚙️ Générer des README multilingues**.
- --

## ⌨️ Commandes et raccourcis

|Nom de la commande |ID de commande |Raccourci |
| ----------------------------- | ---------------------------- |-------- |
|Générer des README multilingues |`auto-translate-readmes.run` |_N/A_ |
- --

## 🧠 Exemple
- *Avant:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```
- *Après (traduit) :**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)
- --

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```
- --

## 🧠 Interface de la barre latérale

La barre latérale vous permet de :
- 🗝️ Entrez et enregistrez votre propre clé API (facultatif)
- ⚙️ Cliquez sur un seul bouton pour générer tous les fichiers README traduits
- 📁 Sortie stockée dans le dossier `docs/lang/`
- --

## 🛠️ Développement

Compiler TypeScript :

```bash
npm run compile
```

Code charpie :

```bash
npm run lint
```

Exécutez des tests :

```bash
npm test
```
- --

## 🧑‍💻 Contribuer

1. Forkez le référentiel.
2. Exécutez `npm install` pour installer les dépendances.
3. Effectuez vos modifications.
4. Compilez TypeScript : `npm run compile`.
5. Testez dans VS Code (appuyez sur **F5** → Extension Development Host).
6. Soumettez une demande de tirage.
- --

## 🐞 Bogues et problèmes

Signalez les problèmes sur [GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).
- --

## 🧾 Licence

Licence MIT © [Fatony Ahmad Fauzi](../../LICENSE)
