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

> 🌐 提供其他语言版本： [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

一个 Visual Studio Code 扩展，可使用 **免费的 Google Translate API** 自动生成多语言 `README.md` 文件 - 无需 API 密钥。

- --

## ✨ 特点

- 🌍 自动将 `README.md` 翻译成 **10 多种语言**。
- 🔒 保护代码块、内联代码和 URL 不被翻译。
- 💬 自动添加语言切换块（`🌐 Available in other languages:`）。
- 💾 允许可选的**自定义 API 密钥输入**（例如 Google Cloud、DeepL）。
- 🧠 使用内置谷歌翻译（无需帐户）。
- ⚙️ 简单的一键侧边栏界面。

- --

## ✅ 支持的 VS Code 版本

- 最低版本：**1.85.0**
- 在 **Windows**、**macOS** 和 **Linux** 上测试。

- --

## 🧩 安装

1. 克隆或下载此存储库：
```bash
   git clone https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git
   cd Auto-Translate-Readmes
   npm install
   ```
2. 在 VS Code 中打开该文件夹。
3. 按 **F5** 启动 **扩展开发主机**。
4. 打开包含 `README.md` 的项目。
5. 打开侧边栏 → 单击 **⚙️ 生成多语言自述文件**。

- --

## ⌨️ 命令和快捷键

|命令名称 |命令ID |快捷方式 |
|-------------------------------------- |---------------------------- |-------- |
|生成多语言自述文件 |`auto-translate-readmes.run` |_不适用_ |

- --

## 🧠 示例

**前：**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**之后（翻译）：**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

- --

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

- --

## 🧠 侧边栏界面

侧边栏允许您：

- 🗝️ 输入并保存您自己的 API 密钥（可选）
- ⚙️ 单击一个按钮即可生成所有翻译的自述文件
- 📁 输出存储在 `docs/lang/` 文件夹中

- --

## 🛠️ 发展

编译打字稿：

```bash
npm run compile
```

皮棉代码：

```bash
npm run lint
```

运行测试：

```bash
npm test
```

- --

## 🧑‍💻 贡献

1. 分叉存储库。
2. 运行`npm install`安装依赖项。
3. 做出改变。
4. 编译 TypeScript：`npm run compile`。
5. 在 VS Code 中测试（按 **F5** → 扩展开发主机）。
6. 提交拉取请求。

- --

## 🐞 错误和问题

在[GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues)上报告问题。

- --

## 🧾 许可证

麻省理工学院许可证 © [Fatony Ahmad Fauzi](../../LICENSE)
