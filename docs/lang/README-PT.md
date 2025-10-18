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

Extensão do Visual Studio Code que gera automaticamente arquivos `README.md` multilíngues usando a **API gratuita do Google Translate** — sem necessidade de chave de API.

---

## ✨ Recursos

- 🌍 Traduzir automaticamente `README.md` para **mais de 10 idiomas**.
- 🔒 Protege blocos de código, código embutido e URLs contra tradução.
- 💬 Adiciona um bloco de alternância de idioma (`🌐 Available in other languages: [Bahasa Indonesia](docs/lang/README-ID.md)`)
- 💾 Permite **entrada opcional de chave de API personalizada** (por exemplo, Google Cloud, DeepL).
- 🧠 Usa Google Translate integrado (não é necessária conta).
- ⚙️ Interface simples da barra lateral com 1 clique.

---

## ✅ Versões de código VS suportadas

- Versão mínima: **1.85.0**
- Testado em **Windows**, **macOS** e **Linux**.

---

## 🧩 Instalação

### Do Marketplace (recomendado)

1. Abra **Código do Visual Studio**.
2. Vá para a visualização **Extensões** (`Ctrl+Shift+X`).
3. Pesquise `Auto Translate Readmes`.
4. Clique em **Instalar**.

### Para Desenvolvimento (do Código Fonte)

1. Clone este repositório:
    ```bash
    git clone [https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git)
    cd Auto-Translate-Readmes
    npm install
    ```
2. Abra a pasta no VS Code.
3. Pressione **F5** para iniciar o **Host de desenvolvimento de extensão**.
4. Na nova janela, abra seu projeto contendo um `README.md`.
5. Abra a barra lateral → clique em **⚙️ Gerar READMEs multilíngues**.

---

## ⌨️ Comandos e atalhos

| Nome do Comando | ID do comando | Atalho |
| ----------------------------- | ---------------------------- | -------- |
| Generate Multilingual READMEs | `auto-translate-readmes.run` | _N/A_    |

---

## 🧠 Exemplo

**Antes:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**Depois (traduzido):**

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

Lint código:

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
4. Compile TypeScript: `npm run compile`.
5. Teste no VS Code (pressione **F5** → Host de desenvolvimento de extensão).
6. Envie uma solicitação pull.

---

## 🐞 Bugs e problemas

Relate problemas na [página de problemas do GitHub](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

---

## 🧾 Licença

MIT License © [Fatony Ahmad Fauzi](../../LICENSE)
