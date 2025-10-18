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

> 🌐 Tersedia dalam bahasa lain: [English](../../README.md) | [Français](README-FR.md) | [Deutsch](README-DE.md) | [日本語](README-JP.md) | [中文](README-ZH.md) | [Español](README-ES.md) | [Polski](README-PL.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [한국어](README-KO.md)

---

Ekstensi Visual Studio Code yang secara otomatis menghasilkan file `README.md` multibahasa menggunakan **API Google Terjemahan gratis** — tidak memerlukan kunci API.

---

## ✨ Fitur

- 🌍 Terjemahkan `README.md` secara otomatis ke **10+ bahasa**.
- 🔒 Melindungi blok kode, kode sebaris, dan URL agar tidak diterjemahkan.
- 💬 Menambahkan blok pengalih bahasa (`🌐 Available in other languages: [Bahasa Indonesia](docs/lang/README-ID.md)`)
- 💾 Mengizinkan **input kunci API khusus** opsional (misalnya, Google Cloud, DeepL).
- 🧠 Menggunakan Google Terjemahan bawaan (tidak perlu akun).
- ⚙️ Antarmuka sidebar 1-klik yang sederhana.

---

## ✅ Versi VS Code yang Didukung

- Versi minimum : **1.85.0**
- Diuji pada **Windows**, **macOS**, dan **Linux**.

---

## 🧩 Instalasi

### Dari Marketplace (Disarankan)

1. Buka **Kode Visual Studio**.
2. Buka tampilan **Ekstensi** (`Ctrl+Shift+X`).
3. Cari `Auto Translate Readmes`.
4. Klik **Instal**.

### Untuk Pengembangan (dari Kode Sumber)

1. Kloning repositori ini:
    ```bash
    git clone [https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes.git)
    cd Auto-Translate-Readmes
    npm install
    ```
2. Buka folder di VS Code.
3. Tekan **F5** untuk meluncurkan **Extension Development Host**.
4. Di jendela baru, buka proyek Anda yang berisi `README.md`.
5. Buka sidebar → klik **⚙️ Hasilkan README Multibahasa**.

---

## ⌨️ Perintah & Pintasan

| Nama Perintah | ID Perintah | Jalan pintas |
| ----------------------------- | ---------------------------- | -------- |
| Generate Multilingual READMEs | `auto-translate-readmes.run` | _N/A_    |

---

## 🧠 Contoh

**Sebelum:**

```md
# My Awesome Extension

A simple extension to help developers write better code.
```

**Setelah (Diterjemahkan):**

```md
# My Awesome Extension

> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Deutsch](README-DE.md) | [Français](README-FR.md)

---

Une extension Visual Studio Code qui aide les développeurs à mieux écrire du code.
```

---

## 🧠 Antarmuka Bilah Sisi

Bilah samping memungkinkan Anda untuk:

- 🗝️ Masukkan dan simpan kunci API Anda sendiri (opsional)
- ⚙️ Klik satu tombol untuk menghasilkan semua file README yang diterjemahkan
- 📁 Output disimpan di folder `docs/lang/`

---

## 🛠️ Perkembangan

Kompilasi TypeScript:

```bash
npm run compile
```

Lint kode:

```bash
npm run lint
```

Jalankan tes:

```bash
npm test
```

---

## 🧑‍💻 Berkontribusi

1. Cabangkan repositori.
2. Jalankan `npm install` untuk menginstal dependensi.
3. Lakukan perubahan Anda.
4. Kompilasi TypeScript: `npm run compile`.
5. Uji di VS Code (tekan **F5** → Extension Development Host).
6. Kirim Permintaan Tarik.

---

## 🐞 Bug & Masalah

Laporkan masalah di [halaman Masalah GitHub](https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/issues).

---

## 🧾 Lisensi

MIT License © [Fatony Ahmad Fauzi](../../LICENSE)
