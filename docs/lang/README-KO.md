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

> 🌐 다른 언어로도 사용 가능: [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [Português](README-PT.md)

---

- *무료 Google Translate API**를 사용하여 다국어 `README.md` 파일을 자동으로 생성하는 Visual Studio Code 확장입니다. API 키가 필요하지 않습니다.
- --

## ✨ 특징
- 🌍 `README.md`을 **10개 이상의 언어**로 자동 번역합니다.
- 🔒 코드 블록, 인라인 코드 및 URL이 번역되지 않도록 보호합니다.
- 💬 언어 전환기 블록(`🌐 Available in other languages:`)을 자동으로 추가합니다.
- 💾 선택적 **맞춤 API 키 입력**(예: Google Cloud, DeepL)을 허용합니다.
- 🧠 내장된 Google 번역을 사용합니다(계정이 필요하지 않음).
- ⚙️ 간단한 원클릭 사이드바 인터페이스.
- --

## ✅ 지원되는 VS 코드 버전
- 최소 버전: **1.85.0**
- **Windows**, **macOS** 및 **Linux**에서 테스트되었습니다.
- --

## 🧩 설치

1. 다음 저장소를 복제하거나 다운로드합니다.
```bash
   git clone https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git
   cd Auto-Translate-Readmes
   npm install
   ```
2. VS Code에서 폴더를 엽니다.
3. **F5**를 눌러 **확장 개발 호스트**를 시작합니다.
4. `README.md`이 포함된 프로젝트를 엽니다.
5. 사이드바를 열고 → **⚙️ 다국어 README 생성**을 클릭합니다.
- --

## ⌨️ 명령 및 단축키

|명령 이름 |명령 ID |바로가기 |
| ----------------------------- | ---------------------------- |-------- |
|다국어 README 생성 |`auto-translate-readmes.run` |_N/A_ |
- --

## 🧠 예
- *전에:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```
- *이후(번역됨):**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)
- --

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```
- --

## 🧠 사이드바 인터페이스

사이드바를 사용하면 다음을 수행할 수 있습니다.
- 🗝️ 자신의 API 키를 입력하고 저장하세요(선택 사항).
- ⚙️ 번역된 모든 README 파일을 생성하려면 버튼 하나만 클릭하세요.
- 📁 출력은 `docs/lang/` 폴더에 저장됩니다.
- --

## 🛠️ 개발

TypeScript 컴파일:

```bash
npm run compile
```

린트 코드:

```bash
npm run lint
```

테스트 실행:

```bash
npm test
```
- --

## 🧑‍💻 기여

1. 저장소를 포크하십시오.
2. `npm install`을 실행하여 종속성을 설치합니다.
3. 변경합니다.
4. TypeScript를 컴파일합니다: `npm run compile`.
5. VS Code에서 테스트합니다(**F5** → 확장 개발 호스트 누르기).
6. 풀 요청(Pull Request)을 제출하세요.
- --

## 🐞 버그 및 문제

[GitHub Issues page](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues)에서 문제를 신고하세요.
- --

## 🧾 라이센스

MIT 라이센스 © [Fatony Ahmad Fauzi](../../LICENSE)
