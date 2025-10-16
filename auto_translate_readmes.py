import os
import re
import time
from deep_translator import GoogleTranslator
from tqdm import tqdm

SOURCE_FILE = "README.md"
OUTPUT_DIR = "docs/lang"

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

def translate_text(text, dest):
    """Menerjemahkan teks menggunakan deep-translator yang lebih stabil."""
    if not text.strip():
        return text
    try:
        return GoogleTranslator(source='auto', target=dest).translate(text)
    except Exception as e:
        print(f"❌ Gagal menerjemahkan: {e}. Menggunakan teks asli.")
        return text

def translate_readme(lang_code, lang_info):
    """Menerjemahkan seluruh body README dalam satu kali permintaan per bahasa."""
    lang_name, translate_code, intro_text = lang_info
    dest_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        src_text = f.read()

    parts = re.split(r'\n-{3,}\n', src_text, 1)
    src_header, src_body = (parts[0], parts[1]) if len(parts) > 1 else (src_text, "")

    cleaned_header = re.sub(r'^\s*>\s*🌐.*$', '', src_header, flags=re.MULTILINE).strip()
    links = ["[English](../../README.md)"]
    for code, (name, _, _) in LANGUAGES.items():
        if code != lang_code:
            links.append(f"[{name}](README-{code.upper()}.md)")
    links_text = " | ".join(links)
    new_switcher = f"> {intro_text} {links_text}"
    final_header = f"{cleaned_header}\n\n{new_switcher}"

    print(f"📘 Menerjemahkan ke {lang_name} ({lang_code.upper()}) ...")

    # --- PERBAIKAN UTAMA DI SINI: Menghapus .strip() ---
    # Ini akan mempertahankan semua baris kosong asli
    body_lines = src_body.split('\n')
    translated_lines = []
    in_code_block = False

    for line in body_lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue

        # Baris struktural (termasuk baris kosong) akan dilewati tanpa diterjemahkan
        is_structural = in_code_block or re.match(r'^\s*\|?[-:|\s]+\|?\s*$', line) or not line.strip()
        if is_structural:
            translated_lines.append(line)
            continue

        content_placeholders = {}
        counter = 0
        temp_line = line

        def protect(pattern, text, flags=0):
            nonlocal counter
            def replace_fn(match):
                nonlocal counter
                key = f"__p{counter}__"
                content_placeholders[key] = match.group(0)
                counter += 1
                return key
            return re.sub(pattern, replace_fn, text, flags=flags)

        temp_line = protect(r"\[.*?\]\(.*?\)|https?:\/\/\S+", temp_line)
        temp_line = protect(r"\*\*.*?\*\*", temp_line)
        temp_line = protect(r"`[^`]+`", temp_line)
        
        translated_line_raw = translate_text(temp_line, translate_code)
        
        restored_line = translated_line_raw
        for key in sorted(content_placeholders.keys(), reverse=True):
            restored_line = restored_line.replace(key, content_placeholders[key])

        final_line = re.sub(r'^(\s*[-*])(?![*\s])', r'\1 ', restored_line)
        translated_lines.append(final_line)

    translated_body = "\n".join(translated_lines)
    final_text = f"{final_header}\n\n---\n{translated_body}"
    final_text = re.sub(r"\(LICENSE\)", "(../../LICENSE)", final_text)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_text)
    print(f"✅ Dibuat / Diperbarui: {dest_path}")

def main():
    """Fungsi utama untuk menjalankan seluruh proses."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("\n🌍 Membuat & menerjemahkan semua README multilingual...\n")
    try:
        with open(SOURCE_FILE, 'r+', encoding='utf-8') as f:
            src_text = f.read()
            if "> 🌐 Available in other languages:" not in src_text:
                print(f"🔧 Language switcher not found in {SOURCE_FILE}. Adding it now...")
                lang_links = " | ".join([f"[{info[0]}](docs/lang/README-{code.upper()}.md)" for code, info in LANGUAGES.items()])
                block_to_add = f"\n> 🌐 Available in other languages: {lang_links}\n"
                match = re.search(r"\n-{3,}\n", src_text)
                if match:
                    position = match.start()
                    new_content = src_text[:position] + block_to_add + src_text[position:]
                else:
                    new_content = src_text.strip() + "\n" + block_to_add
                f.seek(0)
                f.write(new_content)
                f.truncate()
                print(f"✅ Successfully added language switcher to {SOURCE_FILE}.")
            else:
                print(f"👍 Language switcher already exists in {SOURCE_FILE}. Skipping.")
    except Exception as e:
        print(f"❌ Failed to update {SOURCE_FILE}: {e}")

    for code, info in tqdm(LANGUAGES.items(), desc="Translating READMEs"):
        try:
            translate_readme(code, info)
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error saat memproses {code.upper()}: {e}")

    print("\n🎉 Semua README berhasil dibuat dan diterjemahkan!\n")

if __name__ == "__main__":
    main()