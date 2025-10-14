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

    # Hapus blok multi-bahasa lama di header jika ada
    base_header = re.sub(r">\s*🌐[\s\S]*?---", "", base_header).strip()

    links = ["[English](../../README.md)"]
    for code, (name, _, _) in LANGUAGES.items():
        if code != lang_code:
            links.append(f"[{name}](README-{code.upper()}.md)")

    links_text = " | ".join(links)

    return f"""{base_header}

> {intro_text} {links_text}

---
"""


def split_header_and_body(text):
    parts = text.split("\n---", 1)
    if len(parts) == 2:
        return parts[0] + "\n---\n", parts[1]
    return text, ""


def freeze_markdown(text):
    """Simpan blok kode, inline code, dan link agar tidak diterjemahkan."""
    blocks, inlines, links = {}, {}, {}

    def block_replacer(match):
        key = f"⟦BLOCK_{len(blocks)}⟧"
        blocks[key] = match.group(0)
        return key

    def inline_replacer(match):
        key = f"⟦INLINE_{len(inlines)}⟧"
        inlines[key] = match.group(0)
        return key

    def link_replacer(match):
        key = f"⟦LINK_{len(links)}⟧"
        links[key] = match.group(0)
        return key

    text = re.sub(r"```[\s\S]*?```", block_replacer, text)
    text = re.sub(r"`[^`]+`", inline_replacer, text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", link_replacer, text)

    return text, blocks, inlines, links


def unfreeze_markdown(text, blocks, inlines, links):
    """Kembalikan blok, inline code, dan link ke tempat semula."""
    for key, val in blocks.items():
        text = text.replace(key, val)
    for key, val in inlines.items():
        text = text.replace(key, val)
    for key, val in links.items():
        text = text.replace(key, val)
    return text


def restore_blocks(text, blocks):
    """Pulihkan varian placeholder yang mungkin berubah setelah terjemahan."""
    for k, v in blocks.items():
        variants = [
            k,
            k.replace("BLOCK", "BLOK"),
            k.replace("BLOCK", "BLOQUE"),
            k.replace("BLOCK", "BLOCO"),
            k.replace("BLOCK", "БЛОК"),
            k.replace("BLOCK", "ブロック"),
            k.replace("BLOCK", "블록"),
            k.replace("BLOCK", "块"),
        ]
        for variant in variants:
            text = text.replace(variant, v)
    return text


def translate_text(text, dest, translator, retries=3):
    for i in range(retries):
        try:
            return translator.translate(text, dest=dest).text
        except Exception as e:
            print(f"⚠️ Gagal translate percobaan {i+1}/{retries}: {e}")
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
    frozen, blocks, inlines, links = freeze_markdown(src_body)
    header = make_header(lang_code, src_header.strip())

    print(f"📘 Menerjemahkan ke {lang_name} ({lang_code.upper()}) ...")
    translated = translate_text(frozen, translate_code, translator)
    restored = unfreeze_markdown(translated, blocks, inlines, links)
    restored = restore_blocks(restored, blocks)

    # 🔗 Ubah link (LICENSE) → (../../LICENSE)
    restored = re.sub(r"\(LICENSE\)", "(../../LICENSE)", restored)

    final_text = header.strip() + "\n\n" + restored.strip() + "\n"

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ Dibuat / Diperbarui: {dest_path}")


def main():
    print("\n🌍 Membuat & menerjemahkan semua README multilingual...\n")
    translator = Translator()

    for code, info in tqdm(LANGUAGES.items()):
        try:
            translate_readme(code, info, translator)
        except Exception as e:
            print(f"❌ Error di {code.upper()}: {e}")

    print("\n🎉 Semua file README berhasil dibuat dan diterjemahkan!\n")


if __name__ == "__main__":
    main()
