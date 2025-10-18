import os
import re
import json
import time
import argparse
import shutil
from deep_translator import GoogleTranslator
from tqdm import tqdm

SOURCE_FILE = "README.md"
OUTPUT_DIR = "docs/lang"
PROTECTED_FILE = "protected_phrases.json"
PROTECT_STATUS_FILE = ".protect_status"

LANGUAGES = {
    "id": ("Bahasa Indonesia", "id", "🌐 Tersedia dalam bahasa lain:"),
    "fr": ("Français", "fr", "🌐 Disponible dans d'autres langues :"),
    "de": ("Deutsch", "de", "🌐 In anderen Sprachen verfügbar:"),
    "jp": ("日本語", "ja", "🌐 他の言語でも利用可能:"),
    "zh": ("中文", "zh-CN", "🌐 提供其他语言版本："),
    "es": ("Español", "es", "🌐 Disponible en otros idiomas:"),
    "pl": ("Polski", "pl", "🌐 Dostępne w innych językach:"),
    "ru": ("Русский", "ru", "🌐 Доступно на других языках:"),
    "pt": ("Português", "pt", "🌐 Disponível em outros idiomas:"),
    "ko": ("한국어", "ko", "🌐 다른 언어로도 사용 가능:"),
}

DEFAULT_PROTECTED = {
    "protected_phrases": [
        r"MIT\s+License(?:\s*©)?(?:\s*\d{4})?",
        r"https?:\/\/\S+",
        r"\(LICENSE\)",
        r"\(\.\./\.\./LICENSE\)"
    ]
}

# ---------------------- UTILITAS PROTEKSI ----------------------
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

# ---------------------- FUNGSI TERJEMAHAN ----------------------
def translate_text(text, dest):
    if not text.strip():
        return text
    try:
        return GoogleTranslator(source="auto", target=dest).translate(text)
    except Exception as e:
        print(f"❌ Gagal menerjemahkan: {e}")
        return text

def get_existing_translated_languages():
    """Mendapatkan daftar bahasa yang sudah ada file README-nya"""
    existing_langs = []
    for code in LANGUAGES:
        readme_path = os.path.join(OUTPUT_DIR, f"README-{code.upper()}.md")
        if os.path.exists(readme_path):
            existing_langs.append(code)
    return existing_langs

def update_language_switcher(new_languages=None, removed_languages=None):
    """Update language switcher di README utama dan semua README yang sudah diterjemahkan"""
    
    # Dapatkan semua bahasa yang sudah ada
    existing_langs = get_existing_translated_languages()
    
    # Jika ada bahasa baru, tambahkan ke daftar existing
    if new_languages:
        for lang in new_languages:
            if lang not in existing_langs:
                existing_langs.append(lang)
    
    # Jika ada bahasa yang dihapus, hapus dari daftar existing
    if removed_languages:
        for lang in removed_languages:
            if lang in existing_langs:
                existing_langs.remove(lang)
    
    # Update README utama (English)
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Buat daftar link untuk README utama
        lang_links = []
        for code in existing_langs:
            if code in LANGUAGES:
                name = LANGUAGES[code][0]
                lang_links.append(f"[{name}](docs/lang/README-{code.upper()}.md)")
        
        if lang_links:
            switcher = f"> 🌐 Available in other languages: {' | '.join(lang_links)}\n"
            
            # Cari dan replace language switcher yang sudah ada
            if "> 🌐 Available in other languages:" in content:
                # Replace hanya bagian language switcher saja
                content = re.sub(
                    r'> 🌐 Available in other languages:.*', 
                    f'> 🌐 Available in other languages: {" | ".join(lang_links)}', 
                    content
                )
            else:
                # Tambahkan yang baru sebelum ---
                match = re.search(r"\n-{3,}\n", content)
                if match:
                    position = match.start()
                    content = content[:position] + "\n" + switcher + content[position:]
                else:
                    content = content.strip() + "\n" + switcher
        else:
            # Hapus language switcher jika tidak ada bahasa lain (termasuk baris kosong berlebih)
            content = re.sub(r'> 🌐 Available in other languages:.*\n', '', content)
            # Hapus baris kosong berlebih yang tersisa
            content = re.sub(r'\n\n\n', '\n\n', content)  # Ganti 3 baris kosong menjadi 2
            content = re.sub(r'\n\n\n', '\n\n', content)  # Lakukan lagi untuk memastikan
        
        with open(SOURCE_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Language switcher di README utama diperbarui: {', '.join(existing_langs) if existing_langs else 'Tidak ada bahasa lain'}")
    
    except Exception as e:
        print(f"❌ Gagal update language switcher di README utama: {e}")
    
    # Update semua README yang sudah diterjemahkan
    for lang_code in existing_langs:
        if lang_code in LANGUAGES:
            lang_name, _, intro_text = LANGUAGES[lang_code]
            readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
            
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Buat daftar link untuk bahasa ini (semua bahasa kecuali dirinya sendiri)
                    links = ["[English](../../README.md)"]
                    for code in existing_langs:
                        if code != lang_code:
                            name = LANGUAGES[code][0]
                            links.append(f"[{name}](README-{code.upper()}.md)")
                    
                    links_text = " | ".join(links)
                    new_switcher_line = f"> {intro_text} {links_text}"
                    
                    # Cari dan replace language switcher yang sudah ada
                    escaped_intro = re.escape(intro_text)
                    if f"> {intro_text}" in content:
                        # Replace hanya bagian language switcher saja
                        content = re.sub(
                            fr'> {escaped_intro}.*', 
                            new_switcher_line, 
                            content
                        )
                    else:
                        # Tambahkan yang baru sebelum ---
                        match = re.search(r"\n-{3,}\n", content)
                        if match:
                            position = match.start()
                            content = content[:position] + "\n" + new_switcher_line + "\n" + content[position:]
                    
                    with open(readme_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ Language switcher di README-{lang_code.upper()} diperbarui")
                
                except Exception as e:
                    print(f"❌ Gagal update language switcher di README-{lang_code.upper()}: {e}")

def remove_language_files(lang_codes):
    """Hapus file README untuk bahasa tertentu dan update language switcher"""
    removed_langs = []
    
    for lang_code in lang_codes:
        if lang_code in LANGUAGES:
            readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
            
            if os.path.exists(readme_path):
                try:
                    os.remove(readme_path)
                    removed_langs.append(lang_code)
                    print(f"🗑️ File README-{lang_code.upper()}.md berhasil dihapus")
                except Exception as e:
                    print(f"❌ Gagal menghapus README-{lang_code.upper()}.md: {e}")
            else:
                print(f"⚠️ File README-{lang_code.upper()}.md tidak ditemukan")
        else:
            print(f"❌ Kode bahasa '{lang_code}' tidak dikenali")
    
    # Update language switcher setelah menghapus file
    if removed_langs:
        update_language_switcher(removed_languages=removed_langs)
        
        # Hapus folder docs/lang jika kosong, lalu docs jika juga kosong
        if not get_existing_translated_languages():
            try:
                if os.path.exists(OUTPUT_DIR):
                    shutil.rmtree(OUTPUT_DIR)
                    print(f"🗑️ Folder {OUTPUT_DIR} berhasil dihapus (kosong)")
                    
                    # Cek apakah folder docs juga kosong, jika ya hapus
                    docs_dir = os.path.dirname(OUTPUT_DIR)  # 'docs'
                    if os.path.exists(docs_dir) and not os.listdir(docs_dir):
                        shutil.rmtree(docs_dir)
                        print(f"🗑️ Folder {docs_dir} berhasil dihapus (kosong)")
            except Exception as e:
                print(f"❌ Gagal menghapus folder: {e}")
    
    return removed_langs

def remove_all_language_files():
    """Hapus semua file README terjemahan dan folder docs/lang serta docs jika kosong"""
    existing_langs = get_existing_translated_languages()
    
    if not existing_langs:
        print("ℹ️ Tidak ada file README terjemahan yang ditemukan")
        return
    
    # Hapus semua file
    for lang_code in existing_langs:
        readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
        try:
            os.remove(readme_path)
            print(f"🗑️ File README-{lang_code.upper()}.md berhasil dihapus")
        except Exception as e:
            print(f"❌ Gagal menghapus README-{lang_code.upper()}.md: {e}")
    
    # Hapus folder docs/lang jika kosong, lalu docs jika juga kosong
    try:
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
            print(f"🗑️ Folder {OUTPUT_DIR} berhasil dihapus")
            
            # Cek apakah folder docs juga kosong, jika ya hapus
            docs_dir = os.path.dirname(OUTPUT_DIR)  # 'docs'
            if os.path.exists(docs_dir) and not os.listdir(docs_dir):
                shutil.rmtree(docs_dir)
                print(f"🗑️ Folder {docs_dir} berhasil dihapus (kosong)")
    except Exception as e:
        print(f"❌ Gagal menghapus folder: {e}")
    
    # Update README utama untuk menghapus language switcher dan rapikan baris kosong
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Hapus language switcher
        content = re.sub(r'> 🌐 Available in other languages:.*\n', '', content)
        
        # Rapikan baris kosong berlebih
        content = re.sub(r'\n\n\n', '\n\n', content)  # Ganti 3 baris kosong menjadi 2
        content = re.sub(r'\n\n\n', '\n\n', content)  # Lakukan lagi untuk memastikan
        
        with open(SOURCE_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ Language switcher di README utama dihapus dan baris kosong dirapikan")
    
    except Exception as e:
        print(f"❌ Gagal update README utama: {e}")

def translate_readme(lang_code, lang_info, protected):
    lang_name, translate_code, intro_text = lang_info
    dest_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        src_text = f.read()

    parts = re.split(r'\n-{3,}\n', src_text, 1)
    src_header, src_body = (parts[0], parts[1]) if len(parts) > 1 else (src_text, "")

    # Bersihkan language switcher yang sudah ada dari header
    cleaned_header = re.sub(r'^\s*>\s*🌐.*$', '', src_header, flags=re.MULTILINE).strip()
    
    # Dapatkan semua bahasa yang sudah ada untuk membuat language switcher
    existing_langs = get_existing_translated_languages()
    
    # Buat language switcher untuk bahasa ini
    links = ["[English](../../README.md)"]
    for code in existing_langs:
        if code != lang_code:
            name = LANGUAGES[code][0]
            links.append(f"[{name}](README-{code.upper()}.md)")
    
    links_text = " | ".join(links)
    final_header = f"{cleaned_header}\n\n> {intro_text} {links_text}"

    print(f"📘 Menerjemahkan ke {lang_name} ({lang_code.upper()}) ...")

    body_lines = src_body.split("\n")
    translated_lines = []
    in_code_block = False
    in_example_block = False
    in_table = False
    table_header_processed = False

    for i, line in enumerate(body_lines):
        # Deteksi blok kode
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue

        # Deteksi tabel
        if re.match(r'^\|.*\|$', line) and not in_code_block:
            if not in_table:
                in_table = True
                table_header_processed = False
            
            # Baris pemisah tabel (---|---|)
            if re.match(r'^\|?[\s:-]+\|[\s:-]+\|[\s:-]+\|?$', line):
                translated_lines.append(line)
                table_header_processed = True
                continue
            
            # Baris header tabel (baris pertama setelah judul tabel)
            if in_table and not table_header_processed:
                # Pisahkan kolom dan terjemahkan header
                columns = line.split('|')
                translated_columns = []
                
                for j, col in enumerate(columns):
                    col = col.strip()
                    if col and not re.match(r'^[\s:-]*$', col):
                        # Terjemahkan header kolom
                        temp_col = col
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

                        # Proteksi untuk komponen penting
                        temp_col = protect(r"`[^`]+`", temp_col)  # Inline code
                        
                        # Terjemahkan teks header
                        translated_col = translate_text(temp_col, translate_code)
                        
                        # Kembalikan placeholder
                        for key, val in placeholders.items():
                            translated_col = translated_col.replace(key, val)
                        
                        translated_columns.append(f" {translated_col} ")
                    else:
                        translated_columns.append(col)
                
                translated_line = '|'.join(translated_columns)
                translated_lines.append(translated_line)
                table_header_processed = True
            else:
                # Baris data tabel, tidak diterjemahkan
                translated_lines.append(line)
            continue
        else:
            # Keluar dari mode tabel
            if in_table:
                in_table = False
                table_header_processed = False

        # Deteksi bagian contoh (Before/After)
        if re.match(r'^\*\*Before:\*\*$', line, re.IGNORECASE):
            in_example_block = True
            # Terjemahkan "Before:" sesuai bahasa target
            translated_before = translate_text("Before:", translate_code)
            translated_lines.append(f"**{translated_before}**")
            continue
        
        if re.match(r'^\*\*After \(Translated\):\*\*$', line, re.IGNORECASE):
            in_example_block = True
            # Terjemahkan "After (Translated):" sesuai bahasa target
            translated_after = translate_text("After (Translated):", translate_code)
            translated_lines.append(f"**{translated_after}**")
            continue

        # Jika dalam blok kode atau contoh, jangan terjemahkan konten kode
        if in_code_block or in_example_block:
            translated_lines.append(line)
            # Reset status example block jika menemukan baris kosong setelah contoh
            if in_example_block and not line.strip():
                in_example_block = False
            continue

        # Deteksi elemen struktural (baris kosong, dll)
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

        # Proteksi untuk semua pola yang penting
        if is_protect_enabled():
            for p in protected["protected_phrases"]:
                temp_line = protect(p, temp_line)

        # Proteksi tambahan untuk komponen penting
        temp_line = protect(r"\[.*?\]\(https?://[^\)]+\)", temp_line)  # Markdown links dengan URL
        temp_line = protect(r"\[.*?\]\(mailto:[^\)]+\)", temp_line)     # Email links
        temp_line = protect(r"https?://[^\s\)]+", temp_line)           # URL standalone
        temp_line = protect(r"MIT\s+License", temp_line, re.IGNORECASE)  # MIT License
        temp_line = protect(r"\(LICENSE\)", temp_line)                   # (LICENSE)
        temp_line = protect(r"\(\.\./\.\./LICENSE\)", temp_line)         # (../../LICENSE)
        temp_line = protect(r"`[^`]+`", temp_line)                       # Inline code
        temp_line = protect(r"`auto-translate-readmes\.run`", temp_line) # Command ID
        
        # Terjemahkan teks
        translated = translate_text(temp_line, translate_code)

        # Kembalikan placeholder ke teks asli
        for key, val in placeholders.items():
            translated = translated.replace(key, val)

        translated_lines.append(translated)

    translated_body = "\n".join(translated_lines)
    
    # Pastikan link LICENSE tetap konsisten
    final_text = f"{final_header}\n\n---\n{translated_body}"
    
    # Normalisasi link LICENSE ke format yang benar
    final_text = re.sub(r"\(LICENSE\)", "(../../LICENSE)", final_text)
    
    # Bersihkan placeholder yang mungkin tertinggal
    final_text = re.sub(r"__p\d+__", "", final_text)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ {dest_path} berhasil dibuat.")

# ---------------------- MAIN PROGRAM ----------------------
def main():
    parser = argparse.ArgumentParser(description="Auto Translate README with protection options")
    parser.add_argument("--lang", help="Kode bahasa, mis. id,fr,de (bisa multiple dipisah koma)")
    parser.add_argument("--remove-lang", help="Hapus file bahasa tertentu, mis. id,fr (bisa multiple dipisah koma)")
    parser.add_argument("--remove-all-lang", action="store_true", help="Hapus semua file bahasa terjemahan")
    parser.add_argument("--add-protect", help="Tambahkan frasa proteksi")
    parser.add_argument("--remove-protect", help="Hapus frasa proteksi")
    parser.add_argument("--list-protect", action="store_true", help="Tampilkan daftar frasa proteksi")
    parser.add_argument("--init-protect", action="store_true", help="Reset file protected_phrases.json ke default")
    parser.add_argument("--enable-protect", action="store_true", help="Aktifkan proteksi")
    parser.add_argument("--disable-protect", action="store_true", help="Nonaktifkan proteksi")
    parser.add_argument("--status-protect", action="store_true", help="Lihat status proteksi")
    args = parser.parse_args()

    protected = load_protected_phrases()

    if args.init_protect:
        save_protected_phrases(DEFAULT_PROTECTED)
        print("🔁 File protected_phrases.json telah di-reset ke default.")
        return
    if args.add_protect:
        protected["protected_phrases"].append(args.add_protect)
        save_protected_phrases(protected)
        print(f"✅ Frasa '{args.add_protect}' ditambahkan ke proteksi.")
        return
    if args.remove_protect:
        protected["protected_phrases"] = [p for p in protected["protected_phrases"] if p != args.remove_protect]
        save_protected_phrases(protected)
        print(f"🗑️ Frasa '{args.remove_protect}' dihapus dari proteksi.")
        return
    if args.list_protect:
        print("📜 Daftar frasa yang diproteksi:")
        for p in protected["protected_phrases"]:
            print(f"- {p}")
        return
    if args.enable_protect:
        set_protect_status(True)
        print("🟢 Proteksi diaktifkan.")
        return
    if args.disable_protect:
        set_protect_status(False)
        print("🔴 Proteksi dinonaktifkan.")
        return
    if args.status_protect:
        print("🧩 Status proteksi:", "AKTIF ✅" if is_protect_enabled() else "NONAKTIF ❌")
        return

    # Handle penghapusan file bahasa
    if args.remove_lang:
        lang_codes = [lang.strip() for lang in args.remove_lang.split(',')]
        removed = remove_language_files(lang_codes)
        if removed:
            print(f"🎉 Bahasa berhasil dihapus: {', '.join(removed)}")
        return
    
    if args.remove_all_lang:
        remove_all_language_files()
        print("🎉 Semua file bahasa terjemahan berhasil dihapus")
        return

    # Jalankan translate
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if args.lang:
        # Parse multiple languages jika dipisah koma
        lang_codes = [lang.strip() for lang in args.lang.split(',')]
        valid_langs = []
        
        for lang_code in lang_codes:
            if lang_code in LANGUAGES:
                valid_langs.append(lang_code)
            else:
                print(f"❌ Kode bahasa '{lang_code}' tidak dikenali. Dilanjutkan...")
        
        if valid_langs:
            # Terjemahkan bahasa yang dipilih
            for code in valid_langs:
                translate_readme(code, LANGUAGES[code], protected)
                time.sleep(1)
            
            # Update language switcher untuk SEMUA bahasa yang sudah ada (termasuk yang baru)
            update_language_switcher(valid_langs)
        else:
            print("❌ Tidak ada kode bahasa yang valid.")
    else:
        # Terjemahkan semua bahasa
        for code, info in tqdm(LANGUAGES.items(), desc="Menerjemahkan semua README"):
            translate_readme(code, info, protected)
            time.sleep(1)
        
        # Update language switcher untuk semua bahasa
        update_language_switcher()
    
    print("\n🎉 Semua README berhasil diterjemahkan!\n")

if __name__ == "__main__":
    main()