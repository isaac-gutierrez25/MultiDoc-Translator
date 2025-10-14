import os
import re
import time
from googletrans import Translator
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


def make_header(lang_code, base_header):
    """Buat header baru tanpa link lama, lalu tambahkan navigasi bahasa."""
    lang_name, _, intro_text = LANGUAGES[lang_code]
    base_header = re.sub(r">\s*🌐[\s\S]*?---", "", base_header).strip()
    links = ["[English](../../README.md)"]
    for code, (name, _, _) in LANGUAGES.items():
        if code != lang_code:
            links.append(f"[{name}](README-{code.upper()}.md)")
    links_text = " | ".join(links)
    return f"""{base_header}\n\n> {intro_text} {links_text}\n\n---\n"""


def split_header_and_body(text):
    parts = text.split("\n---", 1)
    if len(parts) == 2:
        return parts[0] + "\n---\n", parts[1]
    return text, ""

def freeze_markdown(text):
    """Simpan elemen markdown agar tidak diterjemahkan."""
    placeholders = {}
    counter = 0

    def create_placeholder(match, kind):
        nonlocal counter
        key = f"@@{kind.upper()}_{counter}@@"
        counter += 1
        placeholders[key] = match.group(0)
        return key

    text = re.sub(r"^(?: *\|(?:[-: ]+)*\| *)", lambda m: create_placeholder(m, "TABLE_SEPARATOR"), text, flags=re.MULTILINE)
    text = re.sub(r"```[\s\S]*?```", lambda m: create_placeholder(m, "CODE_BLOCK"), text)
    text = re.sub(r"`[^`]+`", lambda m: create_placeholder(m, "INLINE_CODE"), text)
    text = re.sub(r"\[.*?\]\(.*?\)|https?:\/\/\S+", lambda m: create_placeholder(m, "LINK"), text)
    
    return text, placeholders

def unfreeze_markdown(text, placeholders):
    """Kembalikan elemen markdown ke tempat semula."""
    for key, val in placeholders.items():
        # Gunakan regex untuk pencocokan yang lebih aman
        safe_key = re.escape(key)
        text = re.sub(safe_key, val, text)
    return text

def translate_text(text, dest, translator, retries=3):
    for i in range(retries):
        try:
            return translator.translate(text, dest=dest).text
        except Exception as e:
            print(f"⚠️  Gagal translate percobaan {i+1}/{retries}: {e}")
            time.sleep(2)
    return text

def translate_readme(lang_code, lang_info, translator):
    lang_name, translate_code, _ = lang_info
    src_path = SOURCE_FILE
    dest_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(src_path, "r", encoding="utf-8") as f:
        src_text = f.read()

    src_header, src_body = split_header_and_body(src_text)
    
    frozen, placeholders = freeze_markdown(src_body)
    header = make_header(lang_code, src_header.strip())

    # === PERBAIKAN DI SINI ===
    # Bungkus placeholder dengan tag notranslate
    temp_body = frozen
    for key in placeholders:
        safe_key = re.escape(key)
        temp_body = re.sub(safe_key, f'<span class="notranslate">{key}</span>', temp_body)

    print(f"📘 Menerjemahkan ke {lang_name} ({lang_code.upper()}) ...")
    translated_body_raw = translate_text(temp_body, translate_code, translator)
    
    # Hapus tag notranslate setelah terjemahan
    translated_body = re.sub(r'<span class="notranslate">(.*?)</span>', r'\1', translated_body_raw)
    
    restored = unfreeze_markdown(translated_body, placeholders)
    # === AKHIR PERBAIKAN ===

    # Normalkan format list
    restored = re.sub(r'^\s*(-|\*|–)\s*(.*)', r'- \2', restored, flags=re.MULTILINE)

    # Ubah link LICENSE
    restored = re.sub(r"\(LICENSE\)", "(../../LICENSE)", restored)

    final_text = header.strip() + "\n\n" + restored.strip() + "\n"

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ Dibuat / Diperbarui: {dest_path}")

def main():
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

    translator = Translator()

    for code, info in tqdm(LANGUAGES.items(), desc="Translating READMEs"):
        try:
            translate_readme(code, info, translator)
        except Exception as e:
            print(f"❌ Error processing {code.upper()}: {e}")

    print("\n🎉 All README files created and translated successfully!\n")

if __name__ == "__main__":
    main()