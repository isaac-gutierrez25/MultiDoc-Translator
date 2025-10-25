#!/usr/bin/env python3
"""
MultiDoc Translator - Automated multi-language documentation translator
Support for README.md and CHANGELOG.md translation with protection features
"""

import os
import re
import json
import time
import argparse
import shutil
import sys
from deep_translator import GoogleTranslator
from tqdm import tqdm

SOURCE_FILE = "README.md"
CHANGELOG_FILE = "CHANGELOG.md"
PACKAGE_JSON = "package.json"
OUTPUT_DIR = "docs/lang"
PROTECTED_FILE = "protected_phrases.json"
PROTECT_STATUS_FILE = ".protect_status"

# ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------
DISPLAY_LANGUAGES = {
    "en": {
        "translating_readme": "📘 Translating README to {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} successfully created",
        "translating_changelog": "📘 Translating CHANGELOG to {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} successfully created",
        "changelog_links_updated": "✅ Changelog links updated in {filename}",
        "all_translated": "🎉 All READMEs successfully translated!",
        "language_switcher_updated": "✅ Language switcher in {filename} updated",
        "file_deleted": "🗑️ File {filename} successfully deleted",
        "folder_deleted": "🗑️ Folder {folder} successfully deleted",
        "changelog_section_added": "✅ Changelog section added to README.md with proper spacing and separators",
        "changelog_spacing_fixed": "✅ Fixed changelog section spacing and separators in README.md",
        "github_url_detected": "🔍 GitHub Repository Detection Results:",
        "repo_url": "📦 Repository URL: {url}",
        "releases_url": "🚀 Releases URL: {url}",
        "sources_checked": "📋 Sources checked:",
        "no_github_url": "❌ Could not detect GitHub repository URL automatically.",
        "protection_reset": "🔁 File protected_phrases.json has been reset to default.",
        "phrase_added": "✅ Phrase '{phrase}' added to protection.",
        "phrase_removed": "🗑️ Phrase '{phrase}' removed from protection.",
        "protected_phrases_list": "📜 Protected phrases list:",
        "protection_enabled": "🟢 Protection enabled.",
        "protection_disabled": "🔴 Protection disabled.",
        "protection_status": "🧩 Protection status: {status}",
        "changelog_setup_completed": "✅ Changelog setup completed",
        "changelog_setup_failed": "❌ Changelog setup failed",
        "no_changelog_file": "❌ You don't have CHANGELOG.md file in root directory",
        "changelog_translated": "✅ Successfully translated CHANGELOG to {count} languages",
        "no_changelog_translated": "❌ No CHANGELOG files were successfully translated",
        "languages_removed": "🎉 Languages successfully removed: {langs}",
        "all_languages_removed": "🎉 All translation files successfully removed",
        "auto_setup_changelog": "🔧 Auto-setting up changelog section in README...",
        "checking_changelog_spacing": "🔧 Checking changelog section spacing...",
        "no_valid_language": "❌ No valid language codes provided.",
        "language_not_recognized": "❌ Language code '{code}' not recognized. Continuing...",
        "file_not_found": "⚠️ File {filename} not found",
        "folder_not_empty": "⚠️ Folder {folder} not empty, not deleted",
        "failed_delete_file": "❌ Failed to delete {filename}: {error}",
        "failed_delete_folder": "❌ Failed to delete folder: {error}",
        "failed_update_main": "❌ Failed to update main README: {error}",
        "failed_translate_changelog": "❌ Failed to translate CHANGELOG: {error}",
        "failed_update_changelog_links": "❌ Failed to update changelog links in {filename}: {error}",
        "failed_update_switcher": "❌ Failed to update language switcher in {filename}: {error}",
        "translation_failed": "❌ Translation failed: {error}",
        "reading_package_error": "❌ Error reading package.json: {error}",
        "reading_git_error": "❌ Error reading .git/config: {error}",
        "reading_github_error": "❌ Error searching GitHub URL in README: {error}",
        "changelog_section_exists": "ℹ️ Changelog section already exists in README.md",
        "no_changelog_file_root": "❌ No CHANGELOG.md file found in root directory",
        "no_translation_files": "ℹ️ No translated README files found",
        "language_not_supported": "⚠️ Display language '{code}' not supported, using default",
        "help_description": "MultiDoc Translator - Automated multi-language documentation translator",
        "help_epilog": """
Examples:
  # Translate README to Japanese and Chinese
  python multidoc_translator.py --lang jp,zh

  # Translate only CHANGELOG to all languages with Japanese notifications
  python multidoc_translator.py --translate-changelog all --display jp

  # Remove specific language files
  python multidoc_translator.py --remove-lang jp,zh

  # Auto setup changelog section in README
  python multidoc_translator.py --auto-setup-changelog

  # Detect GitHub repository URL
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Language codes to translate (comma-separated). Supported: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Remove specific translated language files (comma-separated)",
        "help_remove_all_lang": "Remove ALL translated language files and clean up folders",
        "help_add_protect": "Add a phrase to protection list (regex pattern supported)",
        "help_remove_protect": "Remove a phrase from protection list",
        "help_list_protect": "Show all currently protected phrases",
        "help_init_protect": "Reset protected_phrases.json to default values",
        "help_enable_protect": "Enable phrase protection during translation",
        "help_disable_protect": "Disable phrase protection during translation",
        "help_status_protect": "Check if phrase protection is currently enabled",
        "help_translate_changelog": "Translate only CHANGELOG.md (use 'all' for all languages or specify codes)",
        "help_auto_setup_changelog": "Automatically add changelog section to README.md if CHANGELOG.md exists",
        "help_detect_github_url": "Detect and display GitHub repository URL from various sources",
        "help_display": "Display language for terminal notifications (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "id": {
        "translating_readme": "📘 Menerjemahkan README ke {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} berhasil dibuat",
        "translating_changelog": "📘 Menerjemahkan CHANGELOG ke {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} berhasil dibuat",
        "changelog_links_updated": "✅ Link changelog diupdate di {filename}",
        "all_translated": "🎉 Semua README berhasil diterjemahkan!",
        "language_switcher_updated": "✅ Language switcher di {filename} diperbarui",
        "file_deleted": "🗑️ File {filename} berhasil dihapus",
        "folder_deleted": "🗑️ Folder {folder} berhasil dihapus",
        "changelog_section_added": "✅ Changelog section ditambahkan ke README.md dengan spacing dan pemisah yang benar",
        "changelog_spacing_fixed": "✅ Memperbaiki spacing dan pemisah section Changelog di README.md",
        "github_url_detected": "🔍 Hasil Deteksi Repository GitHub:",
        "repo_url": "📦 URL Repository: {url}",
        "releases_url": "🚀 URL Releases: {url}",
        "sources_checked": "📋 Sumber yang dicek:",
        "no_github_url": "❌ Tidak bisa mendeteksi URL repository GitHub secara otomatis.",
        "protection_reset": "🔁 File protected_phrases.json telah di-reset ke default.",
        "phrase_added": "✅ Frasa '{phrase}' ditambahkan ke proteksi.",
        "phrase_removed": "🗑️ Frasa '{phrase}' dihapus dari proteksi.",
        "protected_phrases_list": "📜 Daftar frasa yang diproteksi:",
        "protection_enabled": "🟢 Proteksi diaktifkan.",
        "protection_disabled": "🔴 Proteksi dinonaktifkan.",
        "protection_status": "🧩 Status proteksi: {status}",
        "changelog_setup_completed": "✅ Setup Changelog selesai",
        "changelog_setup_failed": "❌ Setup Changelog gagal",
        "no_changelog_file": "❌ Anda tidak memiliki file CHANGELOG.md di direktori root",
        "changelog_translated": "✅ Berhasil menerjemahkan CHANGELOG ke {count} bahasa",
        "no_changelog_translated": "❌ Tidak ada file CHANGELOG yang berhasil diterjemahkan",
        "languages_removed": "🎉 Bahasa berhasil dihapus: {langs}",
        "all_languages_removed": "🎉 Semua file bahasa terjemahan berhasil dihapus",
        "auto_setup_changelog": "🔧 Auto-setting up section changelog di README...",
        "checking_changelog_spacing": "🔧 Mengecek spacing section changelog...",
        "no_valid_language": "❌ Tidak ada kode bahasa yang valid.",
        "language_not_recognized": "❌ Kode bahasa '{code}' tidak dikenali. Dilanjutkan...",
        "file_not_found": "⚠️ File {filename} tidak ditemukan",
        "folder_not_empty": "⚠️ Folder {folder} tidak kosong, tidak dihapus",
        "failed_delete_file": "❌ Gagal menghapus {filename}: {error}",
        "failed_delete_folder": "❌ Gagal menghapus folder: {error}",
        "failed_update_main": "❌ Gagal update README utama: {error}",
        "failed_translate_changelog": "❌ Gagal menerjemahkan CHANGELOG: {error}",
        "failed_update_changelog_links": "❌ Gagal update link changelog di {filename}: {error}",
        "failed_update_switcher": "❌ Gagal update language switcher di {filename}: {error}",
        "translation_failed": "❌ Terjemahan gagal: {error}",
        "reading_package_error": "❌ Error membaca package.json: {error}",
        "reading_git_error": "❌ Error membaca .git/config: {error}",
        "reading_github_error": "❌ Error mencari URL GitHub di README: {error}",
        "changelog_section_exists": "ℹ️ Section Changelog sudah ada di README.md",
        "no_changelog_file_root": "❌ Tidak ada file CHANGELOG.md di direktori root",
        "no_translation_files": "ℹ️ Tidak ada file README terjemahan yang ditemukan",
        "language_not_supported": "⚠️ Bahasa display '{code}' tidak didukung, menggunakan default",
        "help_description": "MultiDoc Translator - Penerjemah dokumentasi multi-bahasa otomatis",
        "help_epilog": """
Contoh:
  # Terjemahkan README ke Jepang dan China
  python multidoc_translator.py --lang jp,zh

  # Hanya terjemahkan CHANGELOG ke semua bahasa dengan notifikasi Jepang
  python multidoc_translator.py --translate-changelog all --display jp

  # Hapus file bahasa tertentu
  python multidoc_translator.py --remove-lang jp,zh

  # Setup otomatis section changelog di README
  python multidoc_translator.py --auto-setup-changelog

  # Deteksi URL repository GitHub
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Kode bahasa untuk diterjemahkan (dipisahkan koma). Didukung: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Hapus file bahasa terjemahan tertentu (dipisahkan koma)",
        "help_remove_all_lang": "Hapus SEMUA file bahasa terjemahan dan bersihkan folder",
        "help_add_protect": "Tambahkan frasa ke daftar proteksi (pattern regex didukung)",
        "help_remove_protect": "Hapus frasa dari daftar proteksi",
        "help_list_protect": "Tampilkan semua frasa yang saat ini diproteksi",
        "help_init_protect": "Reset protected_phrases.json ke nilai default",
        "help_enable_protect": "Aktifkan proteksi frasa selama terjemahan",
        "help_disable_protect": "Nonaktifkan proteksi frasa selama terjemahan",
        "help_status_protect": "Periksa apakah proteksi frasa saat ini aktif",
        "help_translate_changelog": "Hanya terjemahkan CHANGELOG.md (gunakan 'all' untuk semua bahasa atau tentukan kode)",
        "help_auto_setup_changelog": "Otomatis tambahkan section changelog ke README.md jika CHANGELOG.md ada",
        "help_detect_github_url": "Deteksi dan tampilkan URL repository GitHub dari berbagai sumber",
        "help_display": "Bahasa untuk notifikasi terminal (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "jp": {
        "translating_readme": "📘 READMEを{lang_name}に翻訳中 ({lang_code})...",
        "readme_created": "✅ {path} が正常に作成されました",
        "translating_changelog": "📘 CHANGELOGを{lang_name}に翻訳中 ({lang_code})...",
        "changelog_created": "✅ {path} が正常に作成されました",
        "changelog_links_updated": "✅ {filename} のチェンジログリンクを更新しました",
        "all_translated": "🎉 すべてのREADMEが正常に翻訳されました！",
        "language_switcher_updated": "✅ {filename} の言語スイッチャーを更新しました",
        "file_deleted": "🗑️ ファイル {filename} を削除しました",
        "folder_deleted": "🗑️ フォルダ {folder} を削除しました",
        "changelog_section_added": "✅ README.mdに適切な間隔と区切りでチェンジログセクションを追加しました",
        "changelog_spacing_fixed": "✅ README.mdのチェンジログセクションの間隔と区切りを修正しました",
        "github_url_detected": "🔍 GitHubリポジトリ検出結果:",
        "repo_url": "📦 リポジトリURL: {url}",
        "releases_url": "🚀 リリースURL: {url}",
        "sources_checked": "📋 チェックしたソース:",
        "no_github_url": "❌ GitHubリポジトリURLを自動的に検出できませんでした。",
        "protection_reset": "🔁 protected_phrases.jsonファイルをデフォルトにリセットしました。",
        "phrase_added": "✅ フレーズ「{phrase}」を保護に追加しました。",
        "phrase_removed": "🗑️ フレーズ「{phrase}」を保護から削除しました。",
        "protected_phrases_list": "📜 保護されたフレーズのリスト:",
        "protection_enabled": "🟢 保護を有効にしました。",
        "protection_disabled": "🔴 保護を無効にしました。",
        "protection_status": "🧩 保護ステータス: {status}",
        "changelog_setup_completed": "✅ チェンジログのセットアップが完了しました",
        "changelog_setup_failed": "❌ チェンジログのセットアップに失敗しました",
        "no_changelog_file": "❌ ルートディレクトリにCHANGELOG.mdファイルがありません",
        "changelog_translated": "✅ {count}言語にCHANGELOGを正常に翻訳しました",
        "no_changelog_translated": "❌ 翻訳されたCHANGELOGファイルはありません",
        "languages_removed": "🎉 言語が正常に削除されました: {langs}",
        "all_languages_removed": "🎉 すべての翻訳ファイルが正常に削除されました",
        "auto_setup_changelog": "🔧 READMEにチェンジログセクションを自動設定中...",
        "checking_changelog_spacing": "🔧 チェンジログセクションの間隔を確認中...",
        "no_valid_language": "❌ 有効な言語コードが提供されていません。",
        "language_not_recognized": "❌ 言語コード「{code}」は認識されません。続行します...",
        "file_not_found": "⚠️ ファイル {filename} が見つかりません",
        "folder_not_empty": "⚠️ フォルダ {folder} が空ではないため、削除しません",
        "failed_delete_file": "❌ {filename} の削除に失敗: {error}",
        "failed_delete_folder": "❌ フォルダの削除に失敗: {error}",
        "failed_update_main": "❌ メインREADMEの更新に失敗: {error}",
        "failed_translate_changelog": "❌ CHANGELOGの翻訳に失敗: {error}",
        "failed_update_changelog_links": "❌ {filename} のチェンジログリンク更新に失敗: {error}",
        "failed_update_switcher": "❌ {filename} の言語スイッチャー更新に失敗: {error}",
        "translation_failed": "❌ 翻訳に失敗: {error}",
        "reading_package_error": "❌ package.jsonの読み込みエラー: {error}",
        "reading_git_error": "❌ .git/configの読み込みエラー: {error}",
        "reading_github_error": "❌ READMEでのGitHub URL検索エラー: {error}",
        "changelog_section_exists": "ℹ️ チェンジログセクションは既にREADME.mdに存在します",
        "no_changelog_file_root": "❌ ルートディレクトリにCHANGELOG.mdファイルがありません",
        "no_translation_files": "ℹ️ 翻訳されたREADMEファイルが見つかりません",
        "language_not_supported": "⚠️ 表示言語「{code}」はサポートされていません、デフォルトを使用します",
                "help_description": "MultiDoc Translator - 自動化された多言語ドキュメント翻訳ツール",
        "help_epilog": """
使用例:
  # READMEを日本語と中国語に翻訳
  python multidoc_translator.py --lang jp,zh

  # 変更ログのみをすべての言語に翻訳（日本語通知付き）
  python multidoc_translator.py --translate-changelog all --display jp

  # 特定の言語ファイルを削除
  python multidoc_translator.py --remove-lang jp,zh

  # READMEに変更ログセクションを自動設定
  python multidoc_translator.py --auto-setup-changelog

  # GitHubリポジトリURLを検出
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "翻訳する言語コード（カンマ区切り）。対応: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "特定の翻訳言語ファイルを削除（カンマ区切り）",
        "help_remove_all_lang": "すべての翻訳ファイルを削除しフォルダを整理",
        "help_add_protect": "保護リストにフレーズを追加（正規表現パターン対応）",
        "help_remove_protect": "保護リストからフレーズを削除",
        "help_list_protect": "現在保護されているすべてのフレーズを表示",
        "help_init_protect": "protected_phrases.jsonをデフォルト値にリセット",
        "help_enable_protect": "翻訳中のフレーズ保護を有効化",
        "help_disable_protect": "翻訳中のフレーズ保護を無効化",
        "help_status_protect": "フレーズ保護が現在有効かどうかを確認",
        "help_translate_changelog": "CHANGELOG.mdのみ翻訳（全言語の場合は'all'、またはコード指定）",
        "help_auto_setup_changelog": "CHANGELOG.mdが存在する場合、README.mdに変更ログセクションを自動追加",
        "help_detect_github_url": "さまざまなソースからGitHubリポジトリURLを検出して表示",
        "help_display": "ターミナル通知の表示言語 (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "de": {
        "translating_readme": "📘 Übersetze README in {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} erfolgreich erstellt",
        "translating_changelog": "📘 Übersetze CHANGELOG in {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} erfolgreich erstellt",
        "changelog_links_updated": "✅ Changelog-Links in {filename} aktualisiert",
        "all_translated": "🎉 Alle READMEs erfolgreich übersetzt!",
        "language_switcher_updated": "✅ Sprachumschaltung in {filename} aktualisiert",
        "file_deleted": "🗑️ Datei {filename} erfolgreich gelöscht",
        "folder_deleted": "🗑️ Ordner {folder} erfolgreich gelöscht",
        "changelog_section_added": "✅ Changelog-Abschnitt zu README.md mit korrektem Abstand und Trennzeichen hinzugefügt",
        "changelog_spacing_fixed": "✅ Changelog-Abschnittsabstand und Trennzeichen in README.md behoben",
        "github_url_detected": "🔍 GitHub-Repository-Erkennungsergebnisse:",
        "repo_url": "📦 Repository-URL: {url}",
        "releases_url": "🚀 Releases-URL: {url}",
        "sources_checked": "📋 Geprüfte Quellen:",
        "no_github_url": "❌ GitHub-Repository-URL konnte nicht automatisch erkannt werden.",
        "protection_reset": "🔁 Datei protected_phrases.json wurde auf Standard zurückgesetzt.",
        "phrase_added": "✅ Ausdruck '{phrase}' zum Schutz hinzugefügt.",
        "phrase_removed": "🗑️ Ausdruck '{phrase}' aus Schutz entfernt.",
        "protected_phrases_list": "📜 Geschützte Ausdrücke Liste:",
        "protection_enabled": "🟢 Schutz aktiviert.",
        "protection_disabled": "🔴 Schutz deaktiviert.",
        "protection_status": "🧩 Schutzstatus: {status}",
        "changelog_setup_completed": "✅ Changelog-Einrichtung abgeschlossen",
        "changelog_setup_failed": "❌ Changelog-Einrichtung fehlgeschlagen",
        "no_changelog_file": "❌ Sie haben keine CHANGELOG.md-Datei im Root-Verzeichnis",
        "changelog_translated": "✅ CHANGELOG erfolgreich in {count} Sprachen übersetzt",
        "no_changelog_translated": "❌ Keine CHANGELOG-Dateien wurden erfolgreich übersetzt",
        "languages_removed": "🎉 Sprachen erfolgreich entfernt: {langs}",
        "all_languages_removed": "🎉 Alle Übersetzungsdateien erfolgreich entfernt",
        "auto_setup_changelog": "🔧 Automatische Einrichtung des Changelog-Abschnitts in README...",
        "checking_changelog_spacing": "🔧 Überprüfe Changelog-Abschnittsabstand...",
        "no_valid_language": "❌ Keine gültigen Sprachcodes angegeben.",
        "language_not_recognized": "❌ Sprachcode '{code}' nicht erkannt. Fortfahren...",
        "file_not_found": "⚠️ Datei {filename} nicht gefunden",
        "folder_not_empty": "⚠️ Ordner {folder} nicht leer, nicht gelöscht",
        "failed_delete_file": "❌ Löschen von {filename} fehlgeschlagen: {error}",
        "failed_delete_folder": "❌ Löschen des Ordners fehlgeschlagen: {error}",
        "failed_update_main": "❌ Aktualisierung der Haupt-README fehlgeschlagen: {error}",
        "failed_translate_changelog": "❌ Übersetzung von CHANGELOG fehlgeschlagen: {error}",
        "failed_update_changelog_links": "❌ Aktualisierung der Changelog-Links in {filename} fehlgeschlagen: {error}",
        "failed_update_switcher": "❌ Aktualisierung der Sprachumschaltung in {filename} fehlgeschlagen: {error}",
        "translation_failed": "❌ Übersetzung fehlgeschlagen: {error}",
        "reading_package_error": "❌ Fehler beim Lesen von package.json: {error}",
        "reading_git_error": "❌ Fehler beim Lesen von .git/config: {error}",
        "reading_github_error": "❌ Fehler bei der Suche nach GitHub-URL in README: {error}",
        "changelog_section_exists": "ℹ️ Changelog-Abschnitt existiert bereits in README.md",
        "no_changelog_file_root": "❌ Keine CHANGELOG.md-Datei im Root-Verzeichnis gefunden",
        "no_translation_files": "ℹ️ Keine übersetzten README-Dateien gefunden",
        "language_not_supported": "⚠️ Anzeigesprache '{code}' nicht unterstützt, verwende Standard",
        "help_description": "MultiDoc Translator - Automatisierter mehrsprachiger Dokumentationsübersetzer",
        "help_epilog": """
Beispiele:
  # README auf Japanisch und Chinesisch übersetzen
  python multidoc_translator.py --lang jp,zh

  # Nur CHANGELOG in alle Sprachen mit japanischen Benachrichtigungen übersetzen
  python multidoc_translator.py --translate-changelog all --display jp

  # Bestimmte Sprachdateien entfernen
  python multidoc_translator.py --remove-lang jp,zh

  # Changelog-Bereich automatisch in README einrichten
  python multidoc_translator.py --auto-setup-changelog

  # GitHub-Repository-URL erkennen
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Zu übersetzende Sprachcodes (kommagetrennt). Unterstützt: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Bestimmte übersetzte Sprachdateien entfernen (kommagetrennt)",
        "help_remove_all_lang": "ALLE übersetzten Sprachdateien entfernen und Ordner bereinigen",
        "help_add_protect": "Eine Phrase zur Schutzliste hinzufügen (Regex-Muster unterstützt)",
        "help_remove_protect": "Eine Phrase aus der Schutzliste entfernen",
        "help_list_protect": "Alle aktuell geschützten Phrasen anzeigen",
        "help_init_protect": "protected_phrases.json auf Standardwerte zurücksetzen",
        "help_enable_protect": "Phrasenschutz während der Übersetzung aktivieren",
        "help_disable_protect": "Phrasenschutz während der Übersetzung deaktivieren",
        "help_status_protect": "Überprüfen, ob Phrasenschutz aktuell aktiviert ist",
        "help_translate_changelog": "Nur CHANGELOG.md übersetzen ('all' für alle Sprachen oder Codes angeben)",
        "help_auto_setup_changelog": "Changelog-Bereich automatisch zu README.md hinzufügen, wenn CHANGELOG.md existiert",
        "help_detect_github_url": "GitHub-Repository-URL aus verschiedenen Quellen erkennen und anzeigen",
        "help_display": "Anzeigesprache für Terminalbenachrichtigungen (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "es": {
        "translating_readme": "📘 Traduciendo README a {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} creado exitosamente",
        "translating_changelog": "📘 Traduciendo CHANGELOG a {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} creado exitosamente",
        "changelog_links_updated": "✅ Enlaces del changelog actualizados en {filename}",
        "all_translated": "🎉 ¡Todos los READMEs traducidos exitosamente!",
        "language_switcher_updated": "✅ Selector de idioma actualizado en {filename}",
        "file_deleted": "🗑️ Archivo {filename} eliminado exitosamente",
        "folder_deleted": "🗑️ Carpeta {folder} eliminada exitosamente",
        "changelog_section_added": "✅ Sección de changelog añadida a README.md con espaciado y separadores adecuados",
        "changelog_spacing_fixed": "✅ Espaciado y separadores de la sección changelog corregidos en README.md",
        "github_url_detected": "🔍 Resultados de detección de repositorio GitHub:",
        "repo_url": "📦 URL del repositorio: {url}",
        "releases_url": "🚀 URL de releases: {url}",
        "sources_checked": "📋 Fuentes verificadas:",
        "no_github_url": "❌ No se pudo detectar automáticamente la URL del repositorio GitHub.",
        "protection_reset": "🔁 Archivo protected_phrases.json ha sido restablecido a predeterminado.",
        "phrase_added": "✅ Frase '{phrase}' añadida a protección.",
        "phrase_removed": "🗑️ Frase '{phrase}' eliminada de protección.",
        "protected_phrases_list": "📜 Lista de frases protegidas:",
        "protection_enabled": "🟢 Protección habilitada.",
        "protection_disabled": "🔴 Protección deshabilitada.",
        "protection_status": "🧩 Estado de protección: {status}",
        "changelog_setup_completed": "✅ Configuración de changelog completada",
        "changelog_setup_failed": "❌ Configuración de changelog fallida",
        "no_changelog_file": "❌ No tienes archivo CHANGELOG.md en el directorio raíz",
        "changelog_translated": "✅ CHANGELOG traducido exitosamente a {count} idiomas",
        "no_changelog_translated": "❌ No se tradujeron exitosamente archivos CHANGELOG",
        "languages_removed": "🎉 Idiomas eliminados exitosamente: {langs}",
        "all_languages_removed": "🎉 Todos los archivos de traducción eliminados exitosamente",
        "auto_setup_changelog": "🔧 Configuración automática de sección changelog en README...",
        "checking_changelog_spacing": "🔧 Verificando espaciado de sección changelog...",
        "no_valid_language": "❌ No se proporcionaron códigos de idioma válidos.",
        "language_not_recognized": "❌ Código de idioma '{code}' no reconocido. Continuando...",
        "file_not_found": "⚠️ Archivo {filename} no encontrado",
        "folder_not_empty": "⚠️ Carpeta {folder} no vacía, no eliminada",
        "failed_delete_file": "❌ Error al eliminar {filename}: {error}",
        "failed_delete_folder": "❌ Error al eliminar carpeta: {error}",
        "failed_update_main": "❌ Error al actualizar README principal: {error}",
        "failed_translate_changelog": "❌ Error al traducir CHANGELOG: {error}",
        "failed_update_changelog_links": "❌ Error al actualizar enlaces de changelog en {filename}: {error}",
        "failed_update_switcher": "❌ Error al actualizar selector de idioma en {filename}: {error}",
        "translation_failed": "❌ Error en traducción: {error}",
        "reading_package_error": "❌ Error leyendo package.json: {error}",
        "reading_git_error": "❌ Error leyendo .git/config: {error}",
        "reading_github_error": "❌ Error buscando URL de GitHub en README: {error}",
        "changelog_section_exists": "ℹ️ La sección changelog ya existe en README.md",
        "no_changelog_file_root": "❌ No se encontró archivo CHANGELOG.md en directorio raíz",
        "no_translation_files": "ℹ️ No se encontraron archivos README traducidos",
        "language_not_supported": "⚠️ Idioma de visualización '{code}' no soportado, usando predeterminado",
        "help_description": "MultiDoc Translator - Traductor automatizado de documentación multilingüe",
        "help_epilog": """
Ejemplos:
  # Traducir README a japonés y chino
  python multidoc_translator.py --lang jp,zh

  # Traducir solo CHANGELOG a todos los idiomas con notificaciones en japonés
  python multidoc_translator.py --translate-changelog all --display jp

  # Eliminar archivos de idiomas específicos
  python multidoc_translator.py --remove-lang jp,zh

  # Configuración automática de sección changelog en README
  python multidoc_translator.py --auto-setup-changelog

  # Detectar URL de repositorio GitHub
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Códigos de idioma a traducir (separados por comas). Soportados: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Eliminar archivos de idiomas traducidos específicos (separados por comas)",
        "help_remove_all_lang": "Eliminar TODOS los archivos de idiomas traducidos y limpiar carpetas",
        "help_add_protect": "Agregar una frase a la lista de protección (patrón regex compatible)",
        "help_remove_protect": "Eliminar una frase de la lista de protección",
        "help_list_protect": "Mostrar todas las frases actualmente protegidas",
        "help_init_protect": "Restablecer protected_phrases.json a valores predeterminados",
        "help_enable_protect": "Habilitar protección de frases durante la traducción",
        "help_disable_protect": "Deshabilitar protección de frases durante la traducción",
        "help_status_protect": "Verificar si la protección de frases está actualmente habilitada",
        "help_translate_changelog": "Traducir solo CHANGELOG.md (usar 'all' para todos los idiomas o especificar códigos)",
        "help_auto_setup_changelog": "Agregar automáticamente sección changelog a README.md si CHANGELOG.md existe",
        "help_detect_github_url": "Detectar y mostrar URL de repositorio GitHub desde varias fuentes",
        "help_display": "Idioma de visualización para notificaciones de terminal (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "fr": {
        "translating_readme": "📘 Traduction du README en {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} créé avec succès",
        "translating_changelog": "📘 Traduction du CHANGELOG en {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} créé avec succès",
        "changelog_links_updated": "✅ Liens du changelog mis à jour dans {filename}",
        "all_translated": "🎉 Tous les README traduits avec succès !",
        "language_switcher_updated": "✅ Sélecteur de langue mis à jour dans {filename}",
        "file_deleted": "🗑️ Fichier {filename} supprimé avec succès",
        "folder_deleted": "🗑️ Dossier {folder} supprimé avec succès",
        "changelog_section_added": "✅ Section changelog ajoutée à README.md avec espacement et séparateurs appropriés",
        "changelog_spacing_fixed": "✅ Espacement et séparateurs de section changelog corrigés dans README.md",
        "github_url_detected": "🔍 Résultats de détection du dépôt GitHub :",
        "repo_url": "📦 URL du dépôt : {url}",
        "releases_url": "🚀 URL des releases : {url}",
        "sources_checked": "📋 Sources vérifiées :",
        "no_github_url": "❌ Impossible de détecter automatiquement l'URL du dépôt GitHub.",
        "protection_reset": "🔁 Fichier protected_phrases.json a été réinitialisé par défaut.",
        "phrase_added": "✅ Expression '{phrase}' ajoutée à la protection.",
        "phrase_removed": "🗑️ Expression '{phrase}' retirée de la protection.",
        "protected_phrases_list": "📜 Liste des expressions protégées :",
        "protection_enabled": "🟢 Protection activée.",
        "protection_disabled": "🔴 Protection désactivée.",
        "protection_status": "🧩 Statut de protection : {status}",
        "changelog_setup_completed": "✅ Configuration du changelog terminée",
        "changelog_setup_failed": "❌ Échec de la configuration du changelog",
        "no_changelog_file": "❌ Vous n'avez pas de fichier CHANGELOG.md dans le répertoire racine",
        "changelog_translated": "✅ CHANGELOG traduit avec succès en {count} langues",
        "no_changelog_translated": "❌ Aucun fichier CHANGELOG n'a été traduit avec succès",
        "languages_removed": "🎉 Langues supprimées avec succès : {langs}",
        "all_languages_removed": "🎉 Tous les fichiers de traduction supprimés avec succès",
        "auto_setup_changelog": "🔧 Configuration automatique de la section changelog dans README...",
        "checking_changelog_spacing": "🔧 Vérification de l'espacement de la section changelog...",
        "no_valid_language": "❌ Aucun code de langue valide fourni.",
        "language_not_recognized": "❌ Code de langue '{code}' non reconnu. Continuation...",
        "file_not_found": "⚠️ Fichier {filename} non trouvé",
        "folder_not_empty": "⚠️ Dossier {folder} non vide, non supprimé",
        "failed_delete_file": "❌ Échec de la suppression de {filename} : {error}",
        "failed_delete_folder": "❌ Échec de la suppression du dossier : {error}",
        "failed_update_main": "❌ Échec de la mise à jour du README principal : {error}",
        "failed_translate_changelog": "❌ Échec de la traduction du CHANGELOG : {error}",
        "failed_update_changelog_links": "❌ Échec de la mise à jour des liens du changelog dans {filename} : {error}",
        "failed_update_switcher": "❌ Échec de la mise à jour du sélecteur de langue dans {filename} : {error}",
        "translation_failed": "❌ Échec de la traduction : {error}",
        "reading_package_error": "❌ Erreur de lecture de package.json : {error}",
        "reading_git_error": "❌ Erreur de lecture de .git/config : {error}",
        "reading_github_error": "❌ Erreur de recherche d'URL GitHub dans README : {error}",
        "changelog_section_exists": "ℹ️ La section changelog existe déjà dans README.md",
        "no_changelog_file_root": "❌ Aucun fichier CHANGELOG.md trouvé dans le répertoire racine",
        "no_translation_files": "ℹ️ Aucun fichier README traduit trouvé",
        "language_not_supported": "⚠️ Langue d'affichage '{code}' non supportée, utilisation par défaut",
        "help_description": "MultiDoc Translator - Traducteur automatisé de documentation multilingue",
        "help_epilog": """
Exemples :
  # Traduire README en japonais et chinois
  python multidoc_translator.py --lang jp,zh

  # Traduire seulement CHANGELOG dans toutes les langues avec notifications en japonais
  python multidoc_translator.py --translate-changelog all --display jp

  # Supprimer des fichiers de langue spécifiques
  python multidoc_translator.py --remove-lang jp,zh

  # Configuration automatique de la section changelog dans README
  python multidoc_translator.py --auto-setup-changelog

  # Détecter l'URL du dépôt GitHub
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Codes de langue à traduire (séparés par des virgules). Pris en charge : pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Supprimer des fichiers de langue traduits spécifiques (séparés par des virgules)",
        "help_remove_all_lang": "Supprimer TOUS les fichiers de langue traduits et nettoyer les dossiers",
        "help_add_protect": "Ajouter une phrase à la liste de protection (modèle regex pris en charge)",
        "help_remove_protect": "Supprimer une phrase de la liste de protection",
        "help_list_protect": "Afficher toutes les phrases actuellement protégées",
        "help_init_protect": "Réinitialiser protected_phrases.json aux valeurs par défaut",
        "help_enable_protect": "Activer la protection des phrases pendant la traduction",
        "help_disable_protect": "Désactiver la protection des phrases pendant la traduction",
        "help_status_protect": "Vérifier si la protection des phrases est actuellement activée",
        "help_translate_changelog": "Traduire seulement CHANGELOG.md (utiliser 'all' pour toutes les langues ou spécifier des codes)",
        "help_auto_setup_changelog": "Ajouter automatiquement la section changelog à README.md si CHANGELOG.md existe",
        "help_detect_github_url": "Détecter et afficher l'URL du dépôt GitHub depuis diverses sources",
        "help_display": "Langue d'affichage pour les notifications du terminal (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "kr": {
        "translating_readme": "📘 README를 {lang_name}({lang_code})로 번역 중...",
        "readme_created": "✅ {path}이(가) 성공적으로 생성됨",
        "translating_changelog": "📘 CHANGELOG를 {lang_name}({lang_code})로 번역 중...",
        "changelog_created": "✅ {path}이(가) 성공적으로 생성됨",
        "changelog_links_updated": "✅ {filename}에서 체인지로그 링크 업데이트됨",
        "all_translated": "🎉 모든 README가 성공적으로 번역됨!",
        "language_switcher_updated": "✅ {filename}에서 언어 전환기 업데이트됨",
        "file_deleted": "🗑️ 파일 {filename}이(가) 성공적으로 삭제됨",
        "folder_deleted": "🗑️ 폴더 {folder}이(가) 성공적으로 삭제됨",
        "changelog_section_added": "✅ README.md에 적절한 간격과 구분자로 체인지로그 섹션 추가됨",
        "changelog_spacing_fixed": "✅ README.md에서 체인지로그 섹션 간격과 구분자 수정됨",
        "github_url_detected": "🔍 GitHub 저장소 감지 결과:",
        "repo_url": "📦 저장소 URL: {url}",
        "releases_url": "🚀 릴리스 URL: {url}",
        "sources_checked": "📋 확인된 소스:",
        "no_github_url": "❌ GitHub 저장소 URL을 자동으로 감지할 수 없습니다.",
        "protection_reset": "🔁 protected_phrases.json 파일이 기본값으로 재설정되었습니다.",
        "phrase_added": "✅ '{phrase}' 문구가 보호에 추가됨",
        "phrase_removed": "🗑️ '{phrase}' 문구가 보호에서 제거됨",
        "protected_phrases_list": "📜 보호된 문구 목록:",
        "protection_enabled": "🟢 보호 활성화됨",
        "protection_disabled": "🔴 보호 비활성화됨",
        "protection_status": "🧩 보호 상태: {status}",
        "changelog_setup_completed": "✅ 체인지로그 설정 완료",
        "changelog_setup_failed": "❌ 체인지로그 설정 실패",
        "no_changelog_file": "❌ 루트 디렉토리에 CHANGELOG.md 파일이 없습니다",
        "changelog_translated": "✅ {count}개 언어로 CHANGELOG 성공적으로 번역됨",
        "no_changelog_translated": "❌ 성공적으로 번역된 CHANGELOG 파일이 없습니다",
        "languages_removed": "🎉 언어가 성공적으로 제거됨: {langs}",
        "all_languages_removed": "🎉 모든 번역 파일이 성공적으로 제거됨",
        "auto_setup_changelog": "🔧 README에서 체인지로그 섹션 자동 설정 중...",
        "checking_changelog_spacing": "🔧 체인지로그 섹션 간격 확인 중...",
        "no_valid_language": "❌ 유효한 언어 코드가 제공되지 않았습니다.",
        "language_not_recognized": "❌ '{code}' 언어 코드를 인식할 수 없습니다. 계속 진행합니다...",
        "file_not_found": "⚠️ {filename} 파일을 찾을 수 없습니다",
        "folder_not_empty": "⚠️ {folder} 폴더가 비어 있지 않아 삭제하지 않았습니다",
        "failed_delete_file": "❌ {filename} 삭제 실패: {error}",
        "failed_delete_folder": "❌ 폴더 삭제 실패: {error}",
        "failed_update_main": "❌ 메인 README 업데이트 실패: {error}",
        "failed_translate_changelog": "❌ CHANGELOG 번역 실패: {error}",
        "failed_update_changelog_links": "❌ {filename}에서 체인지로그 링크 업데이트 실패: {error}",
        "failed_update_switcher": "❌ {filename}에서 언어 전환기 업데이트 실패: {error}",
        "translation_failed": "❌ 번역 실패: {error}",
        "reading_package_error": "❌ package.json 읽기 오류: {error}",
        "reading_git_error": "❌ .git/config 읽기 오류: {error}",
        "reading_github_error": "❌ README에서 GitHub URL 검색 오류: {error}",
        "changelog_section_exists": "ℹ️ 체인지로그 섹션이 이미 README.md에 존재합니다",
        "no_changelog_file_root": "❌ 루트 디렉토리에 CHANGELOG.md 파일이 없습니다",
        "no_translation_files": "ℹ️ 번역된 README 파일을 찾을 수 없습니다",
        "language_not_supported": "⚠️ '{code}' 표시 언어는 지원되지 않으며, 기본값을 사용합니다",
        "help_description": "MultiDoc Translator - 자동화된 다국어 문서 번역기",
        "help_epilog": """
사용 예:
  # README를 일본어와 중국어로 번역
  python multidoc_translator.py --lang jp,zh

  # 일본어 알림으로 모든 언어에 대해 CHANGELOG만 번역
  python multidoc_translator.py --translate-changelog all --display jp

  # 특정 언어 파일 삭제
  python multidoc_translator.py --remove-lang jp,zh

  # README에 체인지로그 섹션 자동 설정
  python multidoc_translator.py --auto-setup-changelog

  # GitHub 저장소 URL 감지
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "번역할 언어 코드 (쉼표로 구분). 지원: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "특정 번역된 언어 파일 삭제 (쉼표로 구분)",
        "help_remove_all_lang": "모든 번역 파일 삭제 및 폴더 정리",
        "help_add_protect": "보호 목록에 문구 추가 (정규식 패턴 지원)",
        "help_remove_protect": "보호 목록에서 문구 제거",
        "help_list_protect": "현재 보호 중인 모든 문구 표시",
        "help_init_protect": "protected_phrases.json을 기본값으로 재설정",
        "help_enable_protect": "번역 중 문구 보호 활성화",
        "help_disable_protect": "번역 중 문구 보호 비활성화",
        "help_status_protect": "문구 보호가 현재 활성화되었는지 확인",
        "help_translate_changelog": "CHANGELOG.md만 번역 (모든 언어는 'all' 사용 또는 코드 지정)",
        "help_auto_setup_changelog": "CHANGELOG.md가 존재하면 README.md에 체인지로그 섹션 자동 추가",
        "help_detect_github_url": "다양한 소스에서 GitHub 저장소 URL 감지 및 표시",
        "help_display": "터미널 알림 표시 언어 (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "pl": {
        "translating_readme": "📘 Tłumaczenie README na {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} pomyślnie utworzony",
        "translating_changelog": "📘 Tłumaczenie CHANGELOG na {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} pomyślnie utworzony",
        "changelog_links_updated": "✅ Linki changelog zaktualizowane w {filename}",
        "all_translated": "🎉 Wszystkie README pomyślnie przetłumaczone!",
        "language_switcher_updated": "✅ Przełącznik języka zaktualizowany w {filename}",
        "file_deleted": "🗑️ Plik {filename} pomyślnie usunięty",
        "folder_deleted": "🗑️ Folder {folder} pomyślnie usunięty",
        "changelog_section_added": "✅ Sekcja changelog dodana do README.md z właściwymi odstępami i separatorami",
        "changelog_spacing_fixed": "✅ Naprawiono odstępy i separatory sekcji changelog w README.md",
        "github_url_detected": "🔍 Wyniki wykrywania repozytorium GitHub:",
        "repo_url": "📦 URL repozytorium: {url}",
        "releases_url": "🚀 URL wydań: {url}",
        "sources_checked": "📋 Sprawdzone źródła:",
        "no_github_url": "❌ Nie można automatycznie wykryć URL repozytorium GitHub.",
        "protection_reset": "🔁 Plik protected_phrases.json został zresetowany do domyślnych ustawień.",
        "phrase_added": "✅ Wyrażenie '{phrase}' dodane do ochrony.",
        "phrase_removed": "🗑️ Wyrażenie '{phrase}' usunięte z ochrony.",
        "protected_phrases_list": "📜 Lista chronionych wyrażeń:",
        "protection_enabled": "🟢 Ochrona włączona.",
        "protection_disabled": "🔴 Ochrona wyłączona.",
        "protection_status": "🧩 Status ochrony: {status}",
        "changelog_setup_completed": "✅ Konfiguracja changelog ukończona",
        "changelog_setup_failed": "❌ Konfiguracja changelog nie powiodła się",
        "no_changelog_file": "❌ Nie masz pliku CHANGELOG.md w katalogu głównym",
        "changelog_translated": "✅ Pomyślnie przetłumaczono CHANGELOG na {count} języków",
        "no_changelog_translated": "❌ Żadne pliki CHANGELOG nie zostały pomyślnie przetłumaczone",
        "languages_removed": "🎉 Języki pomyślnie usunięte: {langs}",
        "all_languages_removed": "🎉 Wszystkie pliki tłumaczeń pomyślnie usunięte",
        "auto_setup_changelog": "🔧 Automatyczna konfiguracja sekcji changelog w README...",
        "checking_changelog_spacing": "🔧 Sprawdzanie odstępów sekcji changelog...",
        "no_valid_language": "❌ Nie podano prawidłowych kodów języków.",
        "language_not_recognized": "❌ Kod języka '{code}' nierozpoznany. Kontynuowanie...",
        "file_not_found": "⚠️ Plik {filename} nie znaleziony",
        "folder_not_empty": "⚠️ Folder {folder} nie jest pusty, nie usunięto",
        "failed_delete_file": "❌ Nie udało się usunąć {filename}: {error}",
        "failed_delete_folder": "❌ Nie udało się usunąć folderu: {error}",
        "failed_update_main": "❌ Nie udało się zaktualizować głównego README: {error}",
        "failed_translate_changelog": "❌ Nie udało się przetłumaczyć CHANGELOG: {error}",
        "failed_update_changelog_links": "❌ Nie udało się zaktualizować linków changelog w {filename}: {error}",
        "failed_update_switcher": "❌ Nie udało się zaktualizować przełącznika języka w {filename}: {error}",
        "translation_failed": "❌ Tłumaczenie nie powiodło się: {error}",
        "reading_package_error": "❌ Błąd odczytu package.json: {error}",
        "reading_git_error": "❌ Błąd odczytu .git/config: {error}",
        "reading_github_error": "❌ Błąd wyszukiwania URL GitHub w README: {error}",
        "changelog_section_exists": "ℹ️ Sekcja changelog już istnieje w README.md",
        "no_changelog_file_root": "❌ Nie znaleziono pliku CHANGELOG.md w katalogu głównym",
        "no_translation_files": "ℹ️ Nie znaleziono przetłumaczonych plików README",
        "language_not_supported": "⚠️ Język wyświetlania '{code}' nie jest obsługiwany, używam domyślnego",
        "help_description": "MultiDoc Translator - Zautomatyzowany tłumacz dokumentacji wielojęzycznej",
        "help_epilog": """
Przykłady:
  # Tłumaczenie README na japoński i chiński
  python multidoc_translator.py --lang jp,zh

  # Tłumaczenie tylko CHANGELOG na wszystkie języki z japońskimi powiadomieniami
  python multidoc_translator.py --translate-changelog all --display jp

  # Usuwanie określonych plików językowych
  python multidoc_translator.py --remove-lang jp,zh

  # Automatyczna konfiguracja sekcji changelog w README
  python multidoc_translator.py --auto-setup-changelog

  # Wykrywanie URL repozytorium GitHub
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Kody języków do tłumaczenia (oddzielone przecinkami). Obsługiwane: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Usuwanie określonych przetłumaczonych plików językowych (oddzielone przecinkami)",
        "help_remove_all_lang": "Usuwanie WSZYSTKICH przetłumaczonych plików językowych i czyszczenie folderów",
        "help_add_protect": "Dodawanie frazy do listy ochrony (wzorzec regex obsługiwany)",
        "help_remove_protect": "Usuwanie frazy z listy ochrony",
        "help_list_protect": "Wyświetlanie wszystkich obecnie chronionych fraz",
        "help_init_protect": "Resetowanie protected_phrases.json do wartości domyślnych",
        "help_enable_protect": "Włączanie ochrony fraz podczas tłumaczenia",
        "help_disable_protect": "Wyłączanie ochrony fraz podczas tłumaczenia",
        "help_status_protect": "Sprawdzanie, czy ochrona fraz jest obecnie włączona",
        "help_translate_changelog": "Tłumaczenie tylko CHANGELOG.md (użyj 'all' dla wszystkich języków lub określ kody)",
        "help_auto_setup_changelog": "Automatyczne dodawanie sekcji changelog do README.md, jeśli CHANGELOG.md istnieje",
        "help_detect_github_url": "Wykrywanie i wyświetlanie URL repozytorium GitHub z różnych źródeł",
        "help_display": "Język wyświetlania powiadomień terminala (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "pt": {
        "translating_readme": "📘 Traduzindo README para {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} criado com sucesso",
        "translating_changelog": "📘 Traduzindo CHANGELOG para {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} criado com sucesso",
        "changelog_links_updated": "✅ Links do changelog atualizados em {filename}",
        "all_translated": "🎉 Todos os READMEs traduzidos com sucesso!",
        "language_switcher_updated": "✅ Seletor de idioma atualizado em {filename}",
        "file_deleted": "🗑️ Arquivo {filename} excluído com sucesso",
        "folder_deleted": "🗑️ Pasta {folder} excluída com sucesso",
        "changelog_section_added": "✅ Seção changelog adicionada ao README.md com espaçamento e separadores adequados",
        "changelog_spacing_fixed": "✅ Espaçamento e separadores da seção changelog corrigidos no README.md",
        "github_url_detected": "🔍 Resultados da detecção do repositório GitHub:",
        "repo_url": "📦 URL do repositório: {url}",
        "releases_url": "🚀 URL de releases: {url}",
        "sources_checked": "📋 Fontes verificadas:",
        "no_github_url": "❌ Não foi possível detectar automaticamente a URL do repositório GitHub.",
        "protection_reset": "🔁 Arquivo protected_phrases.json foi redefinido para o padrão.",
        "phrase_added": "✅ Frase '{phrase}' adicionada à proteção.",
        "phrase_removed": "🗑️ Frase '{phrase}' removida da proteção.",
        "protected_phrases_list": "📜 Lista de frases protegidas:",
        "protection_enabled": "🟢 Proteção ativada.",
        "protection_disabled": "🔴 Proteção desativada.",
        "protection_status": "🧩 Status da proteção: {status}",
        "changelog_setup_completed": "✅ Configuração do changelog concluída",
        "changelog_setup_failed": "❌ Configuração do changelog falhou",
        "no_changelog_file": "❌ Você não tem o arquivo CHANGELOG.md no diretório raiz",
        "changelog_translated": "✅ CHANGELOG traduzido com sucesso para {count} idiomas",
        "no_changelog_translated": "❌ Nenhum arquivo CHANGELOG foi traduzido com sucesso",
        "languages_removed": "🎉 Idiomas removidos com sucesso: {langs}",
        "all_languages_removed": "🎉 Todos os arquivos de tradução removidos com sucesso",
        "auto_setup_changelog": "🔧 Configurando automaticamente a seção changelog no README...",
        "checking_changelog_spacing": "🔧 Verificando espaçamento da seção changelog...",
        "no_valid_language": "❌ Nenhum código de idioma válido fornecido.",
        "language_not_recognized": "❌ Código de idioma '{code}' não reconhecido. Continuando...",
        "file_not_found": "⚠️ Arquivo {filename} não encontrado",
        "folder_not_empty": "⚠️ Pasta {folder} não está vazia, não excluída",
        "failed_delete_file": "❌ Falha ao excluir {filename}: {error}",
        "failed_delete_folder": "❌ Falha ao excluir pasta: {error}",
        "failed_update_main": "❌ Falha ao atualizar README principal: {error}",
        "failed_translate_changelog": "❌ Falha ao traduzir CHANGELOG: {error}",
        "failed_update_changelog_links": "❌ Falha ao atualizar links do changelog em {filename}: {error}",
        "failed_update_switcher": "❌ Falha ao atualizar seletor de idioma em {filename}: {error}",
        "translation_failed": "❌ Falha na tradução: {error}",
        "reading_package_error": "❌ Erro lendo package.json: {error}",
        "reading_git_error": "❌ Erro lendo .git/config: {error}",
        "reading_github_error": "❌ Erro pesquisando URL do GitHub no README: {error}",
        "changelog_section_exists": "ℹ️ Seção changelog já existe no README.md",
        "no_changelog_file_root": "❌ Nenhum arquivo CHANGELOG.md encontrado no diretório raiz",
        "no_translation_files": "ℹ️ Nenhum arquivo README traduzido encontrado",
        "language_not_supported": "⚠️ Idioma de exibição '{code}' não suportado, usando padrão",
        "help_description": "MultiDoc Translator - Tradutor automatizado de documentação multilíngue",
        "help_epilog": """
Exemplos:
  # Traduzir README para japonês e chinês
  python multidoc_translator.py --lang jp,zh

  # Traduzir apenas CHANGELOG para todos os idiomas com notificações em japonês
  python multidoc_translator.py --translate-changelog all --display jp

  # Remover arquivos de idiomas específicos
  python multidoc_translator.py --remove-lang jp,zh

  # Configuração automática da seção changelog no README
  python multidoc_translator.py --auto-setup-changelog

  # Detectar URL do repositório GitHub
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Códigos de idioma para traduzir (separados por vírgula). Suportados: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Remover arquivos de idiomas traduzidos específicos (separados por vírgula)",
        "help_remove_all_lang": "Remover TODOS os arquivos de idiomas traduzidos e limpar pastas",
        "help_add_protect": "Adicionar uma frase à lista de proteção (padrão regex suportado)",
        "help_remove_protect": "Remover uma frase da lista de proteção",
        "help_list_protect": "Mostrar todas as frases atualmente protegidas",
        "help_init_protect": "Redefinir protected_phrases.json para valores padrão",
        "help_enable_protect": "Habilitar proteção de frases durante a tradução",
        "help_disable_protect": "Desabilitar proteção de frases durante a tradução",
        "help_status_protect": "Verificar se a proteção de frases está atualmente habilitada",
        "help_translate_changelog": "Traduzir apenas CHANGELOG.md (use 'all' para todos os idiomas ou especifique códigos)",
        "help_auto_setup_changelog": "Adicionar automaticamente seção changelog ao README.md se CHANGELOG.md existir",
        "help_detect_github_url": "Detectar e exibir URL do repositório GitHub de várias fontes",
        "help_display": "Idioma de exibição para notificações do terminal (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "ru": {
        "translating_readme": "📘 Перевод README на {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} успешно создан",
        "translating_changelog": "📘 Перевод CHANGELOG на {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} успешно создан",
        "changelog_links_updated": "✅ Ссылки на changelog обновлены в {filename}",
        "all_translated": "🎉 Все README успешно переведены!",
        "language_switcher_updated": "✅ Переключатель языка обновлен в {filename}",
        "file_deleted": "🗑️ Файл {filename} успешно удален",
        "folder_deleted": "🗑️ Папка {folder} успешно удалена",
        "changelog_section_added": "✅ Раздел changelog добавлен в README.md с правильными отступами и разделителями",
        "changelog_spacing_fixed": "✅ Исправлены отступы и разделители раздела changelog в README.md",
        "github_url_detected": "🔍 Результаты обнаружения репозитория GitHub:",
        "repo_url": "📦 URL репозитория: {url}",
        "releases_url": "🚀 URL релизов: {url}",
        "sources_checked": "📋 Проверенные источники:",
        "no_github_url": "❌ Не удалось автоматически определить URL репозитория GitHub.",
        "protection_reset": "🔁 Файл protected_phrases.json сброшен к значениям по умолчанию.",
        "phrase_added": "✅ Фраза '{phrase}' добавлена в защиту.",
        "phrase_removed": "🗑️ Фраза '{phrase}' удалена из защиты.",
        "protected_phrases_list": "📜 Список защищенных фраз:",
        "protection_enabled": "🟢 Защита включена.",
        "protection_disabled": "🔴 Защита отключена.",
        "protection_status": "🧩 Статус защиты: {status}",
        "changelog_setup_completed": "✅ Настройка changelog завершена",
        "changelog_setup_failed": "❌ Настройка changelog не удалась",
        "no_changelog_file": "❌ У вас нет файла CHANGELOG.md в корневом каталоге",
        "changelog_translated": "✅ CHANGELOG успешно переведен на {count} языков",
        "no_changelog_translated": "❌ Ни один файл CHANGELOG не был успешно переведен",
        "languages_removed": "🎉 Языки успешно удалены: {langs}",
        "all_languages_removed": "🎉 Все файлы переводов успешно удалены",
        "auto_setup_changelog": "🔧 Автоматическая настройка раздела changelog в README...",
        "checking_changelog_spacing": "🔧 Проверка отступов раздела changelog...",
        "no_valid_language": "❌ Не предоставлено действительных кодов языков.",
        "language_not_recognized": "❌ Код языка '{code}' не распознан. Продолжение...",
        "file_not_found": "⚠️ Файл {filename} не найден",
        "folder_not_empty": "⚠️ Папка {folder} не пуста, не удалена",
        "failed_delete_file": "❌ Не удалось удалить {filename}: {error}",
        "failed_delete_folder": "❌ Не удалось удалить папку: {error}",
        "failed_update_main": "❌ Не удалось обновить основной README: {error}",
        "failed_translate_changelog": "❌ Не удалось перевести CHANGELOG: {error}",
        "failed_update_changelog_links": "❌ Не удалось обновить ссылки на changelog в {filename}: {error}",
        "failed_update_switcher": "❌ Не удалось обновить переключатель языка в {filename}: {error}",
        "translation_failed": "❌ Ошибка перевода: {error}",
        "reading_package_error": "❌ Ошибка чтения package.json: {error}",
        "reading_git_error": "❌ Ошибка чтения .git/config: {error}",
        "reading_github_error": "❌ Ошибка поиска URL GitHub в README: {error}",
        "changelog_section_exists": "ℹ️ Раздел changelog уже существует в README.md",
        "no_changelog_file_root": "❌ Файл CHANGELOG.md не найден в корневом каталоге",
        "no_translation_files": "ℹ️ Переведенные файлы README не найдены",
        "language_not_supported": "⚠️ Язык отображения '{code}' не поддерживается, используется по умолчанию",
        "help_description": "MultiDoc Translator - Автоматизированный переводчик многоязычной документации",
        "help_epilog": """
Примеры:
  # Перевод README на японский и китайский
  python multidoc_translator.py --lang jp,zh

  # Перевод только CHANGELOG на все языки с японскими уведомлениями
  python multidoc_translator.py --translate-changelog all --display jp

  # Удаление определенных языковых файлов
  python multidoc_translator.py --remove-lang jp,zh

  # Автоматическая настройка раздела changelog в README
  python multidoc_translator.py --auto-setup-changelog

  # Обнаружение URL репозитория GitHub
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "Коды языков для перевода (разделены запятыми). Поддерживаются: pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "Удаление определенных переведенных языковых файлов (разделены запятыми)",
        "help_remove_all_lang": "Удаление ВСЕХ переведенных языковых файлов и очистка папок",
        "help_add_protect": "Добавление фразы в список защиты (поддерживается regex-шаблон)",
        "help_remove_protect": "Удаление фразы из списка защиты",
        "help_list_protect": "Показать все текущие защищенные фразы",
        "help_init_protect": "Сброс protected_phrases.json к значениям по умолчанию",
        "help_enable_protect": "Включить защиту фраз во время перевода",
        "help_disable_protect": "Отключить защиту фраз во время перевода",
        "help_status_protect": "Проверить, включена ли в настоящее время защита фраз",
        "help_translate_changelog": "Перевести только CHANGELOG.md (использовать 'all' для всех языков или указать коды)",
        "help_auto_setup_changelog": "Автоматически добавить раздел changelog в README.md, если CHANGELOG.md существует",
        "help_detect_github_url": "Обнаружить и отобразить URL репозитория GitHub из различных источников",
        "help_display": "Язык отображения для уведомлений терминала (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    },
    "zh": {
        "translating_readme": "📘 正在将 README 翻译为 {lang_name} ({lang_code})...",
        "readme_created": "✅ {path} 成功创建",
        "translating_changelog": "📘 正在将 CHANGELOG 翻译为 {lang_name} ({lang_code})...",
        "changelog_created": "✅ {path} 成功创建",
        "changelog_links_updated": "✅ 已在 {filename} 中更新更新日志链接",
        "all_translated": "🎉 所有 README 已成功翻译！",
        "language_switcher_updated": "✅ 已在 {filename} 中更新语言切换器",
        "file_deleted": "🗑️ 文件 {filename} 已成功删除",
        "folder_deleted": "🗑️ 文件夹 {folder} 已成功删除",
        "changelog_section_added": "✅ 已使用适当的间距和分隔符将更新日志部分添加到 README.md",
        "changelog_spacing_fixed": "✅ 已修复 README.md 中的更新日志部分间距和分隔符",
        "github_url_detected": "🔍 GitHub 仓库检测结果：",
        "repo_url": "📦 仓库 URL：{url}",
        "releases_url": "🚀 发布版本 URL：{url}",
        "sources_checked": "📋 已检查的来源：",
        "no_github_url": "❌ 无法自动检测 GitHub 仓库 URL。",
        "protection_reset": "🔁 文件 protected_phrases.json 已重置为默认值。",
        "phrase_added": "✅ 短语 '{phrase}' 已添加到保护。",
        "phrase_removed": "🗑️ 短语 '{phrase}' 已从保护中移除。",
        "protected_phrases_list": "📜 受保护短语列表：",
        "protection_enabled": "🟢 保护已启用。",
        "protection_disabled": "🔴 保护已禁用。",
        "protection_status": "🧩 保护状态：{status}",
        "changelog_setup_completed": "✅ 更新日志设置已完成",
        "changelog_setup_failed": "❌ 更新日志设置失败",
        "no_changelog_file": "❌ 您在根目录中没有 CHANGELOG.md 文件",
        "changelog_translated": "✅ 已成功将 CHANGELOG 翻译为 {count} 种语言",
        "no_changelog_translated": "❌ 没有 CHANGELOG 文件被成功翻译",
        "languages_removed": "🎉 语言已成功移除：{langs}",
        "all_languages_removed": "🎉 所有翻译文件已成功移除",
        "auto_setup_changelog": "🔧 正在自动设置 README 中的更新日志部分...",
        "checking_changelog_spacing": "🔧 正在检查更新日志部分间距...",
        "no_valid_language": "❌ 未提供有效的语言代码。",
        "language_not_recognized": "❌ 语言代码 '{code}' 无法识别。继续...",
        "file_not_found": "⚠️ 文件 {filename} 未找到",
        "folder_not_empty": "⚠️ 文件夹 {folder} 不为空，未删除",
        "failed_delete_file": "❌ 删除 {filename} 失败：{error}",
        "failed_delete_folder": "❌ 删除文件夹失败：{error}",
        "failed_update_main": "❌ 更新主 README 失败：{error}",
        "failed_translate_changelog": "❌ 翻译 CHANGELOG 失败：{error}",
        "failed_update_changelog_links": "❌ 在 {filename} 中更新更新日志链接失败：{error}",
        "failed_update_switcher": "❌ 在 {filename} 中更新语言切换器失败：{error}",
        "translation_failed": "❌ 翻译失败：{error}",
        "reading_package_error": "❌ 读取 package.json 时出错：{error}",
        "reading_git_error": "❌ 读取 .git/config 时出错：{error}",
        "reading_github_error": "❌ 在 README 中搜索 GitHub URL 时出错：{error}",
        "changelog_section_exists": "ℹ️ 更新日志部分已存在于 README.md 中",
        "no_changelog_file_root": "❌ 在根目录中未找到 CHANGELOG.md 文件",
        "no_translation_files": "ℹ️ 未找到翻译的 README 文件",
        "language_not_supported": "⚠️ 显示语言 '{code}' 不受支持，使用默认值",
        "help_description": "MultiDoc Translator - 自动化多语言文档翻译器",
        "help_epilog": """
示例：
  # 将 README 翻译为日语和中文
  python multidoc_translator.py --lang jp,zh

  # 仅将 CHANGELOG 翻译为所有语言，使用日语通知
  python multidoc_translator.py --translate-changelog all --display jp

  # 删除特定语言文件
  python multidoc_translator.py --remove-lang jp,zh

  # 自动设置 README 中的更新日志部分
  python multidoc_translator.py --auto-setup-changelog

  # 检测 GitHub 仓库 URL
  python multidoc_translator.py --detect-github-url
        """,
        "help_lang": "要翻译的语言代码（逗号分隔）。支持：pl, zh, jp, de, fr, es, ru, pt, id, kr",
        "help_remove_lang": "删除特定翻译语言文件（逗号分隔）",
        "help_remove_all_lang": "删除所有翻译文件并清理文件夹",
        "help_add_protect": "添加短语到保护列表（支持正则表达式模式）",
        "help_remove_protect": "从保护列表中删除短语",
        "help_list_protect": "显示所有当前受保护的短语",
        "help_init_protect": "将 protected_phrases.json 重置为默认值",
        "help_enable_protect": "在翻译期间启用短语保护",
        "help_disable_protect": "在翻译期间禁用短语保护",
        "help_status_protect": "检查短语保护当前是否启用",
        "help_translate_changelog": "仅翻译 CHANGELOG.md（对所有语言使用 'all' 或指定代码）",
        "help_auto_setup_changelog": "如果 CHANGELOG.md 存在，则自动将更新日志部分添加到 README.md",
        "help_detect_github_url": "从各种来源检测并显示 GitHub 仓库 URL",
        "help_display": "终端通知的显示语言 (en, id, jp, de, es, fr, kr, pl, pt, ru, zh)"
    }
}

# Global variable for display language - CHANGED TO ENGLISH AS DEFAULT
DISPLAY_LANG = "en"  # default changed to English

def set_display_language(lang_code):
    """Set display language for notifications"""
    global DISPLAY_LANG
    if lang_code in DISPLAY_LANGUAGES:
        DISPLAY_LANG = lang_code
    else:
        print(DISPLAY_LANGUAGES["en"]["language_not_supported"].format(code=lang_code))

def t(key, **kwargs):
    """Translation function for notifications"""
    return DISPLAY_LANGUAGES[DISPLAY_LANG][key].format(**kwargs)

# ---------------------- LANGUAGE SETTINGS ----------------------
LANGUAGES = {
    "pl": ("Polski", "pl", "🌐 Dostępne w innych językach:"),
    "zh": ("中文", "zh-CN", "🌐 提供其他语言版本："),
    "jp": ("日本語", "ja", "🌐 他の言語でも利用可能:"),
    "de": ("Deutsch", "de", "🌐 In anderen Sprachen verfügbar:"),
    "fr": ("Français", "fr", "🌐 Disponible dans d'autres langues :"),
    "es": ("Español", "es", "🌐 Disponible en otros idiomas:"),
    "ru": ("Русский", "ru", "🌐 Доступно na innych językach:"),
    "pt": ("Português", "pt", "🌐 Disponível em outros idiomas:"),
    "id": ("Bahasa Indonesia", "id", "🌐 Tersedia dalam bahasa lain:"),
    "kr": ("한국어", "ko", "🌐 다른 언어로도 사용 가능:"),
}

DEFAULT_PROTECTED = {
    "protected_phrases": [
        r"MIT\s+License(?:\s*©)?(?:\s*\d{4})?",
        r"https?:\/\/\S+",
        r"\(LICENSE\)",
        r"\(\.\./\.\./LICENSE\)",
        r"\*\*1\.85\.0\*\*",
        r"\*\*Windows\*\*",
        r"\*\*macOS\*\*", 
        r"\*\*Linux\*\*",
        r"\*\*Windows,\s*macOS\s*et\s*Linux\*\*",
        r"Visual Studio Code",
        r"VS Code",
        r"Google Translate",
        r"API",
        r"GitHub",
        r"README\.md",
        r"CHANGELOG\.md",
        r"Markdown"
    ]
}

# ---------------------- GITHUB URL DETECTION ----------------------
def get_github_repo_url():
    """Detect GitHub repository URL from various sources"""
    # Try from package.json first
    try:
        if os.path.exists(PACKAGE_JSON):
            with open(PACKAGE_JSON, "r", encoding="utf-8") as f:
                package_data = json.load(f)
            
            if package_data.get("repository"):
                repo_url = ""
                if isinstance(package_data["repository"], str):
                    repo_url = package_data["repository"]
                elif isinstance(package_data["repository"], dict) and package_data["repository"].get("url"):
                    repo_url = package_data["repository"]["url"]
                
                # Normalize URL
                if repo_url:
                    # Handle git+https:// format
                    repo_url = repo_url.replace("git+", "")
                    # Handle git@github.com: format
                    repo_url = repo_url.replace("git@github.com:", "https://github.com/")
                    # Handle .git suffix
                    repo_url = repo_url.replace(".git", "")
                    # Ensure it's a GitHub URL
                    if "github.com" in repo_url:
                        return repo_url
    except Exception as e:
        print(t("reading_package_error", error=e))
    
    # Try from .git/config
    try:
        git_config_path = os.path.join(".git", "config")
        if os.path.exists(git_config_path):
            with open(git_config_path, "r", encoding="utf-8") as f:
                git_config = f.read()
            
            url_match = re.search(r'url\s*=\s*(.+)', git_config)
            if url_match and url_match.group(1):
                repo_url = url_match.group(1).strip()
                # Normalize URL
                repo_url = repo_url.replace("git@github.com:", "https://github.com/")
                repo_url = repo_url.replace(".git", "")
                if "github.com" in repo_url:
                    return repo_url
    except Exception as e:
        print(t("reading_git_error", error=e))
    
    # Fallback: search in README.md
    try:
        if os.path.exists(SOURCE_FILE):
            with open(SOURCE_FILE, "r", encoding="utf-8") as f:
                readme_content = f.read()
            
            github_url_match = re.search(r'https://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-_.]+', readme_content)
            if github_url_match:
                return github_url_match.group(0)
    except Exception as e:
        print(t("reading_github_error", error=e))
    
    return None

def get_github_releases_url():
    """Generate GitHub Releases URL from repository URL"""
    repo_url = get_github_repo_url()
    if repo_url:
        return f"{repo_url}/releases"
    
    # Fallback default (for this extension itself)
    return "https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/releases"

def detect_github_url():
    """Function to detect and display GitHub URL"""
    repo_url = get_github_repo_url()
    releases_url = get_github_releases_url()
    
    if repo_url:
        print(t("github_url_detected"))
        print(t("repo_url", url=repo_url))
        print(t("releases_url", url=releases_url))
        print("\n" + t("sources_checked"))
        print("• package.json (repository field)")
        print("• .git/config")
        print("• README.md (GitHub URL patterns)")
        return True
    else:
        print(t("no_github_url"))
        print("\nPlease check:")
        print("• package.json has 'repository' field")
        print("• .git/config has remote URL") 
        print("• Or add GitHub URL manually to README")
        return False

# ---------------------- PROTECTION UTILITIES ----------------------
def load_protected_phrases():
    if not os.path.exists(PROTECTED_FILE):
        save_protected_phrases(DEFAULT_PROTECTED)
    with open(PROTECTED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_protected_phrases(data):
    with open(PROTECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_protect_enabled():
    return os.path.exists(PROTECT_STATUS_FILE)

def set_protect_status(enabled):
    if enabled:
        open(PROTECT_STATUS_FILE, "w").close()
    else:
        if os.path.exists(PROTECT_STATUS_FILE):
            os.remove(PROTECT_STATUS_FILE)

# ---------------------- CHANGELOG DETECTION ----------------------
def has_changelog_file():
    """Check if CHANGELOG.md file exists in root"""
    return os.path.exists(CHANGELOG_FILE)

def has_changelog_section_in_readme():
    """Check if README.md has Changelog section"""
    if not os.path.exists(SOURCE_FILE):
        return False
    
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check patterns for Changelog section
    patterns = [
        r"##\s+🧾\s+Changelog",
        r"##\s+Changelog",
        r"#+\s+Changelog",
        r"##\s+📝\s+Changelog",  # Tambahkan pattern alternatif
        r"##\s+.*[Cc]hangelog"   # Pattern lebih fleksibel
    ]
    
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    
    return False

def fix_existing_changelog_spacing():
    """Fix spacing and separators for existing Changelog section"""
    if not has_changelog_section_in_readme():
        return False
    
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        changes_made = False
        
        # 1. Fix pattern: --- directly followed by ## 🧾 Changelog
        # Becomes: --- + 1 empty line + ## 🧾 Changelog
        old_pattern = r'---\s*\n\s*## 🧾 Changelog'
        new_pattern = '---\n\n## 🧾 Changelog'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_pattern, content)
            changes_made = True
        
        # 2. Check if there's separator between Changelog and License
        if '## 🧾 Changelog' in content and '## 🧾 License' in content:
            # Check if there's --- between Changelog and License
            between_sections = re.search(r'## 🧾 Changelog.*?(## 🧾 License)', content, re.DOTALL)
            if between_sections:
                section_content = between_sections.group(0)
                if '---' not in section_content:
                    # Add --- before License
                    content = re.sub(
                        r'(## 🧾 Changelog.*?)(## 🧾 License)',
                        r'\1\n\n---\n\n\2',
                        content,
                        flags=re.DOTALL
                    )
                    changes_made = True
        
        if changes_made:
            with open(SOURCE_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(t("changelog_spacing_fixed"))
            return True
        
        return False
        
    except Exception as e:
        print(t("failed_update_main", error=e))
        return False

def add_changelog_section_to_readme():
    """Add Changelog section to README.md if not exists with proper spacing and separators"""
    if not has_changelog_file():
        print(t("no_changelog_file_root"))
        return False
    
    if has_changelog_section_in_readme():
        print(t("changelog_section_exists"))
        # Fix spacing if already exists
        fix_existing_changelog_spacing()
        return True
    
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Get dynamic GitHub Releases URL
        github_releases_url = get_github_releases_url()
        
        # Find position before License section to add Changelog
        license_pattern = r'##\s+🧾\s+License'
        license_match = re.search(license_pattern, content, re.IGNORECASE)
        
        # Changelog section with correct format including separators
        changelog_section = f"""

---

## 🧾 Changelog

See all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.

> 📦 You can also view release notes directly on the [GitHub Releases page]({github_releases_url}).

"""
        
        if license_match:
            # Insert before License section
            position = license_match.start()
            
            # Check if there's already --- before License
            content_before_license = content[:position].rstrip()
            if content_before_license.endswith('---'):
                # If there's already ---, we only need to add Changelog section
                # Remove existing --- and replace with complete section
                last_dash_pos = content_before_license.rfind('---')
                new_content = content[:last_dash_pos].rstrip() + changelog_section + content[position:]
            else:
                # If no ---, add complete section with ---
                new_content = content[:position] + changelog_section + content[position:]
        else:
            # Add at end of file before License if exists
            if "## 🧾 License" in content:
                license_pos = content.find("## 🧾 License")
                content_before_license = content[:license_pos].rstrip()
                
                if content_before_license.endswith('---'):
                    # If there's already ---, replace with complete section
                    last_dash_pos = content_before_license.rfind('---')
                    new_content = content[:last_dash_pos].rstrip() + changelog_section + content[license_pos:]
                else:
                    # If no ---, add complete section
                    new_content = content[:license_pos] + changelog_section + content[license_pos:]
            else:
                # Add at end of file with separator
                if content.strip().endswith('---'):
                    new_content = content.rstrip() + f'\n\n## 🧾 Changelog\n\nSee all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.\n\n> 📦 You can also view release notes directly on the [GitHub Releases page]({github_releases_url}).'
                else:
                    new_content = content.strip() + f'\n\n---\n\n## 🧾 Changelog\n\nSee all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.\n\n> 📦 You can also view release notes directly on the [GitHub Releases page]({github_releases_url}).'
        
        # Final cleanup: ensure correct format
        # Pattern: --- followed by 1 empty line, then ## 🧾 Changelog
        new_content = re.sub(r'---\s*\n\s*## 🧾 Changelog', '---\n\n## 🧾 Changelog', new_content)
        
        # Also ensure there's --- before License
        if '## 🧾 Changelog' in new_content and '## 🧾 License' in new_content:
            # Check if there's --- between Changelog and License
            between_sections = re.search(r'## 🧾 Changelog.*?(## 🧾 License)', new_content, re.DOTALL)
            if between_sections:
                section_content = between_sections.group(0)
                if '---' not in section_content:
                    # Add --- before License
                    new_content = re.sub(
                        r'(## 🧾 Changelog.*?)(## 🧾 License)',
                        r'\1\n\n---\n\n\2',
                        new_content,
                        flags=re.DOTALL
                    )
        
        # Also fix if there are multiple empty lines
        new_content = re.sub(r'\n\n\n+', '\n\n', new_content)
        
        with open(SOURCE_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(t("changelog_section_added"))
        print(f"🔗 GitHub Releases URL: {github_releases_url}")
        return True
        
    except Exception as e:
        print(t("changelog_setup_failed"))
        return False

# ---------------------- TRANSLATION FUNCTIONS ----------------------
def translate_text(text, dest):
    if not text.strip():
        return text
    try:
        # Tambahkan timeout dan retry mechanism
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return GoogleTranslator(source="auto", target=dest).translate(text)
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retry
                    continue
                raise e
    except Exception as e:
        print(t("translation_failed", error=e))
        # Return original text instead of failing completely
        return text

def get_existing_translated_languages():
    """Get list of languages that already have README files"""
    existing_langs = []
    if not os.path.exists(OUTPUT_DIR):
        return existing_langs
        
    for code in LANGUAGES:
        # Special filename format for jp, zh, kr
        if code == "jp":
            readme_path = os.path.join(OUTPUT_DIR, "README-JP.md")
        elif code == "zh":
            readme_path = os.path.join(OUTPUT_DIR, "README-ZH.md")
        elif code == "kr":
            readme_path = os.path.join(OUTPUT_DIR, "README-KR.md")
        else:
            readme_path = os.path.join(OUTPUT_DIR, f"README-{code.upper()}.md")
            
        if os.path.exists(readme_path):
            existing_langs.append(code)
    return existing_langs

def update_language_switcher(new_languages=None, removed_languages=None):
    """Update language switcher in main README and all translated READMEs"""
    
    # Get all existing languages
    existing_langs = get_existing_translated_languages()
    
    # If there are new languages, add to existing list
    if new_languages:
        for lang in new_languages:
            if lang not in existing_langs:
                existing_langs.append(lang)
    
    # If there are removed languages, remove from existing list
    if removed_languages:
        for lang in removed_languages:
            if lang in existing_langs:
                existing_langs.remove(lang)
    
    # Update main README (English)
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Create link list for main README with desired order
        lang_links = []
        # Order: pl, zh, jp, de, fr, es, ru, pt, id, kr
        ordered_langs = ["pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"]
        ordered_existing = [lang for lang in ordered_langs if lang in existing_langs]
        
        for code in ordered_existing:
            if code in LANGUAGES:
                name = LANGUAGES[code][0]
                # Special filename format for links
                if code == "jp":
                    lang_links.append(f"[{name}](docs/lang/README-JP.md)")
                elif code == "zh":
                    lang_links.append(f"[{name}](docs/lang/README-ZH.md)")
                elif code == "kr":
                    lang_links.append(f"[{name}](docs/lang/README-KR.md)")
                else:
                    lang_links.append(f"[{name}](docs/lang/README-{code.upper()}.md)")
        
        if lang_links:
            switcher = f"> 🌐 Available in other languages: {' | '.join(lang_links)}\n"
            
            # Find and replace existing language switcher
            if "> 🌐 Available in other languages:" in content:
                # Replace only the language switcher part
                content = re.sub(
                    r'> 🌐 Available in other languages:.*', 
                    f'> 🌐 Available in other languages: {" | ".join(lang_links)}', 
                    content
                )
            else:
                # Add new one before ---
                match = re.search(r"\n-{3,}\n", content)
                if match:
                    position = match.start()
                    content = content[:position] + "\n" + switcher + content[position:]
                else:
                    content = content.strip() + "\n" + switcher
        else:
            # Remove language switcher if no other languages (including excess empty lines)
            content = re.sub(r'> 🌐 Available in other languages:.*\n', '', content)
            # Remove remaining excess empty lines
            content = re.sub(r'\n\n\n', '\n\n', content)
            content = re.sub(r'\n\n\n', '\n\n', content)
        
        with open(SOURCE_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(t("language_switcher_updated", filename="main README"))
        if ordered_existing:
            print(f"   Languages: {', '.join(ordered_existing)}")
        else:
            print(f"   {t('no_translation_files')}")
    
    except Exception as e:
        print(t("failed_update_switcher", filename="main README", error=e))
    
    # Update all translated READMEs
    for lang_code in existing_langs:
        if lang_code in LANGUAGES:
            lang_name, _, intro_text = LANGUAGES[lang_code]
            # Special filename format for jp, zh, kr
            if lang_code == "jp":
                readme_path = os.path.join(OUTPUT_DIR, "README-JP.md")
            elif lang_code == "zh":
                readme_path = os.path.join(OUTPUT_DIR, "README-ZH.md")
            elif lang_code == "kr":
                readme_path = os.path.join(OUTPUT_DIR, "README-KR.md")
            else:
                readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
            
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Create link list for this language (all languages except itself)
                    links = ["[English](../../README.md)"]
                    # Order: pl, zh, jp, de, fr, es, ru, pt, id, kr
                    ordered_langs = ["pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"]
                    ordered_others = [code for code in ordered_langs if code in existing_langs and code != lang_code]
                    
                    for code in ordered_others:
                        name = LANGUAGES[code][0]
                        # Special filename format for links
                        if code == "jp":
                            links.append(f"[{name}](README-JP.md)")
                        elif code == "zh":
                            links.append(f"[{name}](README-ZH.md)")
                        elif code == "kr":
                            links.append(f"[{name}](README-KR.md)")
                        else:
                            links.append(f"[{name}](README-{code.upper()}.md)")
                    
                    links_text = " | ".join(links)
                    new_switcher_line = f"> {intro_text} {links_text}"
                    
                    # Find and replace existing language switcher
                    escaped_intro = re.escape(intro_text)
                    if f"> {intro_text}" in content:
                        # Replace only the language switcher part
                        content = re.sub(
                            fr'> {escaped_intro}.*', 
                            new_switcher_line, 
                            content
                        )
                    else:
                        # Add new one before ---
                        match = re.search(r"\n-{3,}\n", content)
                        if match:
                            position = match.start()
                            content = content[:position] + "\n" + new_switcher_line + "\n" + content[position:]
                    
                    with open(readme_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(t("language_switcher_updated", filename=f"README-{lang_code.upper()}"))
                
                except Exception as e:
                    print(t("failed_update_switcher", filename=f"README-{lang_code.upper()}", error=e))

def remove_language_files(lang_codes):
    """Remove README files for specific languages and update language switcher"""
    removed_langs = []
    
    for lang_code in lang_codes:
        if lang_code in LANGUAGES:
            # Special filename format for jp, zh, kr
            if lang_code == "jp":
                readme_path = os.path.join(OUTPUT_DIR, "README-JP.md")
                changelog_path = os.path.join(OUTPUT_DIR, "CHANGELOG-JP.md")
            elif lang_code == "zh":
                readme_path = os.path.join(OUTPUT_DIR, "README-ZH.md")
                changelog_path = os.path.join(OUTPUT_DIR, "CHANGELOG-ZH.md")
            elif lang_code == "kr":
                readme_path = os.path.join(OUTPUT_DIR, "README-KR.md")
                changelog_path = os.path.join(OUTPUT_DIR, "CHANGELOG-KR.md")
            else:
                readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
                changelog_path = os.path.join(OUTPUT_DIR, f"CHANGELOG-{lang_code.upper()}.md")
            
            # Remove README file
            if os.path.exists(readme_path):
                try:
                    os.remove(readme_path)
                    removed_langs.append(lang_code)
                    print(t("file_deleted", filename=os.path.basename(readme_path)))
                except Exception as e:
                    print(t("failed_delete_file", filename=os.path.basename(readme_path), error=e))
            else:
                print(t("file_not_found", filename=os.path.basename(readme_path)))
            
            # Remove CHANGELOG file if exists
            if os.path.exists(changelog_path):
                try:
                    os.remove(changelog_path)
                    print(t("file_deleted", filename=os.path.basename(changelog_path)))
                except Exception as e:
                    print(t("failed_delete_file", filename=os.path.basename(changelog_path), error=e))
        else:
            print(t("language_not_recognized", code=lang_code))
    
    # Update language switcher after removing files
    if removed_langs:
        update_language_switcher(removed_languages=removed_langs)
        
        # Remove docs/lang folder if empty, then docs if also empty
        if not get_existing_translated_languages():
            try:
                if os.path.exists(OUTPUT_DIR) and not os.listdir(OUTPUT_DIR):
                    shutil.rmtree(OUTPUT_DIR)
                    print(t("folder_deleted", folder=OUTPUT_DIR))
                    
                    # Check if docs folder is also empty, if yes remove
                    docs_dir = os.path.dirname(OUTPUT_DIR)
                    if os.path.exists(docs_dir) and not os.listdir(docs_dir):
                        shutil.rmtree(docs_dir)
                        print(t("folder_deleted", folder=docs_dir))
            except Exception as e:
                print(t("failed_delete_folder", error=e))
    
    return removed_langs

def remove_all_language_files():
    """Remove all translated README files and docs/lang folder and docs if empty"""
    existing_langs = get_existing_translated_languages()
    
    if not existing_langs:
        print(t("no_translation_files"))
        return
    
    # Remove all README and CHANGELOG files
    for lang_code in existing_langs:
        # Special filename format for jp, zh, kr
        if lang_code == "jp":
            readme_path = os.path.join(OUTPUT_DIR, "README-JP.md")
            changelog_path = os.path.join(OUTPUT_DIR, "CHANGELOG-JP.md")
        elif lang_code == "zh":
            readme_path = os.path.join(OUTPUT_DIR, "README-ZH.md")
            changelog_path = os.path.join(OUTPUT_DIR, "CHANGELOG-ZH.md")
        elif lang_code == "kr":
            readme_path = os.path.join(OUTPUT_DIR, "README-KR.md")
            changelog_path = os.path.join(OUTPUT_DIR, "CHANGELOG-KR.md")
        else:
            readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
            changelog_path = os.path.join(OUTPUT_DIR, f"CHANGELOG-{lang_code.upper()}.md")
        
        try:
            if os.path.exists(readme_path):
                os.remove(readme_path)
                print(t("file_deleted", filename=os.path.basename(readme_path)))
            
            if os.path.exists(changelog_path):
                os.remove(changelog_path)
                print(t("file_deleted", filename=os.path.basename(changelog_path)))
        except Exception as e:
            print(t("failed_delete_file", filename=f"for {lang_code}", error=e))
    
    # Remove docs/lang folder if empty, then docs if also empty
    try:
        if os.path.exists(OUTPUT_DIR):
            if not os.listdir(OUTPUT_DIR):
                shutil.rmtree(OUTPUT_DIR)
                print(t("folder_deleted", folder=OUTPUT_DIR))
                
                # Check if docs folder is also empty, if yes remove
                docs_dir = os.path.dirname(OUTPUT_DIR)
                if os.path.exists(docs_dir) and not os.listdir(docs_dir):
                    shutil.rmtree(docs_dir)
                    print(t("folder_deleted", folder=docs_dir))
            else:
                print(t("folder_not_empty", folder=OUTPUT_DIR))
    except Exception as e:
        print(t("failed_delete_folder", error=e))
    
    # Update main README to remove language switcher and clean up empty lines
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove language switcher
        content = re.sub(r'> 🌐 Available in other languages:.*\n', '', content)
        
        # Clean up excess empty lines
        content = re.sub(r'\n\n\n', '\n\n', content)
        content = re.sub(r'\n\n\n', '\n\n', content)
        
        with open(SOURCE_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(t("language_switcher_updated", filename="main README"))
    
    except Exception as e:
        print(t("failed_update_main", error=e))

def protect_specific_phrases(text, lang_code):
    """Special protection for important phrases after translation"""
    
    # Protection for version
    text = re.sub(r'(\*\*)?1\.85\.0(\*\*)?', '**1.85.0**', text)
    
    # Protection for operating systems
    text = re.sub(r'(\*\*)?Windows(\*\*)?', '**Windows**', text, flags=re.IGNORECASE)
    text = re.sub(r'(\*\*)?macOS(\*\*)?', '**macOS**', text, flags=re.IGNORECASE)
    text = re.sub(r'(\*\*)?Linux(\*\*)?', '**Linux**', text, flags=re.IGNORECASE)
    
    # Special protection for OS list format
    text = re.sub(r'\*\*Windows\*\*,?\s*\*\*macOS\*\*,?\s*(et|and|und|y|и)\s*\*\*Linux\*\*', '**Windows**, **macOS** et **Linux**', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*Windows\*\*,?\s*\*\*macOS\*\*,?\s*\*\*Linux\*\*', '**Windows**, **macOS** et **Linux**', text, flags=re.IGNORECASE)
    
    return text

# ---------------------- CHANGELOG TRANSLATION ----------------------
def translate_changelog(lang_code, lang_info, protected):
    """Translate CHANGELOG.md file to target language"""
    if not has_changelog_file():
        return False
    
    lang_name, translate_code, _ = lang_info
    # Special filename format for jp, zh, kr
    if lang_code == "jp":
        changelog_dest_path = os.path.join(OUTPUT_DIR, "CHANGELOG-JP.md")
    elif lang_code == "zh":
        changelog_dest_path = os.path.join(OUTPUT_DIR, "CHANGELOG-ZH.md")
    elif lang_code == "kr":
        changelog_dest_path = os.path.join(OUTPUT_DIR, "CHANGELOG-KR.md")
    else:
        changelog_dest_path = os.path.join(OUTPUT_DIR, f"CHANGELOG-{lang_code.upper()}.md")
    
    print(t("translating_changelog", lang_name=lang_name, lang_code=lang_code.upper()))
    
    try:
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            changelog_content = f.read()
        
        # Separate CHANGELOG header and body
        parts = re.split(r'\n-{3,}\n', changelog_content, 1)
        changelog_header = parts[0] if len(parts) > 0 else ""
        changelog_body = parts[1] if len(parts) > 1 else ""
        
        # Translate CHANGELOG title
        translated_title = translate_text("Changelog", translate_code)
        
        # Create translated header
        if "# Changelog" in changelog_header:
            translated_header = changelog_header.replace("# Changelog", f"# {translated_title}")
        else:
            translated_header = f"# {translated_title}\n\n{changelog_header}"
        
        # Process CHANGELOG body translation
        body_lines = changelog_body.split("\n")
        translated_lines = []
        in_code_block = False
        
        for line in body_lines:
            # Detect code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                translated_lines.append(line)
                continue
            
            # If in code block, don't translate
            if in_code_block:
                translated_lines.append(line)
                continue
            
            # Detect version (format: ## [1.0.0] - 2024-01-01)
            version_match = re.match(r'^(##\s+\[[\d\.]+\]\s*-\s*\d{4}-\d{2}-\d{2})', line)
            if version_match:
                translated_lines.append(line)  # Don't translate version line
                continue
            
            # Detect structural elements
            is_structural = (
                re.match(r"^\s*[-=]+\s*$", line) or  # Separator lines
                not line.strip() or                   # Empty lines
                re.match(r"^\s*\[.*?\]:\s*", line)   # Link references
            )
            
            if is_structural:
                translated_lines.append(line)
                continue
            
            # Protect text before translation
            temp_line = line
            placeholders = {}
            counter = 0
            
            def protect(pattern, text, flags=0):
                nonlocal counter
                def repl(m):
                    nonlocal counter
                    key = f"__p{counter}__"
                    placeholders[key] = m.group(0)
                    counter += 1
                    return key
                return re.sub(pattern, repl, text, flags=flags)
            
            # Protection for all important patterns
            if is_protect_enabled():
                for p in protected["protected_phrases"]:
                    temp_line = protect(p, temp_line)
            
            # Additional protection specifically for CHANGELOG
            temp_line = protect(r"https?://[^\s\)]+", temp_line)           # URLs
            temp_line = protect(r"`[^`]+`", temp_line)                     # Inline code
            temp_line = protect(r"\[.*?\]\([^)]+\)", temp_line)            # Markdown links
            temp_line = protect(r"\[[\d\.]+\]:\s*\S+", temp_line)          # Version links
            
            # Translate text
            translated = translate_text(temp_line, translate_code)
            
            # Restore placeholders to original text
            for key, val in placeholders.items():
                translated = translated.replace(key, val)
            
            translated_lines.append(translated)
        
        translated_body = "\n".join(translated_lines)
        
        # Combine header and body
        final_changelog = f"{translated_header}\n\n---\n{translated_body}"
        
        # Cleanup remaining placeholders
        final_changelog = re.sub(r"__p\d+__", "", final_changelog)
        
        # Write translated CHANGELOG file
        with open(changelog_dest_path, "w", encoding="utf-8") as f:
            f.write(final_changelog)
        
        print(t("changelog_created", path=changelog_dest_path))
        return True
        
    except Exception as e:
        print(t("failed_translate_changelog", error=e))
        return False

def update_changelog_links_in_readme(lang_code, lang_info):
    """Update CHANGELOG links in translated README"""
    # Special filename format for jp, zh, kr
    if lang_code == "jp":
        readme_path = os.path.join(OUTPUT_DIR, "README-JP.md")
        changelog_dest_path = "CHANGELOG-JP.md"
    elif lang_code == "zh":
        readme_path = os.path.join(OUTPUT_DIR, "README-ZH.md")
        changelog_dest_path = "CHANGELOG-ZH.md"
    elif lang_code == "kr":
        readme_path = os.path.join(OUTPUT_DIR, "README-KR.md")
        changelog_dest_path = "CHANGELOG-KR.md"
    else:
        readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
        changelog_dest_path = f"CHANGELOG-{lang_code.upper()}.md"
    
    if not os.path.exists(readme_path):
        return
    
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Translate "Changelog" and "release notes" text
        _, translate_code, _ = lang_info
        translated_changelog = translate_text("Changelog", translate_code)
        translated_release_notes = translate_text("release notes", translate_code)
        translated_view = translate_text("view", translate_code)
        translated_also = translate_text("also", translate_code)
        translated_you_can = translate_text("You can", translate_code)
        
        # Get dynamic GitHub Releases URL
        github_releases_url = get_github_releases_url()
        
        # Update Changelog section title
        content = re.sub(
            r'##\s+🧾\s+Changelog',
            f'## 🧾 {translated_changelog}',
            content,
            flags=re.IGNORECASE
        )
        
        # Update link to translated CHANGELOG file
        content = re.sub(
            r'\[CHANGELOG\.md\]\(CHANGELOG\.md\)',
            f'[{translated_changelog}]({changelog_dest_path})',
            content
        )
        
        # Update release notes text with dynamic URL
        old_release_pattern = r'You can also view release notes directly on the \[GitHub Releases page\]\([^)]+\)'
        new_release_text = f'{translated_you_can} {translated_also} {translated_view} {translated_release_notes} directly on the [GitHub Releases page]({github_releases_url})'
        
        content = re.sub(old_release_pattern, new_release_text, content, flags=re.IGNORECASE)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(t("changelog_links_updated", filename=f"README-{lang_code.upper()}"))
        
    except Exception as e:
        print(t("failed_update_changelog_links", filename=f"README-{lang_code.upper()}", error=e))

def translate_changelog_only(lang_codes=None):
    """Translate only CHANGELOG without README"""
    if not has_changelog_file():
        print(t("no_changelog_file"))
        return False
    
    protected = load_protected_phrases()
    
    # If no languages specified, use all languages
    if not lang_codes:
        lang_codes = LANGUAGES.keys()
    
    success_count = 0
    for lang_code in lang_codes:
        if lang_code in LANGUAGES:
            if translate_changelog(lang_code, LANGUAGES[lang_code], protected):
                success_count += 1
                
                # Update links in README if it exists
                update_changelog_links_in_readme(lang_code, LANGUAGES[lang_code])
            
            time.sleep(1)  # Delay to avoid rate limiting
    
    if success_count > 0:
        print(t("changelog_translated", count=success_count))
        return True
    else:
        print(t("no_changelog_translated"))
        return False

# ---------------------- MAIN README TRANSLATION FUNCTION ----------------------
def translate_readme(lang_code, lang_info, protected):
    lang_name, translate_code, intro_text = lang_info
    
    # Special filename format for jp, zh, kr
    if lang_code == "jp":
        dest_path = os.path.join(OUTPUT_DIR, "README-JP.md")
    elif lang_code == "zh":
        dest_path = os.path.join(OUTPUT_DIR, "README-ZH.md")
    elif lang_code == "kr":
        dest_path = os.path.join(OUTPUT_DIR, "README-KR.md")
    else:
        dest_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        src_text = f.read()

    parts = re.split(r'\n-{3,}\n', src_text, 1)
    src_header, src_body = (parts[0], parts[1]) if len(parts) > 1 else (src_text, "")

    # Clean existing language switcher from header
    cleaned_header = re.sub(r'^\s*>\s*🌐.*$', '', src_header, flags=re.MULTILINE).strip()
    
    # Get all existing languages to create language switcher
    existing_langs = get_existing_translated_languages()
    
    # Create language switcher for this language
    links = ["[English](../../README.md)"]
    for code in existing_langs:
        if code != lang_code:
            name = LANGUAGES[code][0]
            # Special filename format for links
            if code == "jp":
                links.append(f"[{name}](README-JP.md)")
            elif code == "zh":
                links.append(f"[{name}](README-ZH.md)")
            elif code == "kr":
                links.append(f"[{name}](README-KR.md)")
            else:
                links.append(f"[{name}](README-{code.upper()}.md)")
    
    links_text = " | ".join(links)
    final_header = f"{cleaned_header}\n\n> {intro_text} {links_text}"

    print(t("translating_readme", lang_name=lang_name, lang_code=lang_code.upper()))

    body_lines = src_body.split("\n")
    translated_lines = []
    in_code_block = False
    in_example_block = False
    in_table = False
    table_header_processed = False

    for i, line in enumerate(body_lines):
        # Detect code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue

        # Detect tables
        if re.match(r'^\|.*\|$', line) and not in_code_block:
            if not in_table:
                in_table = True
                table_header_processed = False
            
            # Table separator row (---|---|)
            if re.match(r'^\|?[\s:-]+\|[\s:-]+\|[\s:-]+\|?$', line):
                translated_lines.append(line)
                table_header_processed = True
                continue
            
            # FIX: Table header NOT translated, copied directly
            if in_table and not table_header_processed:
                translated_lines.append(line)  # Table header not translated
                table_header_processed = True
            else:
                # Table data rows, not translated
                translated_lines.append(line)
            continue
        else:
            # Exit table mode
            if in_table:
                in_table = False
                table_header_processed = False

        # Detect example sections (Before/After)
        if re.match(r'^\*\*Before:\*\*$', line, re.IGNORECASE):
            in_example_block = True
            # Translate "Before:" according to target language
            translated_before = translate_text("Before:", translate_code)
            translated_lines.append(f"**{translated_before}**")
            continue
        
        if re.match(r'^\*\*After \(Translated\):\*\*$', line, re.IGNORECASE):
            in_example_block = True
            # Translate "After (Translated):" according to target language
            translated_after = translate_text("After (Translated):", translate_code)
            translated_lines.append(f"**{translated_after}**")
            continue

        # If in code block or example, don't translate code content
        if in_code_block or in_example_block:
            translated_lines.append(line)
            # Reset example block status if finding empty line after example
            if in_example_block and not line.strip():
                in_example_block = False
            continue

        # Detect structural elements (empty lines, etc)
        is_structural = (re.match(r"^\s*\|?[-:|\s]+\|?\s*$", line) or 
                        not line.strip())
        if is_structural:
            translated_lines.append(line)
            continue

        temp_line = line
        placeholders = {}
        counter = 0

        def protect(pattern, text, flags=0):
            nonlocal counter
            def repl(m):
                nonlocal counter
                key = f"__p{counter}__"
                placeholders[key] = m.group(0)
                counter += 1
                return key
            return re.sub(pattern, repl, text, flags=flags)

        # Protection for all important patterns
        if is_protect_enabled():
            for p in protected["protected_phrases"]:
                temp_line = protect(p, temp_line)

        # Additional protection for important components
        temp_line = protect(r"\[.*?\]\(https?://[^\)]+\)", temp_line)  # Markdown links with URL
        temp_line = protect(r"\[.*?\]\(mailto:[^\)]+\)", temp_line)     # Email links
        temp_line = protect(r"https?://[^\s\)]+", temp_line)           # URL standalone
        temp_line = protect(r"MIT\s+License", temp_line, re.IGNORECASE)  # MIT License
        temp_line = protect(r"\(LICENSE\)", temp_line)                   # (LICENSE)
        temp_line = protect(r"\(\.\./\.\./LICENSE\)", temp_line)         # (../../LICENSE)
        temp_line = protect(r"`[^`]+`", temp_line)                       # Inline code
        temp_line = protect(r"`auto-translate-readmes\.run`", temp_line) # Command ID
        
        # Special protection for version and operating systems
        temp_line = protect(r"\*\*1\.85\.0\*\*", temp_line)             # Specific version 1.85.0
        temp_line = protect(r"\*\*Windows\*\*", temp_line)              # Windows
        temp_line = protect(r"\*\*macOS\*\*", temp_line)                # macOS
        temp_line = protect(r"\*\*Linux\*\*", temp_line)                # Linux
        
        # Translate text
        translated = translate_text(temp_line, translate_code)

        # Restore placeholders to original text
        for key, val in placeholders.items():
            translated = translated.replace(key, val)

        translated_lines.append(translated)

    translated_body = "\n".join(translated_lines)
    
    # --- GENERIC FIXES ---
    # 1. Fix bullet points
    translated_body = re.sub(r'^-(?=\w)', '- ', translated_body, flags=re.MULTILINE)
    
    # 2. Fix non-breaking space
    translated_body = translated_body.replace('\xa0', ' ')
    
    # 3. FIX: Fix colon formatting WITHOUT breaking bold text
    translated_body = re.sub(
        r'(\w+)\s*:\s*(\*\*(?!.*\*\*:\*\*))',
        r'\1 : \2',
        translated_body
    )
    
    # 4. MAIN FIX: Fix extra parenthesis
    translated_body = re.sub(
        r'(\[.*?\]\([^)]+\)\.)\)',
        r'\1',
        translated_body
    )
    
    # 5. Fix bold format
    translated_body = re.sub(r'(\*\*)(\d+\.\d+\.\d+)(\*\*)', r'**\2**', translated_body)
    
    # 6. ADDITIONAL FIX: Fix bold text broken by colon formatting
    translated_body = re.sub(
        r'\*\*(\w+)\s*:\s*\*\*',
        r'**\1:**',
        translated_body
    )
    
    # Ensure LICENSE link remains consistent
    final_text = f"{final_header}\n\n---\n{translated_body}"
    final_text = re.sub(r"\(LICENSE\)", "(../../LICENSE)", final_text)
    final_text = re.sub(r"__p\d+__", "", final_text)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(t("readme_created", path=dest_path))

    # After successfully translating README, handle CHANGELOG
    if has_changelog_file() and has_changelog_section_in_readme():
        # Translate CHANGELOG
        translate_changelog(lang_code, lang_info, protected)
        
        # Update CHANGELOG link in translated README
        update_changelog_links_in_readme(lang_code, lang_info)

# ---------------------- MAIN PROGRAM ----------------------
def main():
    display_lang = "en"  # default
    
    # Cek parameter --display di command line
    for i, arg in enumerate(sys.argv):
        if arg == "--display" and i + 1 < len(sys.argv):
            display_lang = sys.argv[i + 1]
            break
        elif arg.startswith("--display="):
            display_lang = arg.split("=")[1]
            break
    
    # Gunakan bahasa help yang sesuai
    help_lang = display_lang if display_lang in DISPLAY_LANGUAGES else "en"
    
    # PERBAIKAN: Gunakan help_lang secara konsisten
    parser = argparse.ArgumentParser(
        description=DISPLAY_LANGUAGES[help_lang]["help_description"],
        epilog=DISPLAY_LANGUAGES[help_lang]["help_epilog"],
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # PERBAIKAN: Gunakan help_lang untuk semua help text
    parser.add_argument("--lang", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_lang"])
    
    parser.add_argument("--remove-lang", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_remove_lang"])
    
    parser.add_argument("--remove-all-lang", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_remove_all_lang"])
    
    parser.add_argument("--add-protect", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_add_protect"])
    
    parser.add_argument("--remove-protect", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_remove_protect"])
    
    parser.add_argument("--list-protect", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_list_protect"])
    
    parser.add_argument("--init-protect", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_init_protect"])
    
    parser.add_argument("--enable-protect", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_enable_protect"])
    
    parser.add_argument("--disable-protect", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_disable_protect"])
    
    parser.add_argument("--status-protect", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_status_protect"])
    
    parser.add_argument("--translate-changelog", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_translate_changelog"])
    
    parser.add_argument("--auto-setup-changelog", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_auto_setup_changelog"])
    
    parser.add_argument("--detect-github-url", 
                       action="store_true", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_detect_github_url"])
    
    parser.add_argument("--display", 
                       help=DISPLAY_LANGUAGES[help_lang]["help_display"], 
                       default="en",
                       choices=["en", "id", "jp", "de", "es", "fr", "kr", "pl", "pt", "ru", "zh"])
    
    args = parser.parse_args()

    # Set display language untuk notifikasi
    set_display_language(args.display)

    protected = load_protected_phrases()

    # Handle GitHub URL detection commands
    if args.detect_github_url:
        detect_github_url()
        return

    # Handle protection commands
    if args.init_protect:
        save_protected_phrases(DEFAULT_PROTECTED)
        print(t("protection_reset"))
        return
    if args.add_protect:
        protected["protected_phrases"].append(args.add_protect)
        save_protected_phrases(protected)
        print(t("phrase_added", phrase=args.add_protect))
        return
    if args.remove_protect:
        protected["protected_phrases"] = [p for p in protected["protected_phrases"] if p != args.remove_protect]
        save_protected_phrases(protected)
        print(t("phrase_removed", phrase=args.remove_protect))
        return
    if args.list_protect:
        print(t("protected_phrases_list"))
        for p in protected["protected_phrases"]:
            print(f"- {p}")
        return
    if args.enable_protect:
        set_protect_status(True)
        print(t("protection_enabled"))
        return
    if args.disable_protect:
        set_protect_status(False)
        print(t("protection_disabled"))
        return
    if args.status_protect:
        status = "ACTIVE ✅" if is_protect_enabled() else "INACTIVE ❌"
        print(t("protection_status", status=status))
        return

    # Handle CHANGELOG commands
    if args.auto_setup_changelog:
        if add_changelog_section_to_readme():
            print(t("changelog_setup_completed"))
        else:
            print(t("changelog_setup_failed"))
        return
    
    if args.translate_changelog:
        if not has_changelog_file():
            print(t("no_changelog_file"))
            return
        
        if args.translate_changelog.lower() == 'all':
            lang_codes = None  # Translate all languages
        else:
            lang_codes = [lang.strip().lower() for lang in args.translate_changelog.split(',')]
            # Validate language codes
            lang_codes = [code for code in lang_codes if code in LANGUAGES]
            
            if not lang_codes:
                print(t("no_valid_language"))
                return
        
        translate_changelog_only(lang_codes)
        return

    # Handle language file removal
    if args.remove_lang:
        lang_codes = [lang.strip() for lang in args.remove_lang.split(',')]
        removed = remove_language_files(lang_codes)
        if removed:
            print(t("languages_removed", langs=', '.join(removed)))
        return
    
    if args.remove_all_lang:
        remove_all_language_files()
        print(t("all_languages_removed"))
        return

    # Run translate (README + CHANGELOG automatically)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Auto setup changelog if CHANGELOG file exists but section not in README
    if has_changelog_file() and not has_changelog_section_in_readme():
        print(t("auto_setup_changelog"))
        add_changelog_section_to_readme()
    elif has_changelog_section_in_readme():
        # Fix spacing for existing section
        print(t("checking_changelog_spacing"))
        fix_existing_changelog_spacing()
    
    if args.lang:
        # Parse multiple languages if comma-separated
        lang_codes = [lang.strip() for lang in args.lang.split(',')]
        valid_langs = []
        
        for lang_code in lang_codes:
            if lang_code in LANGUAGES:
                valid_langs.append(lang_code)
            else:
                print(t("language_not_recognized", code=lang_code))
        
        if valid_langs:
            # Translate selected languages
            for code in valid_langs:
                translate_readme(code, LANGUAGES[code], protected)
                time.sleep(1)
            
            # Update language switcher for ALL existing languages (including new ones)
            update_language_switcher(valid_langs)
        else:
            print(t("no_valid_language"))
    else:
        # Translate all languages
        for code, info in tqdm(LANGUAGES.items(), desc="Translating all READMEs"):
            translate_readme(code, info, protected)
            time.sleep(1)
        
        # Update language switcher for all languages
        update_language_switcher()
    
    print("\n" + t("all_translated") + "\n")

if __name__ == "__main__":
    main()