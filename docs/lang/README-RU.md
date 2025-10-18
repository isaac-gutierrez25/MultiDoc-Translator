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

> 🌐 Доступно на других языках: [English](../../README.md) | [Bahasa Indonesia](README-ID.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

Расширение Visual Studio Code, которое автоматически генерирует многоязычные файлы `README.md` с помощью **бесплатного API Google Translate** — ключ API не требуется.

---

## ✨ Особенности

- 🌍 Автоматически переводить `README.md` на **более 10 языков**.
- 🔒 Защищает блоки кода, встроенный код и URL-адреса от перевода.
- 💬 Добавляет блок переключения языка (`🌐 Available in other languages: [Bahasa Indonesia](docs/lang/README-ID.md)`)
- 💾 Позволяет дополнительный **ввод пользовательских ключей API** (например, Google Cloud, DeepL).
- 🧠 Использует встроенный Google Translate (учетная запись не требуется).
- ⚙️ Простой интерфейс боковой панели в 1 клик.

---

## ✅ Поддерживаемые версии кода VS

- Минимальная версия : **1.85.0**
- Протестировано на **Windows**, **macOS** и **Linux**.

---

## 🧩 Установка

### Из торговой площадки (рекомендуется)

1. Откройте **Код Visual Studio**.
2. Перейдите в представление **Расширения** (`Ctrl+Shift+X`).
3. Найдите `Auto Translate Readmes`.
4. Нажмите **Установить**.

### Для разработки (из исходного кода)

1. Клонируйте этот репозиторий:
    ```bash
    git clone [https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git)
    cd Auto-Translate-Readmes
    npm install
    ```
2. Откройте папку в VS Code.
3. Нажмите **F5**, чтобы запустить **Хост разработки расширений**.
4. В новом окне откройте проект, содержащий файл `README.md`.
5. Откройте боковую панель → нажмите **⚙️ Создать многоязычные файлы README**.

---

## ⌨️ Команды и сочетания клавиш

| Имя команды | Идентификатор команды | Ярлык |
| ----------------------------- | ---------------------------- | -------- |
| Generate Multilingual READMEs | `auto-translate-readmes.run` | _N/A_    |

---

## 🧠 Пример

**До:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**После (переведено):**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

---

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

---

## 🧠 Интерфейс боковой панели

Боковая панель позволяет:

- 🗝️ Введите и сохраните свой собственный ключ API (необязательно).
- ⚙️ Нажмите одну кнопку, чтобы создать все переведенные файлы README.
- 📁 Вывод хранится в папке `docs/lang/`.

---

## 🛠️ Развитие

Скомпилируйте TypeScript:

```bash
npm run compile
```

Lint код:

```bash
npm run lint
```

Запустите тесты:

```bash
npm test
```

---

## 🧑‍💻 Вносим вклад

1. Форкните репозиторий.
2. Запустите `npm install` для установки зависимостей.
3. Внесите изменения.
4. Скомпилируйте TypeScript: `npm run compile`.
5. Протестируйте в VS Code (нажмите **F5** → Хост разработки расширений).
6. Отправьте запрос на включение.

---

## 🐞 Ошибки и проблемы

Сообщайте о проблемах на [странице проблем GitHub](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

---

## 🧾 Лицензия

MIT License © [Фатони Ахмад Фаузи](../../LICENSE)
