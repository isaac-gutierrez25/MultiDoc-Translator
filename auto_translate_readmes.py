import os
import re
import json
import time
import argparse
import shutil
from deep_translator import GoogleTranslator
from tqdm import tqdm

SOURCE_FILE = "README.md"
CHANGELOG_FILE = "CHANGELOG.md"
PACKAGE_JSON = "package.json"
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
    "ru": ("Русский", "ru", "🌐 Доступно na innych językach:"),
    "pt": ("Português", "pt", "🌐 Disponível em outros idiomas:"),
    "ko": ("한국어", "ko", "🌐 다른 언어로도 사용 가능:"),
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
    """Deteksi URL repository GitHub dari berbagai sumber"""
    # Coba dari package.json pertama
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
        print(f"❌ Error reading package.json: {e}")
    
    # Coba dari .git/config
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
        print(f"❌ Error reading .git/config: {e}")
    
    # Fallback: cari di README.md
    try:
        if os.path.exists(SOURCE_FILE):
            with open(SOURCE_FILE, "r", encoding="utf-8") as f:
                readme_content = f.read()
            
            github_url_match = re.search(r'https://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-_.]+', readme_content)
            if github_url_match:
                return github_url_match.group(0)
    except Exception as e:
        print(f"❌ Error searching GitHub URL in README: {e}")
    
    return None

def get_github_releases_url():
    """Generate GitHub Releases URL dari repository URL"""
    repo_url = get_github_repo_url()
    if repo_url:
        return f"{repo_url}/releases"
    
    # Fallback default (untuk extension ini sendiri)
    return "https://github.com/fatonyahmadfauzi/Auto-Translate-Readmes/releases"

def detect_github_url():
    """Fungsi untuk mendeteksi dan menampilkan GitHub URL"""
    repo_url = get_github_repo_url()
    releases_url = get_github_releases_url()
    
    if repo_url:
        print("🔍 GitHub Repository Detection Results:")
        print(f"📦 Repository URL: {repo_url}")
        print(f"🚀 Releases URL: {releases_url}")
        print("\n📋 Sources checked:")
        print("• package.json (repository field)")
        print("• .git/config")
        print("• README.md (GitHub URL patterns)")
        return True
    else:
        print("❌ Could not detect GitHub repository URL automatically.")
        print("\nPlease check:")
        print("• package.json has 'repository' field")
        print("• .git/config has remote URL") 
        print("• Or add GitHub URL manually to README")
        return False

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

# ---------------------- DETEKSI CHANGELOG ----------------------
def has_changelog_file():
    """Cek apakah file CHANGELOG.md ada di root"""
    return os.path.exists(CHANGELOG_FILE)

def has_changelog_section_in_readme():
    """Cek apakah README.md memiliki bagian Changelog"""
    if not os.path.exists(SOURCE_FILE):
        return False
    
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Cek pattern untuk bagian Changelog
    patterns = [
        r"##\s+🧾\s+Changelog",
        r"##\s+Changelog",
        r"#+\s+Changelog"
    ]
    
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    
    return False

def fix_existing_changelog_spacing():
    """Perbaiki spacing dan pembatas untuk section Changelog yang sudah ada"""
    if not has_changelog_section_in_readme():
        return False
    
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        changes_made = False
        
        # 1. Perbaiki pattern: --- langsung diikuti ## 🧾 Changelog
        # Menjadi: --- + 1 baris kosong + ## 🧾 Changelog
        old_pattern = r'---\s*\n\s*## 🧾 Changelog'
        new_pattern = '---\n\n## 🧾 Changelog'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_pattern, content)
            changes_made = True
        
        # 2. Periksa apakah ada pembatas antara Changelog dan License
        if '## 🧾 Changelog' in content and '## 🧾 License' in content:
            # Cek apakah ada --- antara Changelog dan License
            between_sections = re.search(r'## 🧾 Changelog.*?(## 🧾 License)', content, re.DOTALL)
            if between_sections:
                section_content = between_sections.group(0)
                if '---' not in section_content:
                    # Tambahkan --- sebelum License
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
            
            print("✅ Fixed changelog section spacing and separators in README.md")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Failed to fix changelog spacing: {e}")
        return False

def add_changelog_section_to_readme():
    """Tambahkan bagian Changelog ke README.md jika belum ada dengan spacing dan pembatas yang benar"""
    if not has_changelog_file():
        print("❌ No CHANGELOG.md file found in root directory")
        return False
    
    if has_changelog_section_in_readme():
        print("ℹ️ Changelog section already exists in README.md")
        # Perbaiki spacing jika sudah ada
        fix_existing_changelog_spacing()
        return True
    
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Dapatkan GitHub Releases URL yang dinamis
        github_releases_url = get_github_releases_url()
        
        # Cari posisi sebelum License section untuk menambahkan Changelog
        license_pattern = r'##\s+🧾\s+License'
        license_match = re.search(license_pattern, content, re.IGNORECASE)
        
        # Section Changelog dengan format yang benar termasuk pembatas
        changelog_section = f"""

---

## 🧾 Changelog

See all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.

> 📦 You can also view release notes directly on the [GitHub Releases page]({github_releases_url}).

"""
        
        if license_match:
            # Sisipkan sebelum License section
            position = license_match.start()
            
            # Cek apakah sudah ada --- sebelum License
            content_before_license = content[:position].rstrip()
            if content_before_license.endswith('---'):
                # Jika sudah ada ---, kita hanya perlu menambahkan Changelog section
                # Hapus --- yang sudah ada dan ganti dengan section lengkap
                last_dash_pos = content_before_license.rfind('---')
                new_content = content[:last_dash_pos].rstrip() + changelog_section + content[position:]
            else:
                # Jika tidak ada ---, tambahkan section lengkap dengan ---
                new_content = content[:position] + changelog_section + content[position:]
        else:
            # Tambahkan di akhir file sebelum License jika ada
            if "## 🧾 License" in content:
                license_pos = content.find("## 🧾 License")
                content_before_license = content[:license_pos].rstrip()
                
                if content_before_license.endswith('---'):
                    # Jika sudah ada ---, ganti dengan section lengkap
                    last_dash_pos = content_before_license.rfind('---')
                    new_content = content[:last_dash_pos].rstrip() + changelog_section + content[license_pos:]
                else:
                    # Jika tidak ada ---, tambahkan section lengkap
                    new_content = content[:license_pos] + changelog_section + content[license_pos:]
            else:
                # Tambahkan di akhir file dengan pembatas
                if content.strip().endswith('---'):
                    new_content = content.rstrip() + f'\n\n## 🧾 Changelog\n\nSee all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.\n\n> 📦 You can also view release notes directly on the [GitHub Releases page]({github_releases_url}).'
                else:
                    new_content = content.strip() + f'\n\n---\n\n## 🧾 Changelog\n\nSee all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.\n\n> 📦 You can also view release notes directly on the [GitHub Releases page]({github_releases_url}).'
        
        # Final cleanup: pastikan format yang benar
        # Pattern: --- diikuti oleh 1 baris kosong, lalu ## 🧾 Changelog
        new_content = re.sub(r'---\s*\n\s*## 🧾 Changelog', '---\n\n## 🧾 Changelog', new_content)
        
        # Juga pastikan ada --- sebelum License
        if '## 🧾 Changelog' in new_content and '## 🧾 License' in new_content:
            # Cek apakah ada --- antara Changelog dan License
            between_sections = re.search(r'## 🧾 Changelog.*?(## 🧾 License)', new_content, re.DOTALL)
            if between_sections:
                section_content = between_sections.group(0)
                if '---' not in section_content:
                    # Tambahkan --- sebelum License
                    new_content = re.sub(
                        r'(## 🧾 Changelog.*?)(## 🧾 License)',
                        r'\1\n\n---\n\n\2',
                        new_content,
                        flags=re.DOTALL
                    )
        
        # Juga perbaiki jika ada multiple empty lines
        new_content = re.sub(r'\n\n\n+', '\n\n', new_content)
        
        with open(SOURCE_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("✅ Changelog section added to README.md with proper spacing and separators")
        print(f"🔗 GitHub Releases URL: {github_releases_url}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add changelog section: {e}")
        return False

# ---------------------- FUNGSI TERJEMAHAN ----------------------
def translate_text(text, dest):
    if not text.strip():
        return text
    try:
        return GoogleTranslator(source="auto", target=dest).translate(text)
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return text

def get_existing_translated_languages():
    """Mendapatkan daftar bahasa yang sudah ada file README-nya"""
    existing_langs = []
    if not os.path.exists(OUTPUT_DIR):
        return existing_langs
        
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
            content = re.sub(r'\n\n\n', '\n\n', content)
            content = re.sub(r'\n\n\n', '\n\n', content)
        
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
            changelog_path = os.path.join(OUTPUT_DIR, f"CHANGELOG-{lang_code.upper()}.md")
            
            # Hapus file README
            if os.path.exists(readme_path):
                try:
                    os.remove(readme_path)
                    removed_langs.append(lang_code)
                    print(f"🗑️ File README-{lang_code.upper()}.md berhasil dihapus")
                except Exception as e:
                    print(f"❌ Gagal menghapus README-{lang_code.upper()}.md: {e}")
            else:
                print(f"⚠️ File README-{lang_code.upper()}.md tidak ditemukan")
            
            # Hapus file CHANGELOG jika ada
            if os.path.exists(changelog_path):
                try:
                    os.remove(changelog_path)
                    print(f"🗑️ File CHANGELOG-{lang_code.upper()}.md berhasil dihapus")
                except Exception as e:
                    print(f"❌ Gagal menghapus CHANGELOG-{lang_code.upper()}.md: {e}")
        else:
            print(f"❌ Kode bahasa '{lang_code}' tidak dikenali")
    
    # Update language switcher setelah menghapus file
    if removed_langs:
        update_language_switcher(removed_languages=removed_langs)
        
        # Hapus folder docs/lang jika kosong, lalu docs jika juga kosong
        if not get_existing_translated_languages():
            try:
                if os.path.exists(OUTPUT_DIR) and not os.listdir(OUTPUT_DIR):
                    shutil.rmtree(OUTPUT_DIR)
                    print(f"🗑️ Folder {OUTPUT_DIR} berhasil dihapus (kosong)")
                    
                    # Cek apakah folder docs juga kosong, jika ya hapus
                    docs_dir = os.path.dirname(OUTPUT_DIR)
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
    
    # Hapus semua file README dan CHANGELOG
    for lang_code in existing_langs:
        readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
        changelog_path = os.path.join(OUTPUT_DIR, f"CHANGELOG-{lang_code.upper()}.md")
        
        try:
            if os.path.exists(readme_path):
                os.remove(readme_path)
                print(f"🗑️ File README-{lang_code.upper()}.md berhasil dihapus")
            
            if os.path.exists(changelog_path):
                os.remove(changelog_path)
                print(f"🗑️ File CHANGELOG-{lang_code.upper()}.md berhasil dihapus")
        except Exception as e:
            print(f"❌ Gagal menghapus file untuk {lang_code}: {e}")
    
    # Hapus folder docs/lang jika kosong, lalu docs jika juga kosong
    try:
        if os.path.exists(OUTPUT_DIR):
            if not os.listdir(OUTPUT_DIR):
                shutil.rmtree(OUTPUT_DIR)
                print(f"🗑️ Folder {OUTPUT_DIR} berhasil dihapus")
                
                # Cek apakah folder docs juga kosong, jika ya hapus
                docs_dir = os.path.dirname(OUTPUT_DIR)
                if os.path.exists(docs_dir) and not os.listdir(docs_dir):
                    shutil.rmtree(docs_dir)
                    print(f"🗑️ Folder {docs_dir} berhasil dihapus (kosong)")
            else:
                print(f"⚠️ Folder {OUTPUT_DIR} tidak kosong, tidak dihapus")
    except Exception as e:
        print(f"❌ Gagal menghapus folder: {e}")
    
    # Update README utama untuk menghapus language switcher dan rapikan baris kosong
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Hapus language switcher
        content = re.sub(r'> 🌐 Available in other languages:.*\n', '', content)
        
        # Rapikan baris kosong berlebih
        content = re.sub(r'\n\n\n', '\n\n', content)
        content = re.sub(r'\n\n\n', '\n\n', content)
        
        with open(SOURCE_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ Language switcher di README utama dihapus dan baris kosong dirapikan")
    
    except Exception as e:
        print(f"❌ Gagal update README utama: {e}")

def protect_specific_phrases(text, lang_code):
    """Proteksi khusus untuk frasa-frasa penting setelah terjemahan"""
    
    # Proteksi untuk versi
    text = re.sub(r'(\*\*)?1\.85\.0(\*\*)?', '**1.85.0**', text)
    
    # Proteksi untuk sistem operasi
    text = re.sub(r'(\*\*)?Windows(\*\*)?', '**Windows**', text, flags=re.IGNORECASE)
    text = re.sub(r'(\*\*)?macOS(\*\*)?', '**macOS**', text, flags=re.IGNORECASE)
    text = re.sub(r'(\*\*)?Linux(\*\*)?', '**Linux**', text, flags=re.IGNORECASE)
    
    # Proteksi khusus untuk format daftar sistem operasi
    text = re.sub(r'\*\*Windows\*\*,?\s*\*\*macOS\*\*,?\s*(et|and|und|y|и)\s*\*\*Linux\*\*', '**Windows**, **macOS** et **Linux**', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\*Windows\*\*,?\s*\*\*macOS\*\*,?\s*\*\*Linux\*\*', '**Windows**, **macOS** et **Linux**', text, flags=re.IGNORECASE)
    
    return text

# ---------------------- TERJEMAHAN CHANGELOG ----------------------
def translate_changelog(lang_code, lang_info, protected):
    """Terjemahkan file CHANGELOG.md ke bahasa target"""
    if not has_changelog_file():
        return False
    
    lang_name, translate_code, _ = lang_info
    changelog_dest_path = os.path.join(OUTPUT_DIR, f"CHANGELOG-{lang_code.upper()}.md")
    
    print(f"📘 Translating CHANGELOG to {lang_name} ({lang_code.upper()}) ...")
    
    try:
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            changelog_content = f.read()
        
        # Pisahkan header dan body CHANGELOG
        parts = re.split(r'\n-{3,}\n', changelog_content, 1)
        changelog_header = parts[0] if len(parts) > 0 else ""
        changelog_body = parts[1] if len(parts) > 1 else ""
        
        # Terjemahkan judul CHANGELOG
        translated_title = translate_text("Changelog", translate_code)
        
        # Buat header yang sudah diterjemahkan
        if "# Changelog" in changelog_header:
            translated_header = changelog_header.replace("# Changelog", f"# {translated_title}")
        else:
            translated_header = f"# {translated_title}\n\n{changelog_header}"
        
        # Proses terjemahan body CHANGELOG
        body_lines = changelog_body.split("\n")
        translated_lines = []
        in_code_block = False
        
        for line in body_lines:
            # Deteksi blok kode
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                translated_lines.append(line)
                continue
            
            # Jika dalam blok kode, jangan terjemahkan
            if in_code_block:
                translated_lines.append(line)
                continue
            
            # Deteksi versi (format: ## [1.0.0] - 2024-01-01)
            version_match = re.match(r'^(##\s+\[[\d\.]+\]\s*-\s*\d{4}-\d{2}-\d{2})', line)
            if version_match:
                translated_lines.append(line)  # Jangan terjemahkan line versi
                continue
            
            # Deteksi elemen struktural
            is_structural = (
                re.match(r"^\s*[-=]+\s*$", line) or  # Garis pemisah
                not line.strip() or                   # Baris kosong
                re.match(r"^\s*\[.*?\]:\s*", line)   # Link references
            )
            
            if is_structural:
                translated_lines.append(line)
                continue
            
            # Proteksi teks sebelum terjemahan
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
            
            # Proteksi tambahan khusus CHANGELOG
            temp_line = protect(r"https?://[^\s\)]+", temp_line)           # URL
            temp_line = protect(r"`[^`]+`", temp_line)                     # Inline code
            temp_line = protect(r"\[.*?\]\([^)]+\)", temp_line)            # Markdown links
            temp_line = protect(r"\[[\d\.]+\]:\s*\S+", temp_line)          # Version links
            
            # Terjemahkan teks
            translated = translate_text(temp_line, translate_code)
            
            # Kembalikan placeholder ke teks asli
            for key, val in placeholders.items():
                translated = translated.replace(key, val)
            
            translated_lines.append(translated)
        
        translated_body = "\n".join(translated_lines)
        
        # Gabungkan header dan body
        final_changelog = f"{translated_header}\n\n---\n{translated_body}"
        
        # Cleanup placeholder yang tersisa
        final_changelog = re.sub(r"__p\d+__", "", final_changelog)
        
        # Tulis file CHANGELOG yang sudah diterjemahkan
        with open(changelog_dest_path, "w", encoding="utf-8") as f:
            f.write(final_changelog)
        
        print(f"✅ {changelog_dest_path} successfully created")
        return True
        
    except Exception as e:
        print(f"❌ Failed to translate CHANGELOG: {e}")
        return False

def update_changelog_links_in_readme(lang_code, lang_info):
    """Update link CHANGELOG di README yang sudah diterjemahkan"""
    readme_path = os.path.join(OUTPUT_DIR, f"README-{lang_code.upper()}.md")
    changelog_dest_path = f"CHANGELOG-{lang_code.upper()}.md"
    
    if not os.path.exists(readme_path):
        return
    
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Terjemahkan teks "Changelog" dan "release notes"
        _, translate_code, _ = lang_info
        translated_changelog = translate_text("Changelog", translate_code)
        translated_release_notes = translate_text("release notes", translate_code)
        translated_view = translate_text("view", translate_code)
        translated_also = translate_text("also", translate_code)
        translated_you_can = translate_text("You can", translate_code)
        
        # Dapatkan GitHub Releases URL yang dinamis
        github_releases_url = get_github_releases_url()
        
        # Update judul Changelog section
        content = re.sub(
            r'##\s+🧾\s+Changelog',
            f'## 🧾 {translated_changelog}',
            content,
            flags=re.IGNORECASE
        )
        
        # Update link ke file CHANGELOG yang sudah diterjemahkan
        content = re.sub(
            r'\[CHANGELOG\.md\]\(CHANGELOG\.md\)',
            f'[{translated_changelog}]({changelog_dest_path})',
            content
        )
        
        # Update teks release notes dengan URL yang dinamis
        old_release_pattern = r'You can also view release notes directly on the \[GitHub Releases page\]\([^)]+\)'
        new_release_text = f'{translated_you_can} {translated_also} {translated_view} {translated_release_notes} directly on the [GitHub Releases page]({github_releases_url})'
        
        content = re.sub(old_release_pattern, new_release_text, content, flags=re.IGNORECASE)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Changelog links updated in README-{lang_code.upper()}")
        
    except Exception as e:
        print(f"❌ Failed to update changelog links in README-{lang_code.upper()}: {e}")

def translate_changelog_only(lang_codes=None):
    """Hanya menerjemahkan CHANGELOG tanpa README"""
    if not has_changelog_file():
        print("❌ You don't have CHANGELOG.md file in root directory")
        return False
    
    protected = load_protected_phrases()
    
    # Jika tidak ada bahasa yang ditentukan, gunakan semua bahasa
    if not lang_codes:
        lang_codes = LANGUAGES.keys()
    
    success_count = 0
    for lang_code in lang_codes:
        if lang_code in LANGUAGES:
            if translate_changelog(lang_code, LANGUAGES[lang_code], protected):
                success_count += 1
                
                # Update links in README if it exists
                update_changelog_links_in_readme(lang_code, LANGUAGES[lang_code])
            
            time.sleep(1)  # Delay untuk menghindari rate limiting
    
    if success_count > 0:
        print(f"✅ Successfully translated CHANGELOG to {success_count} languages")
        return True
    else:
        print("❌ No CHANGELOG files were successfully translated")
        return False

# ---------------------- FUNGSI TRANSLATE README UTAMA ----------------------
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

    print(f"📘 Menerjemahkan README ke {lang_name} ({lang_code.upper()}) ...")

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
            
            # PERBAIKAN: Header tabel TIDAK diterjemahkan, langsung disalin
            if in_table and not table_header_processed:
                translated_lines.append(line)  # Header tabel tidak diterjemahkan
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
        
        # Proteksi khusus untuk versi dan sistem operasi
        temp_line = protect(r"\*\*1\.85\.0\*\*", temp_line)             # Versi spesifik 1.85.0
        temp_line = protect(r"\*\*Windows\*\*", temp_line)              # Windows
        temp_line = protect(r"\*\*macOS\*\*", temp_line)                # macOS
        temp_line = protect(r"\*\*Linux\*\*", temp_line)                # Linux
        
        # Terjemahkan teks
        translated = translate_text(temp_line, translate_code)

        # Kembalikan placeholder ke teks asli
        for key, val in placeholders.items():
            translated = translated.replace(key, val)

        translated_lines.append(translated)

    translated_body = "\n".join(translated_lines)
    
    # --- PERBAIKAN GENERIK ---
    # 1. Perbaiki bullet points
    translated_body = re.sub(r'^-(?=\w)', '- ', translated_body, flags=re.MULTILINE)
    
    # 2. Perbaiki non-breaking space
    translated_body = translated_body.replace('\xa0', ' ')
    
    # 3. PERBAIKAN: Fix colon formatting TANPA merusak bold text
    translated_body = re.sub(
        r'(\w+)\s*:\s*(\*\*(?!.*\*\*:\*\*))',
        r'\1 : \2',
        translated_body
    )
    
    # 4. PERBAIKAN UTAMA: Fix extra parenthesis
    translated_body = re.sub(
        r'(\[.*?\]\([^)]+\)\.)\)',
        r'\1',
        translated_body
    )
    
    # 5. Perbaiki format bold
    translated_body = re.sub(r'(\*\*)(\d+\.\d+\.\d+)(\*\*)', r'**\2**', translated_body)
    
    # 6. PERBAIKAN TAMBAHAN: Fix bold text yang rusak karena colon formatting
    translated_body = re.sub(
        r'\*\*(\w+)\s*:\s*\*\*',
        r'**\1:**',
        translated_body
    )
    
    # Pastikan link LICENSE tetap konsisten
    final_text = f"{final_header}\n\n---\n{translated_body}"
    final_text = re.sub(r"\(LICENSE\)", "(../../LICENSE)", final_text)
    final_text = re.sub(r"__p\d+__", "", final_text)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ {dest_path} berhasil dibuat.")

    # Setelah berhasil translate README, handle CHANGELOG
    if has_changelog_file() and has_changelog_section_in_readme():
        # Terjemahkan CHANGELOG
        translate_changelog(lang_code, lang_info, protected)
        
        # Update link CHANGELOG di README yang sudah diterjemahkan
        update_changelog_links_in_readme(lang_code, lang_info)

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
    
    # Perintah baru untuk CHANGELOG
    parser.add_argument("--translate-changelog", help="Translate CHANGELOG only (lang codes: id,fr,de,etc or 'all')")
    parser.add_argument("--auto-setup-changelog", action="store_true", help="Auto setup changelog section in README")
    
    # Perintah baru untuk GitHub URL detection
    parser.add_argument("--detect-github-url", action="store_true", help="Detect GitHub repository URL automatically")
    
    args = parser.parse_args()

    protected = load_protected_phrases()

    # Handle perintah GitHub URL detection
    if args.detect_github_url:
        detect_github_url()
        return

    # Handle perintah protection
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

    # Handle perintah CHANGELOG
    if args.auto_setup_changelog:
        if add_changelog_section_to_readme():
            print("✅ Changelog setup completed")
        else:
            print("❌ Changelog setup failed")
        return
    
    if args.translate_changelog:
        if not has_changelog_file():
            print("❌ You don't have CHANGELOG.md file in root directory")
            return
        
        if args.translate_changelog.lower() == 'all':
            lang_codes = None  # Translate ke semua bahasa
        else:
            lang_codes = [lang.strip() for lang in args.translate_changelog.split(',')]
            # Validasi kode bahasa
            lang_codes = [code for code in lang_codes if code in LANGUAGES]
            
            if not lang_codes:
                print("❌ No valid language codes provided")
                return
        
        translate_changelog_only(lang_codes)
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

    # Jalankan translate (README + CHANGELOG otomatis)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Auto setup changelog jika file CHANGELOG ada tapi section belum ada di README
    if has_changelog_file() and not has_changelog_section_in_readme():
        print("🔧 Auto-setting up changelog section in README...")
        add_changelog_section_to_readme()
    elif has_changelog_section_in_readme():
        # Perbaiki spacing untuk section yang sudah ada
        print("🔧 Checking changelog section spacing...")
        fix_existing_changelog_spacing()
    
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