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

> 🌐 Disponível em outros idiomas: [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [한국어](README-KO.md)

---

Extensão do Visual Studio Code que gera automaticamente arquivos `README.md` multilíngues usando **free Google Translate API** — nenhuma chave de API é necessária.

---

## ✨ Recursos

- 🌍 Traduza automaticamente `README.md` em **10+ languages**.
- 🔒 Protege blocos de código, código embutido e URLs contra tradução.
- 💬 Adiciona um bloco de alternância de idioma (`🌐 Available in other languages:`) automaticamente.
- 💾 Permite **custom API key input** opcional (por exemplo, Google Cloud, DeepL).
- 🧠 Usa Google Translate integrado (não é necessária conta).
- ⚙️ Interface simples da barra lateral com 1 clique.

---

## ✅ Versões de código VS suportadas

- Versão mínima: **1.85.0**
- Testado em **Windows**, **macOS** e **Linux**.

---

## 🧩 Instalação

### Do Marketplace (recomendado)

1. Abra **Visual Studio Code**.
2. Vá para a visualização **Extensions** (`Ctrl+Shift+X`).
3. Pesquise `Auto Translate Readmes`.
4. Clique em **Install**.

### Para Desenvolvimento (do Código Fonte)

1. Clone este repositório:
    ```bash
    git clone [https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git)
    cd Auto-Translate-Readmes
    npm install
    ```
2. Abra a pasta no VS Code.
3. Pressione **F5** para iniciar o **Extension Development Host**.
4. Na nova janela, abra seu projeto contendo um `README.md`.
5. Abra a barra lateral → clique em **⚙️ Generate Multilingual READMEs**.

---

## ⌨️ Comandos e atalhos

| Nome do comando | ID do comando | Atalho |
| ----------------------------- | ---------------------------- | -------- |
| Gere READMEs multilíngues | `auto-translate-readmes.run` | _N/A_ |

---

## 🧠 Exemplo

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

## 🧠 Interface da barra lateral

A barra lateral permite que você:

- 🗝️ Insira e salve sua própria chave API (opcional)
- ⚙️ Clique em um único botão para gerar todos os arquivos README traduzidos
- 📁 Saída armazenada na pasta `docs/lang/`

---

## 🛠️ Desenvolvimento

Compilar TypeScript:

```bash
npm run compile
```

Código Lint:

```bash
npm run lint
```

Execute testes:

```bash
npm test
```

---

## 🧑‍💻 Contribuindo

1. Bifurque o repositório.
2. Execute `npm install` para instalar dependências.
3. Faça suas alterações.
4. Compilar TypeScript: `npm run compile`.
5. Teste no VS Code (pressione **F5** → Host de desenvolvimento de extensão).
6. Envie uma solicitação pull.

---

## 🐞 Bugs e problemas

Relate problemas no [GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

---

## 🧾 Licença

MINHA Licença © [Fatony Ahmad Fauzi](../../LICENSE)
