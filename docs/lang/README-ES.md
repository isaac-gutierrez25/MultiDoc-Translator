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

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

Una extensión de Visual Studio Code que genera automáticamente archivos `README.md` multilingües utilizando la **API gratuita de Google Translate**; no se requiere clave API.

- --

## ✨ Características

- 🌍 Traducir automáticamente `README.md` a **más de 10 idiomas**.
- 🔒 Protege bloques de código, código en línea y URL para que no se traduzcan.
- 💬 Agrega un bloque de cambio de idioma (`🌐 Available in other languages:`) automáticamente.
- 💾 Permite **entrada de clave API personalizada** opcional (por ejemplo, Google Cloud, DeepL).
- 🧠 Utiliza el Traductor de Google integrado (no se necesita cuenta).
- ⚙️ Interfaz de barra lateral sencilla con 1 clic.

- --

## ✅ Versiones de código VS compatibles

- Versión mínima: **1.85.0**
- Probado en **Windows**, **macOS** y **Linux**.

- --

## 🧩 Instalación

1. Clona o descarga este repositorio:
```bash
   git clone https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git
   cd Auto-Translate-Readmes
   npm install
   ```
2. Abra la carpeta en VS Code.
3. Presione **F5** para iniciar el **Host de desarrollo de extensiones**.
4. Abra su proyecto que contiene `README.md`.
5. Abra la barra lateral → haga clic en **⚙️ Generar archivos LÉAME multilingües**.

- --

## ⌨️ Comandos y atajos

|Nombre del comando |ID de comando |Atajo |
|----------------------- |---------------------------- |-------- |
|Generar archivos README multilingües |`auto-translate-readmes.run` |_N/A_ |

- --

## 🧠 Ejemplo

**Antes:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**Después (Traducido):**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

- --

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

- --

## 🧠 Interfaz de la barra lateral

La barra lateral le permite:

- 🗝️ Ingresa y guarda tu propia clave API (opcional)
- ⚙️ Haga clic en un solo botón para generar todos los archivos LÉAME traducidos
- 📁 Salida almacenada en la carpeta `docs/lang/`

- --

## 🛠️ Desarrollo

Compilar TypeScript:

```bash
npm run compile
```

Código de pelusa:

```bash
npm run lint
```

Ejecutar pruebas:

```bash
npm test
```

- --

## 🧑‍💻 Contribuyendo

1. Bifurque el repositorio.
2. Ejecute `npm install` para instalar dependencias.
3. Realice sus cambios.
4. Compile TypeScript: `npm run compile`.
5. Pruebe en VS Code (presione **F5** → Host de desarrollo de extensiones).
6. Envíe una solicitud de extracción.

- --

## 🐞 Errores y problemas

Informar problemas en [GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

- --

## 🧾 Licencia

Licencia MIT © [Fatony Ahmad Fauzi](../../LICENSE)
