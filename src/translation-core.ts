import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';
import fetch from 'node-fetch';
import { LANGUAGES, getL10n } from './l10n'; // ✅ IMPORT LANGUAGES DAN L10N

// Constants
export const SOURCE_FILE = "README.md";
export const CHANGELOG_FILE = "CHANGELOG.md";
export const PACKAGE_JSON = "package.json";
export const OUTPUT_DIR = "docs/lang";
export const PROTECTED_FILE = "protected_phrases.json";
export const PROTECT_STATUS_FILE = ".protect_status";

// Interfaces
export interface ProtectedData {
    protected_phrases: string[];
}

// 🛡️ Enhanced Protection Phrases (UNIVERSAL - tanpa author/version spesifik)
export const DEFAULT_PROTECTED_PHRASES: string[] = [
    "MIT\\s+License",
    "https?:\\/\\/\\S+",
    "\\(LICENSE\\)",
    "\\(\\.\\.\\/\\.\\.\\/LICENSE\\)",
    "Visual Studio Code",
    "VS Code",
    "Google Translate",
    "API",
    "GitHub",
    "README\\.md",
    "CHANGELOG\\.md",
    "Markdown",
    "MultiDoc-Translator",
    "MultiDoc Translator",
    "Ctrl \\+ Alt \\+ P",
    "F5",
    "Ctrl\\+Shift\\+X",
    "<script[^>]*>[\\s\\S]*?<\\/script>",
    "<link[^>]*>",
    "<img[^>]*>",
    "Lint",
    "TypeScript",
    "JavaScript",
    "HTML", 
    "CSS",
    "npm",
    "Node\\.js"
];

// Logger utility untuk konsistensi
export class Logger {
    static log(message: string): void {
        console.log(`[MultiDoc] ${message}`);
    }
    
    static error(message: string, error?: any): void {
        console.error(`[MultiDoc] ERROR: ${message}`, error);
    }
    
    static warn(message: string): void {
        console.warn(`[MultiDoc] WARN: ${message}`);
    }
}

// Type guard function untuk validasi data proteksi
export function isValidProtectedData(data: any): data is ProtectedData {
    return data && 
           Array.isArray(data.protected_phrases) && 
           data.protected_phrases.every((item: any) => typeof item === 'string');
}

// Translation cache untuk performance
export class TranslationCache {
    private cache = new Map<string, string>();
    private maxSize = 1000;

    get(key: string): string | undefined {
        return this.cache.get(key);
    }

    set(key: string, value: string): void {
        if (this.cache.size >= this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        this.cache.set(key, value);
    }

    clear(): void {
        this.cache.clear();
    }
}

const translationCache = new TranslationCache();

// 🌐 Translate via Google dengan retry mechanism dan caching
export async function translateWithGoogle(text: string, to: string, retries: number = 3): Promise<string> {
    if (!text.trim()) {
        return text;
    }
    
    const cacheKey = `${to}:${text}`;
    const cached = translationCache.get(cacheKey);
    if (cached) {
        return cached;
    }
    
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${to}&dt=t&q=${encodeURIComponent(text)}`;
    
    for (let attempt = 1; attempt <= retries; attempt++) {
        try {
            const res = await fetch(url);
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }
            const data: any = await res.json();
            const result = data[0]?.map((seg: any) => seg[0]).join("") || text;
            
            // Cache hasil yang berhasil
            translationCache.set(cacheKey, result);
            return result;
            
        } catch (error) {
            Logger.error(`Translation attempt ${attempt} failed for language ${to}`, error);
            
            if (attempt === retries) {
                Logger.warn(`Final translation failure for: ${text.substring(0, 50)}...`);
                return text;
            }
            
            // Exponential backoff
            await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        }
    }
    
    return text;
}

// 🛡️ Protection Management Functions
export function loadProtectedPhrases(workspace: string): ProtectedData {
    const protectedPath = path.join(workspace, PROTECTED_FILE);
    if (!fs.existsSync(protectedPath)) {
        saveProtectedPhrases(workspace, { protected_phrases: DEFAULT_PROTECTED_PHRASES });
        return { protected_phrases: DEFAULT_PROTECTED_PHRASES };
    }
    
    try {
        const data = fs.readFileSync(protectedPath, "utf-8");
        const parsedData = JSON.parse(data);
        
        // Validate the data structure
        if (isValidProtectedData(parsedData)) {
            return parsedData;
        } else {
            Logger.warn('Invalid protected phrases data structure, using defaults');
            return { protected_phrases: DEFAULT_PROTECTED_PHRASES };
        }
    } catch (error) {
        Logger.error('Error loading protected phrases', error);
        return { protected_phrases: DEFAULT_PROTECTED_PHRASES };
    }
}

export function saveProtectedPhrases(workspace: string, data: ProtectedData): void {
    try {
        const protectedPath = path.join(workspace, PROTECTED_FILE);
        fs.writeFileSync(protectedPath, JSON.stringify(data, null, 2), "utf-8");
    } catch (error) {
        Logger.error('Error saving protected phrases', error);
        throw error;
    }
}

export function isProtectEnabled(workspace: string): boolean {
    const statusPath = path.join(workspace, PROTECT_STATUS_FILE);
    return fs.existsSync(statusPath);
}

export function setProtectStatus(workspace: string, enabled: boolean): void {
    const statusPath = path.join(workspace, PROTECT_STATUS_FILE);
    try {
        if (enabled) {
            fs.writeFileSync(statusPath, "");
        } else {
            if (fs.existsSync(statusPath)) {
                fs.unlinkSync(statusPath);
            }
        }
    } catch (error) {
        Logger.error('Error setting protection status', error);
        throw error;
    }
}

// 🔄 GitHub Repository Detection Functions
export function getGitHubRepoUrl(workspace: string): string | null {
    // Coba dari package.json pertama
    try {
        const packageJsonPath = path.join(workspace, PACKAGE_JSON);
        if (fs.existsSync(packageJsonPath)) {
            const packageData = JSON.parse(fs.readFileSync(packageJsonPath, "utf-8"));
            if (packageData.repository) {
                let repoUrl = '';
                if (typeof packageData.repository === 'string') {
                    repoUrl = packageData.repository;
                } else if (packageData.repository.url) {
                    repoUrl = packageData.repository.url;
                }
                
                // Normalize URL
                if (repoUrl) {
                    // Handle git+https:// format
                    repoUrl = repoUrl.replace(/^git\+/, '');
                    // Handle git@github.com: format
                    repoUrl = repoUrl.replace(/^git@github.com:/, 'https://github.com/');
                    // Handle .git suffix
                    repoUrl = repoUrl.replace(/\.git$/, '');
                    // Ensure it's a GitHub URL
                    if (repoUrl.includes('github.com')) {
                        Logger.log(`GitHub URL detected from package.json: ${repoUrl}`);
                        return repoUrl;
                    }
                }
            }
        }
    } catch (error) {
        Logger.error('Error reading package.json for GitHub URL', error);
    }
    
    // Coba dari .git/config
    try {
        const gitConfigPath = path.join(workspace, '.git', 'config');
        if (fs.existsSync(gitConfigPath)) {
            const gitConfig = fs.readFileSync(gitConfigPath, 'utf-8');
            const urlMatch = gitConfig.match(/url\s*=\s*(.+)/);
            if (urlMatch && urlMatch[1]) {
                let repoUrl = urlMatch[1].trim();
                // Normalize URL
                repoUrl = repoUrl.replace(/^git@github.com:/, 'https://github.com/');
                repoUrl = repoUrl.replace(/\.git$/, '');
                if (repoUrl.includes('github.com')) {
                    Logger.log(`GitHub URL detected from .git/config: ${repoUrl}`);
                    return repoUrl;
                }
            }
        }
    } catch (error) {
        Logger.error('Error reading .git/config for GitHub URL', error);
    }
    
    // Fallback: cari di README.md
    try {
        const readmePath = path.join(workspace, SOURCE_FILE);
        if (fs.existsSync(readmePath)) {
            const readmeContent = fs.readFileSync(readmePath, 'utf-8');
            const githubUrlMatch = readmeContent.match(/https:\/\/github\.com\/[a-zA-Z0-9-]+\/[a-zA-Z0-9-_.]+/);
            if (githubUrlMatch) {
                Logger.log(`GitHub URL detected from README: ${githubUrlMatch[0]}`);
                return githubUrlMatch[0];
            }
        }
    } catch (error) {
        Logger.error('Error searching GitHub URL in README', error);
    }
    
    Logger.warn('No GitHub URL detected');
    return null;
}

export function getGitHubReleasesUrl(workspace: string): string {
    const repoUrl = getGitHubRepoUrl(workspace);
    if (repoUrl) {
        return `${repoUrl}/releases`;
    }
    
    // Fallback default (untuk extension ini sendiri)
    return "https://github.com/fatonyahmadfauzi/MultiDoc-Translator/releases";
}

// 🔄 CHANGELOG FUNCTIONS
export function hasChangelogFile(workspace: string): boolean {
    const changelogPath = path.join(workspace, CHANGELOG_FILE);
    return fs.existsSync(changelogPath);
}

export function hasChangelogSectionInReadme(workspace: string): boolean {
    const sourcePath = path.join(workspace, SOURCE_FILE);
    if (!fs.existsSync(sourcePath)) {
        return false;
    }
    
    const content = fs.readFileSync(sourcePath, "utf-8");
    
    // Check patterns for Changelog section
    const patterns = [
        /##\s+🧾\s+Changelog/,
        /##\s+Changelog/,
        /#+\s+Changelog/
    ];
    
    for (const pattern of patterns) {
        if (pattern.test(content)) {
            return true;
        }
    }
    
    return false;
}

export function fixExistingChangelogSpacing(workspace: string): boolean {
    if (!hasChangelogSectionInReadme(workspace)) {
        return false;
    }
    
    try {
        const sourcePath = path.join(workspace, SOURCE_FILE);
        let content = fs.readFileSync(sourcePath, "utf-8");
        
        let changesMade = false;
        
        // 1. Fix pattern: --- directly followed by ## 🧾 Changelog
        // Becomes: --- + 1 empty line + ## 🧾 Changelog
        const oldPattern = /---\s*\n\s*## 🧾 Changelog/g;
        const newPattern = '---\n\n## 🧾 Changelog';
        
        if (oldPattern.test(content)) {
            content = content.replace(oldPattern, newPattern);
            changesMade = true;
        }
        
        // 2. Check if there's separator between Changelog and License
        if (content.includes('## 🧾 Changelog') && content.includes('## 🧾 License')) {
            const betweenSections = content.match(/## 🧾 Changelog.*?(## 🧾 License)/s);
            if (betweenSections && !betweenSections[0].includes('---')) {
                // Add --- before License
                content = content.replace(
                    /(## 🧾 Changelog.*?)(## 🧾 License)/s,
                    '$1\n\n---\n\n$2'
                );
                changesMade = true;
            }
        }
        
        if (changesMade) {
            fs.writeFileSync(sourcePath, content, "utf-8");
            Logger.log("Fixed changelog section spacing and separators in README.md");
            return true;
        }
        
        return false;
        
    } catch (error) {
        Logger.error('Failed to fix changelog spacing', error);
        return false;
    }
}

export function addChangelogSectionToReadme(workspace: string): boolean {
    if (!hasChangelogFile(workspace)) {
        Logger.error("No CHANGELOG.md file found in root directory");
        return false;
    }
    
    if (hasChangelogSectionInReadme(workspace)) {
        Logger.log("Changelog section already exists in README.md");
        // Fix spacing if already exists
        fixExistingChangelogSpacing(workspace);
        return true;
    }
    
    try {
        const sourcePath = path.join(workspace, SOURCE_FILE);
        let content = fs.readFileSync(sourcePath, "utf-8");
        
        // Dapatkan GitHub Releases URL yang dinamis
        const githubReleasesUrl = getGitHubReleasesUrl(workspace);
        
        // Find position before License section to add Changelog
        const licensePattern = /##\s+🧾\s+License/gi;
        const licenseMatch = licensePattern.exec(content);
        
        // Changelog section with correct format including separators
        const changelogSection = `

---

## 🧾 Changelog

See all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.

> 📦 You can also view release notes directly on the [GitHub Releases page](${githubReleasesUrl}).

`;
        
        if (licenseMatch) {
            // Insert before License section
            const position = licenseMatch.index;
            
            // Check if there's already --- before License
            const contentBeforeLicense = content.substring(0, position).trimEnd();
            if (contentBeforeLicense.endsWith('---')) {
                // If --- already exists, we just need to add Changelog section
                // Remove existing --- and replace with complete section
                const lastDashPos = contentBeforeLicense.lastIndexOf('---');
                content = content.substring(0, lastDashPos).trimEnd() + changelogSection + content.substring(position);
            } else {
                // If no ---, add complete section with ---
                content = content.substring(0, position) + changelogSection + content.substring(position);
            }
        } else {
            // Add at the end of file before License if exists
            if (content.includes("## 🧾 License")) {
                const licensePos = content.indexOf("## 🧾 License");
                const contentBeforeLicense = content.substring(0, licensePos).trimEnd();
                
                if (contentBeforeLicense.endsWith('---')) {
                    // If --- already exists, replace with complete section
                    const lastDashPos = contentBeforeLicense.lastIndexOf('---');
                    content = content.substring(0, lastDashPos).trimEnd() + changelogSection + content.substring(licensePos);
                } else {
                    // If no ---, add complete section
                    content = content.substring(0, licensePos) + changelogSection + content.substring(licensePos);
                }
            } else {
                // Add at the end of file with separator
                if (content.trim().endsWith('---')) {
                    content = content.trimEnd() + '\n\n## 🧾 Changelog\n\nSee all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.\n\n> 📦 You can also view release notes directly on the [GitHub Releases page](${githubReleasesUrl}).';
                } else {
                    content = content.trim() + '\n\n---\n\n## 🧾 Changelog\n\nSee all notable changes for each version in the [CHANGELOG.md](CHANGELOG.md) file.\n\n> 📦 You can also view release notes directly on the [GitHub Releases page](${githubReleasesUrl}).';
                }
            }
        }
        
        // Final cleanup: ensure correct format
        // Pattern: --- followed by 1 empty line, then ## 🧾 Changelog
        content = content.replace(/---\s*\n\s*## 🧾 Changelog/g, '---\n\n## 🧾 Changelog');
        
        // Also ensure there's --- before License
        if (content.includes('## 🧾 Changelog') && content.includes('## 🧾 License')) {
            // Check if there's --- between Changelog and License
            const betweenSections = content.match(/## 🧾 Changelog.*?(## 🧾 License)/s);
            if (betweenSections && !betweenSections[0].includes('---')) {
                // Add --- before License
                content = content.replace(
                    /(## 🧾 Changelog.*?)(## 🧾 License)/s,
                    '$1\n\n---\n\n$2'
                );
            }
        }
        
        // Also fix if there are multiple empty lines
        content = content.replace(/\n\n\n+/g, '\n\n');
        
        fs.writeFileSync(sourcePath, content, "utf-8");
        
        Logger.log("Changelog section added to README.md with proper spacing and separators");
        Logger.log(`GitHub Releases URL: ${githubReleasesUrl}`);
        return true;
        
    } catch (error) {
        Logger.error('Failed to add changelog section', error);
        return false;
    }
}

// Fungsi untuk proteksi yang lebih kuat - UNIVERSAL: TANPA PROTEKSI AUTHOR & VERSION
export function createPlaceholderProtection(text: string, protectedPhrases: string[]): { text: string, placeholders: Record<string, string> } {
    let protectedText = text;
    const placeholders: Record<string, string> = {};
    let counter = 0;

    // Fungsi helper untuk proteksi dengan tracking yang lebih baik
    const protectPattern = (pattern: RegExp, key: string) => {
        protectedText = protectedText.replace(pattern, (match) => {
            // Hindari duplikasi placeholder untuk match yang sama
            const existingEntry = Object.entries(placeholders).find(([_, value]) => value === match);
            if (existingEntry) {
                return existingEntry[0];
            }
            
            const placeholder = `__${key}_${counter++}__`;
            placeholders[placeholder] = match;
            return placeholder;
        });
    };

    // 1. Proteksi MIT License TANPA author name (UNIVERSAL)
    protectPattern(/MIT\s+License/g, 'LICENSE_TEXT');
    protectPattern(/\(LICENSE\)/g, 'LICENSEREF');
    protectPattern(/\(\.\.\/\.\.\/LICENSE\)/g, 'LICENSEPATH');
    
    // 2. Proteksi nama project baru
    protectPattern(/MultiDoc-Translator/g, 'PROJECT_NAME');
    protectPattern(/MultiDoc Translator/g, 'PROJECT_NAME_SPACE');
    
    // 3. Proteksi inline code
    protectPattern(/`[^`\n\r]+`/g, 'INLINECODE');
    
    // 4. Proteksi blok kode
    protectPattern(/```[\s\S]*?```/g, 'CODEBLOCK');
    
    // 5. Proteksi URL dan links
    protectPattern(/https?:\/\/[^\s\)]+/g, 'URL');
    protectPattern(/\[[^\]]*\]\([^)]+\)/g, 'MDLINK');
    
    // 6. Proteksi command dan shortcuts
    protectPattern(/Ctrl \+ Alt \+ P/g, 'SHORTCUT');
    protectPattern(/F5/g, 'F5KEY');
    protectPattern(/Ctrl\+Shift\+X/g, 'EXTSHORTCUT');
    
    // 7. Proteksi brand dan nama (TANPA author spesifik)
    protectPattern(/Visual Studio Code/g, 'VSCODE');
    protectPattern(/VS Code/g, 'VSCODE_SHORT');
    protectPattern(/GitHub/g, 'GITHUB');
    
    // 8. Proteksi OS (tetap dipertahankan karena universal)
    protectPattern(/\*\*Windows\*\*/g, 'WINDOWS');
    protectPattern(/\*\*macOS\*\*/g, 'MACOS');
    protectPattern(/\*\*Linux\*\*/g, 'LINUX');
    protectPattern(/\*\*Windows, macOS and Linux\*\*/g, 'ALLOS');
    
    // 9. Proteksi istilah teknis (tetap universal)
    protectPattern(/\bLint\b/g, 'LINT');
    protectPattern(/\bTypeScript\b/g, 'TYPESCRIPT');
    protectPattern(/\bJavaScript\b/g, 'JAVASCRIPT');
    protectPattern(/\bHTML\b/g, 'HTML');
    protectPattern(/\bCSS\b/g, 'CSS');
    protectPattern(/\bnpm\b/g, 'NPM');
    protectPattern(/\bNode\.js\b/g, 'NODEJS');

    // 10. Proteksi menggunakan frasa custom
    const isProtectionEnabled = true;
    if (isProtectionEnabled) {
        for (const phrase of protectedPhrases) {
            try {
                const regex = new RegExp(phrase, 'g');
                protectPattern(regex, 'CUSTOM');
            } catch (error) {
                Logger.warn(`Invalid regex pattern: ${phrase}`);
            }
        }
    }

    return { text: protectedText, placeholders };
}

// Fungsi untuk restore placeholder - PERBAIKAN: lebih robust
export function restorePlaceholders(text: string, placeholders: Record<string, string>): string {
    let restoredText = text;
    
    // Restore dalam urutan yang tepat untuk menghindari konflik
    const sortedPlaceholders = Object.entries(placeholders)
        .sort(([a], [b]) => {
            // Prioritaskan placeholder yang lebih panjang dulu
            return b.length - a.length;
        });
    
    for (const [placeholder, original] of sortedPlaceholders) {
        // Gunakan global replace dengan regex escape
        const escapedPlaceholder = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(escapedPlaceholder, 'g');
        restoredText = restoredText.replace(regex, original);
    }
    
    return restoredText;
}

// Fungsi untuk perbaikan formatting setelah terjemahan
export function fixPostTranslationFormatting(translated: string, originalLine: string): string {
    if (!translated.trim()) {
        return translated;
    }

    // 1. Perbaiki bullet points
    translated = translated.replace(/^-(?=[^\s-])/gm, '- ');
    
    // 2. Perbaiki non-breaking space
    translated = translated.replace(/\xa0/g, ' ');
    
    // 3. Perbaiki format bold yang rusak
    translated = translated
        .replace(/\*\s*\*([^*]+)\*\s*\*/g, '**$1**')
        .replace(/\*\*([^*]+)\*\s*\*/g, '**$1**');
    
    // 4. Perbaiki list formatting
    translated = translated.replace(/^(\s*[-*+])(?![*\s-])(\S)/gm, '$1 $2');
    
    // 5. Perbaiki colon formatting tanpa merusak bold text
    translated = translated.replace(
        /([a-zA-Z\u00C0-\u024F])\s*:\s*(\*\*[^*]+\*\*)/g,
        '$1 : $2'
    );
    
    // 6. Perbaiki extra parenthesis
    translated = translated.replace(
        /(\[[^\]]*\]\([^)]+\))\.\)/g,
        '$1)'
    );
    
    // 7. Perbaiki bold text dengan colon
    translated = translated.replace(
        /\*\*([a-zA-Z\u00C0-\u024F]+)\s*:\s*\*\*/g,
        '**$1:**'
    );
    
    // 8. Perbaiki spasi setelah bullet points
    translated = translated.replace(/^([-*+])\s*(\S)/gm, '$1 $2');
    
    // Kembalikan indentasi asli
    const indent = originalLine.match(/^\s*/)?.[0] ?? "";
    return indent + translated.trim();
}

// Fungsi final cleanup - UNIVERSAL: TANPA PERBAIKAN AUTHOR & VERSION SPESIFIK
export function finalCleanup(text: string): string {
    // Hapus semua placeholder yang tersisa dengan pattern yang lebih komprehensif
    let cleaned = text.replace(/__[A-Za-z_]+_\d+__/g, '');
    
    // Hapus baris yang hanya berisi placeholder
    cleaned = cleaned.replace(/^\s*__[A-Za-z_]+_\d+__\s*$/gm, '');
    
    // Perbaikan formatting yang mungkin rusak (UMUM)
    cleaned = cleaned
        .replace(/\*\* \*\*/g, '')
        .replace(/\*\*(\w+)\s*\*\*/g, '**$1**')
        .replace(/`\s+`/g, '')
        .replace(/\s+\./g, '.')
        .replace(/\s+,/g, ',')
        .replace(/\s+:/g, ':')
        // PERBAIKAN: Hapus baris kosong berlebih - hanya 1 baris kosong maksimal
        .replace(/\n{3,}/g, '\n\n')
        .replace(/^\s*[\r\n]+/gm, '\n')
        .trim();
    
    return cleaned;
}

// Helper function untuk mendapatkan bahasa yang sudah ada
export function getExistingTranslatedLanguages(workspace: string): string[] {
    const outputDir = path.join(workspace, OUTPUT_DIR);
    const existingLangs: string[] = [];
    
    if (fs.existsSync(outputDir)) {
        try {
            const files = fs.readdirSync(outputDir);
            files.forEach(file => {
                const match = file.match(/README-([A-Z]+)\.md/);
                if (match && match[1].toLowerCase() in LANGUAGES) {
                    existingLangs.push(match[1].toLowerCase());
                }
            });
        } catch (error) {
            Logger.error('Error reading output directory', error);
        }
    }
    
    return existingLangs;
}

// Fungsi untuk perbaikan tambahan setelah terjemahan - UNIVERSAL
export function applyPostTranslationFixes(text: string, langCode: string): string {
    // Perbaikan khusus untuk bahasa Indonesia
    if (langCode === 'id') {
        // Pastikan istilah teknis tidak diterjemahkan
        text = text.replace(/(?<!\w)(Lint|TypeScript|JavaScript|HTML|CSS|npm|Node\.js|MultiDoc-Translator)(?!\w)/gi, (match) => {
            return match;
        });
    }

    // Perbaikan umum untuk semua bahasa (TANPA versi spesifik)
    text = text
        // Pastikan nama project tetap utuh
        .replace(/(\*\*)?MultiDoc-Translator(\*\*)?/g, '**MultiDoc-Translator**')
        .replace(/(\*\*)?MultiDoc Translator(\*\*)?/g, '**MultiDoc-Translator**')
        // Pastikan OS tetap bold (universal)
        .replace(/(\*\*)?Windows(\*\*)?/g, '**Windows**')
        .replace(/(\*\*)?macOS(\*\*)?/g, '**macOS**')
        .replace(/(\*\*)?Linux(\*\*)?/g, '**Linux**')
        // Pastikan kombinasi OS tetap konsisten
        .replace(/\*\*Windows\*\*,?\s*\*\*macOS\*\*,?\s*(and|et|und|y|и|dan)\s*\*\*Linux\*\*/g, '**Windows**, **macOS** and **Linux**')
        // Pastikan tag HTML tetap utuh
        .replace(/&lt;(script|link|img)/g, '<$1')
        .replace(/&lt;\/script&gt;/g, '</script>')
        .replace(/&lt;br\s*\/?&gt;/g, '<br/>')
        // PERBAIKAN: Hapus baris kosong berlebih
        .replace(/\n{3,}/g, '\n\n');

    return text;
}

// 🗑️ Functions to Remove Language Files
export function removeLanguageFiles(langCodes: string[], workspace: string): string[] {
    const removedLangs: string[] = [];
    const outputDir = path.join(workspace, OUTPUT_DIR);

    for (const langCode of langCodes) {
        if (langCode in LANGUAGES) {
            const readmePath = path.join(outputDir, `README-${langCode.toUpperCase()}.md`);
            const changelogPath = path.join(outputDir, `CHANGELOG-${langCode.toUpperCase()}.md`);
            
            // Hapus file README
            if (fs.existsSync(readmePath)) {
                try {
                    fs.unlinkSync(readmePath);
                    removedLangs.push(langCode);
                    Logger.log(`File README-${langCode.toUpperCase()}.md successfully deleted`);
                } catch (error) {
                    Logger.error(`Failed to delete README-${langCode.toUpperCase()}.md`, error);
                }
            } else {
                Logger.warn(`File README-${langCode.toUpperCase()}.md not found`);
            }
            
            // Hapus file CHANGELOG jika ada
            if (fs.existsSync(changelogPath)) {
                try {
                    fs.unlinkSync(changelogPath);
                    Logger.log(`File CHANGELOG-${langCode.toUpperCase()}.md successfully deleted`);
                } catch (error) {
                    Logger.error(`Failed to delete CHANGELOG-${langCode.toUpperCase()}.md`, error);
                }
            }
        } else {
            Logger.error(`Language code '${langCode}' not recognized`);
        }
    }

    return removedLangs;
}

// 🗑️ Function to Remove All Language Files
export function removeAllLanguageFiles(workspace: string): string[] {
    const outputDir = path.join(workspace, OUTPUT_DIR);
    const allRemovedLangs: string[] = [];

    if (!fs.existsSync(outputDir)) {
        Logger.log("No translation files found");
        return [];
    }

    try {
        // Dapatkan semua bahasa yang sudah ada sebelum menghapus
        const existingLangs: string[] = [];
        const files = fs.readdirSync(outputDir);
        const readmeFiles = files.filter(file => file.startsWith("README-") && file.endsWith(".md"));

        for (const file of readmeFiles) {
            const langCodeMatch = file.match(/README-([A-Z]+)\.md/);
            if (langCodeMatch) {
                const langCode = langCodeMatch[1].toLowerCase();
                existingLangs.push(langCode);
                try {
                    fs.unlinkSync(path.join(outputDir, file));
                    allRemovedLangs.push(langCode);
                    Logger.log(`File ${file} successfully deleted`);
                } catch (error) {
                    Logger.error(`Failed to delete ${file}`, error);
                }
            }
        }

        // Hapus semua file CHANGELOG
        const changelogFiles = files.filter(file => file.startsWith("CHANGELOG-") && file.endsWith(".md"));
        for (const file of changelogFiles) {
            try {
                fs.unlinkSync(path.join(outputDir, file));
                Logger.log(`File ${file} successfully deleted`);
            } catch (error) {
                Logger.error(`Failed to delete ${file}`, error);
            }
        }

        // Hapus folder docs/lang jika kosong, lalu docs jika juga kosong
        try {
            if (fs.existsSync(outputDir)) {
                const remainingFiles = fs.readdirSync(outputDir);
                if (remainingFiles.length === 0) {
                    fs.rmdirSync(outputDir);
                    Logger.log(`Folder ${outputDir} successfully deleted (empty)`);
                    
                    // Cek apakah folder docs juga kosong, jika ya hapus
                    const docsDir = path.dirname(outputDir);
                    if (fs.existsSync(docsDir) && fs.readdirSync(docsDir).length === 0) {
                        fs.rmdirSync(docsDir);
                        Logger.log(`Folder ${docsDir} successfully deleted (empty)`);
                    }
                }
            }
        } catch (error) {
            Logger.error('Failed to delete folder', error);
        }
    } catch (error) {
        Logger.error('Error in removeAllLanguageFiles', error);
    }

    // Update README utama untuk menghapus language switcher dan rapikan baris kosong
    try {
        const sourceFile = path.join(workspace, SOURCE_FILE);
        if (fs.existsSync(sourceFile)) {
            let content = fs.readFileSync(sourceFile, "utf-8");
            
            // Hapus language switcher dengan pattern yang lebih komprehensif
            const switcherPatterns = [
                /> 🌐 Available in other languages:[^\n]*(\n|$)/g,
                /> 🌐 Tersedia dalam bahasa lain:[^\n]*(\n|$)/g,
                /> 🌐 Disponible dans d'autres langues:[^\n]*(\n|$)/g,
                /> 🌐 Disponible dans d'autres langues :[^\n]*(\n|$)/g,
                /> 🌐 In anderen Sprachen verfügbar:[^\n]*(\n|$)/g,
                /> 🌐 他の言語でも利用可能:[^\n]*(\n|$)/g,
                /> 🌐 提供其他语言版本：[^\n]*(\n|$)/g,
                /> 🌐 Disponible en otros idiomas:[^\n]*(\n|$)/g,
                /> 🌐 Dostępne w innych językach:[^\n]*(\n|$)/g,
                /> 🌐 Доступно на他の言語で:[^\n]*(\n|$)/g,
                /> 🌐 Disponível em outros idiomas:[^\n]*(\n|$)/g,
                /> 🌐 다른 언어로도 사용 가능:[^\n]*(\n|$)/g
            ];
            
            for (const pattern of switcherPatterns) {
                content = content.replace(pattern, '');
            }
            
            // Rapikan baris kosong berlebih - PERBAIKAN: hanya 1 baris kosong maksimal
            content = content.replace(/\n{3,}/g, '\n\n');
            
            fs.writeFileSync(sourceFile, content, "utf-8");
            Logger.log("Language switcher removed from main README and empty lines cleaned up");
        }
    } catch (error) {
        Logger.error('Failed to update main README', error);
    }

    return allRemovedLangs;
}

// 🔄 PERBAIKAN BESAR: Update language switcher dengan urutan sesuai Python
export function updateLanguageSwitcher(workspace: string, newLanguages?: string[], removedLanguages?: string[]): void {
    const sourceFile = path.join(workspace, SOURCE_FILE);
    const outputDir = path.join(workspace, OUTPUT_DIR);

    if (!fs.existsSync(sourceFile)) {
        return;
    }

    try {
        // Dapatkan semua bahasa yang sudah ada
        const existingLangs = getExistingTranslatedLanguages(workspace);

        // Jika ada bahasa baru, tambahkan ke daftar existing
        if (newLanguages) {
            for (const lang of newLanguages) {
                if (!existingLangs.includes(lang)) {
                    existingLangs.push(lang);
                }
            }
        }

        // Jika ada bahasa yang dihapus, hapus dari daftar existing
        if (removedLanguages) {
            for (const lang of removedLanguages) {
                const index = existingLangs.indexOf(lang);
                if (index > -1) {
                    existingLangs.splice(index, 1);
                }
            }
        }

        // PERBAIKAN: Urutkan bahasa sesuai urutan di LANGUAGES (seperti Python)
        const sortedExistingLangs = Object.keys(LANGUAGES).filter(code => 
            existingLangs.includes(code) && code !== 'en' // Filter out English
        );

        // PERBAIKAN: Update README utama (English) dengan spacing yang benar
        let content = fs.readFileSync(sourceFile, "utf-8");

        // Buat daftar link untuk README utama - URUTAN SESUAI PYTHON
        const langLinks: string[] = [];
        for (const code of sortedExistingLangs) {
            if (code in LANGUAGES) {
                const name = LANGUAGES[code][0];
                langLinks.push(`[${name}](docs/lang/README-${code.toUpperCase()}.md)`);
            }
        }

        if (langLinks.length > 0) {
            const switcher = `> 🌐 Available in other languages: ${langLinks.join(" | ")}`;
            
            // PERBAIKAN: Hapus SEMUA kemungkinan language switcher yang sudah ada dengan pattern yang tepat
            const switcherPatterns = [
                /> 🌐 Available in other languages:[^\n]*(\n|$)/g,
                /> 🌐 Tersedia dalam bahasa lain:[^\n]*(\n|$)/g,
                /> 🌐 Disponible dans d'autres langues:[^\n]*(\n|$)/g,
                /> 🌐 Disponible dans d'autres langues :[^\n]*(\n|$)/g,
                /> 🌐 In anderen Sprachen verfügbar:[^\n]*(\n|$)/g,
                /> 🌐 他の言語でも利用可能:[^\n]*(\n|$)/g,
                /> 🌐 提供其他语言版本：[^\n]*(\n|$)/g,
                /> 🌐 Disponible en otros idiomas:[^\n]*(\n|$)/g,
                /> 🌐 Dostępne w innych językach:[^\n]*(\n|$)/g,
                /> 🌐 Доступно на他の言語で:[^\n]*(\n|$)/g,
                /> 🌐 Disponível em outros idiomas:[^\n]*(\n|$)/g,
                /> 🌐 다른 언어로도 사용 가능:[^\n]*(\n|$)/g
            ];
            
            for (const pattern of switcherPatterns) {
                content = content.replace(pattern, '');
            }
            
            // PERBAIKAN: Cari posisi yang tepat untuk menambahkan switcher - SEBELUM --- dengan spacing yang benar
            const lines = content.split('\n');
            let insertIndex = -1;
            
            // Cari garis pemisah pertama (---)
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].trim().match(/^-{3,}$/)) {
                    insertIndex = i;
                    break;
                }
            }
            
            if (insertIndex !== -1) {
                // PERBAIKAN: Sisipkan switcher tepat sebelum garis pemisah dengan 1 baris kosong
                lines.splice(insertIndex, 0, switcher, '');
                content = lines.join('\n');
            } else {
                // Jika tidak ada garis pemisah, tambahkan di akhir header dengan spacing yang benar
                const headerEnd = content.indexOf('\n\n');
                if (headerEnd !== -1) {
                    content = content.slice(0, headerEnd) + '\n\n' + switcher + '\n' + content.slice(headerEnd);
                } else {
                    content = content.trim() + '\n\n' + switcher + '\n';
                }
            }
            
            // PERBAIKAN: Rapikan baris kosong berlebih
            content = content.replace(/\n{3,}/g, '\n\n');
        } else {
            // Hapus semua language switcher jika tidak ada bahasa lain
            const switcherPatterns = [
                /> 🌐 Available in other languages:[^\n]*(\n|$)/g,
                /> 🌐 Tersedia dalam bahasa lain:[^\n]*(\n|$)/g,
                /> 🌐 Disponible dans d'autres langues:[^\n]*(\n|$)/g,
                /> 🌐 Disponible dans d'autres langues :[^\n]*(\n|$)/g
            ];
            
            for (const pattern of switcherPatterns) {
                content = content.replace(pattern, '');
            }
            
            // PERBAIKAN: Rapikan baris kosong berlebih
            content = content.replace(/\n{3,}/g, '\n\n');
        }

        fs.writeFileSync(sourceFile, content, "utf-8");
        Logger.log(`Language switcher in main README updated: ${sortedExistingLangs.join(', ') || 'No other languages'}`);
    } catch (error) {
        Logger.error('Failed to update language switcher in main README', error);
    }

    // PERBAIKAN KHUSUS: Update semua README yang sudah diterjemahkan dengan spacing yang benar dan tanpa duplikasi
    for (const langCode of getExistingTranslatedLanguages(workspace)) {
        if (langCode in LANGUAGES) {
            const [langName, , introText] = LANGUAGES[langCode];
            const readmePath = path.join(outputDir, `README-${langCode.toUpperCase()}.md`);
            
            if (fs.existsSync(readmePath)) {
                try {
                    let content = fs.readFileSync(readmePath, "utf-8");
                    
                    // PERBAIKAN: Buat daftar link untuk bahasa ini dengan urutan sesuai Python
                    // English selalu pertama, lalu bahasa lain sesuai urutan LANGUAGES
                    const links = ["[English](../../README.md)"];
                    for (const code of getExistingTranslatedLanguages(workspace)) {
                        if (code !== langCode) {
                            const name = LANGUAGES[code][0];
                            links.push(`[${name}](README-${code.toUpperCase()}.md)`);
                        }
                    }
                    
                    const linksText = links.join(" | ");
                    const newSwitcherLine = `> ${introText} ${linksText}`;
                    
                    // PERBAIKAN KHUSUS: Hapus SEMUA language switcher yang sudah ada untuk bahasa ini
                    // Termasuk semua variasi yang mungkin
                    const switcherPatterns = [
                        /> 🌐 Available in other languages:[^\n]*(\n|$)/g,
                        /> 🌐 Tersedia dalam bahasa lain:[^\n]*(\n|$)/g,
                        /> 🌐 Disponible dans d'autres langues:[^\n]*(\n|$)/g,
                        /> 🌐 Disponible dans d'autres langues :[^\n]*(\n|$)/g,
                        /> 🌐 In anderen Sprachen verfügbar:[^\n]*(\n|$)/g,
                        /> 🌐 他の言語でも利用可能:[^\n]*(\n|$)/g,
                        /> 🌐 提供其他语言版本：[^\n]*(\n|$)/g,
                        /> 🌐 Disponible en otros idiomas:[^\n]*(\n|$)/g,
                        /> 🌐 Dostępne w innych językach:[^\n]*(\n|$)/g,
                        /> 🌐 Доступно на他の言語で:[^\n]*(\n|$)/g,
                        /> 🌐 Disponível em outros idiomas:[^\n]*(\n|$)/g,
                        /> 🌐 다른 언어로도 사용 가능:[^\n]*(\n|$)/g
                    ];
                    
                    for (const pattern of switcherPatterns) {
                        content = content.replace(pattern, '');
                    }
                    
                    // PERBAIKAN: Cari posisi yang tepat untuk menambahkan switcher dengan spacing yang benar
                    const lines = content.split('\n');
                    let insertIndex = -1;
                    
                    // Cari garis pemisah pertama (---)
                    for (let i = 0; i < lines.length; i++) {
                        if (lines[i].trim().match(/^-{3,}$/)) {
                            insertIndex = i;
                            break;
                        }
                    }
                    
                    if (insertIndex !== -1) {
                        // PERBAIKAN: Sisipkan switcher tepat sebelum garis pemisah dengan 1 baris kosong
                        // Pastikan tidak ada duplikasi dengan memeriksa apakah sudah ada
                        const hasExistingSwitcher = lines.some(line => 
                            line.includes(introText) && line.startsWith('> 🌐')
                        );
                        
                        if (!hasExistingSwitcher) {
                            lines.splice(insertIndex, 0, newSwitcherLine, '');
                            content = lines.join('\n');
                        } else {
                            // Jika sudah ada, ganti yang sudah ada dengan yang baru
                            for (let i = 0; i < lines.length; i++) {
                                if (lines[i].includes(introText) && lines[i].startsWith('> 🌐')) {
                                    lines[i] = newSwitcherLine;
                                    break;
                                }
                            }
                            content = lines.join('\n');
                        }
                    } else {
                        // Jika tidak ada garis pemisah, tambahkan di akhir header dengan spacing yang benar
                        const headerEnd = content.indexOf('\n\n');
                        if (headerEnd !== -1) {
                            // Periksa apakah sudah ada switcher di header
                            const headerContent = content.slice(0, headerEnd);
                            const hasExistingSwitcher = headerContent.includes(introText) && headerContent.includes('> 🌐');
                            
                            if (!hasExistingSwitcher) {
                                content = content.slice(0, headerEnd) + '\n\n' + newSwitcherLine + '\n' + content.slice(headerEnd);
                            } else {
                                // Ganti yang sudah ada
                                content = content.replace(
                                    new RegExp(`> ${introText}[^\\n]*`, 'g'),
                                    newSwitcherLine
                                );
                            }
                        } else {
                            // Jika tidak ada header end, tambahkan di akhir dengan spacing
                            const hasExistingSwitcher = content.includes(introText) && content.includes('> 🌐');
                            if (!hasExistingSwitcher) {
                                content = content.trim() + '\n\n' + newSwitcherLine + '\n';
                            } else {
                                // Ganti yang sudah ada
                                content = content.replace(
                                    new RegExp(`> ${introText}[^\\n]*`, 'g'),
                                    newSwitcherLine
                                );
                            }
                        }
                    }
                    
                    // PERBAIKAN: Rapikan baris kosong berlebih dan pastikan tidak ada duplikasi
                    content = content.replace(/\n{3,}/g, '\n\n');
                    
                    // PERBAIKAN FINAL: Hapus duplikasi language switcher jika masih ada
                    const linesFinal = content.split('\n');
                    const uniqueLines: string[] = [];
                    let lastSwitcherLine = '';
                    
                    for (const line of linesFinal) {
                        if (line.startsWith('> 🌐') && line.includes(introText)) {
                            if (line !== lastSwitcherLine) {
                                uniqueLines.push(line);
                                lastSwitcherLine = line;
                            }
                            // Skip duplikat
                        } else {
                            uniqueLines.push(line);
                        }
                    }
                    
                    content = uniqueLines.join('\n');
                    
                    fs.writeFileSync(readmePath, content, "utf-8");
                    Logger.log(`Language switcher in README-${langCode.toUpperCase()} updated`);
                } catch (error) {
                    Logger.error(`Failed to update language switcher in README-${langCode.toUpperCase()}`, error);
                }
            }
        }
    }
}

// 🔄 NEW: Translate CHANGELOG function
export async function translateChangelog(
    langCode: string, 
    langInfo: [string, string, string], 
    protectedData: ProtectedData, 
    workspace: string
): Promise<boolean> {
    if (!hasChangelogFile(workspace)) {
        return false;
    }
    
    const [langName, translateCode] = langInfo;
    const changelogDestPath = path.join(workspace, OUTPUT_DIR, `CHANGELOG-${langCode.toUpperCase()}.md`);
    
    Logger.log(`Translating CHANGELOG to ${langName} (${langCode.toUpperCase()})`);
    
    try {
        const changelogPath = path.join(workspace, CHANGELOG_FILE);
        const changelogContent = fs.readFileSync(changelogPath, "utf-8");
        
        // Pisahkan header dan body CHANGELOG
        const parts = changelogContent.split(/\n-{3,}\n/);
        const changelogHeader = parts[0] || "";
        const changelogBody = parts.slice(1).join("\n---\n");
        
        // Terjemahkan judul CHANGELOG
        const translatedTitle = await translateWithGoogle("Changelog", translateCode);
        
        // Buat header yang sudah diterjemahkan
        let translatedHeader = changelogHeader;
        if (changelogHeader.includes("# Changelog")) {
            translatedHeader = changelogHeader.replace("# Changelog", `# ${translatedTitle}`);
        } else {
            translatedHeader = `# ${translatedTitle}\n\n${changelogHeader}`;
        }
        
        // Proses terjemahan body CHANGELOG
        const bodyLines = changelogBody.split(/\r?\n/);
        const translatedLines: string[] = [];
        let inCodeBlock = false;

        // Define changelog section headers to translate
        const sectionHeaders: Record<string, Record<string, string>> = {
            // Japanese headers
            jp: {
                "### Added": "### 追加",
                "### Changed": "### 変更",
                "### Fixed": "### 修正",
                "### Removed": "### 削除",
                "### Deprecated": "### 非推奨",
                "### Breaking Changes": "### 重大な変更"
            },
            // Chinese headers
            zh: {
                "### Added": "### 新增",
                "### Changed": "### 更改",
                "### Fixed": "### 修复",
                "### Removed": "### 移除",
                "### Deprecated": "### 弃用",
                "### Breaking Changes": "### 重大变更"
            },
            // Indonesian headers
            id: {
                "### Added": "### Ditambahkan",
                "### Changed": "### Diubah",
                "### Fixed": "### Diperbaiki",
                "### Removed": "### Dihapus",
                "### Deprecated": "### Usang",
                "### Breaking Changes": "### Perubahan Besar"
            },
            // Korean headers (both ko and kr codes)
            ko: {
                "### Added": "### 추가됨",
                "### Changed": "### 변경됨",
                "### Fixed": "### 수정됨",
                "### Removed": "### 제거됨",
                "### Deprecated": "### 더 이상 사용되지 않음",
                "### Breaking Changes": "### 주요 변경 사항"
            },
            kr: {
                "### Added": "### 추가됨",
                "### Changed": "### 변경됨",
                "### Fixed": "### 수정됨",
                "### Removed": "### 제거됨",
                "### Deprecated": "### 더 이상 사용되지 않음",
                "### Breaking Changes": "### 주요 변경 사항"
            },
            // Polish headers
            pl: {
                "### Added": "### Dodano",
                "### Changed": "### Zmieniono",
                "### Fixed": "### Naprawiono",
                "### Removed": "### Usunięto",
                "### Deprecated": "### Przestarzałe",
                "### Breaking Changes": "### Istotne zmiany"
            },
            // Russian headers
            ru: {
                "### Added": "### Добавлено",
                "### Changed": "### Изменено",
                "### Fixed": "### Исправлено",
                "### Removed": "### Удалено",
                "### Deprecated": "### Устарело",
                "### Breaking Changes": "### Критические изменения"
            },
            // French headers
            fr: {
                "### Added": "### Ajouté",
                "### Changed": "### Modifié",
                "### Fixed": "### Corrigé",
                "### Removed": "### Supprimé",
                "### Deprecated": "### Obsolète",
                "### Breaking Changes": "### Changements majeurs"
            },
            // German headers
            de: {
                "### Added": "### Hinzugefügt",
                "### Changed": "### Geändert",
                "### Fixed": "### Behoben",
                "### Removed": "### Entfernt",
                "### Deprecated": "### Veraltet",
                "### Breaking Changes": "### Größere Änderungen"
            },
            // Spanish headers
            es: {
                "### Added": "### Añadido",
                "### Changed": "### Cambiado",
                "### Fixed": "### Corregido",
                "### Removed": "### Eliminado",
                "### Deprecated": "### Obsoleto",
                "### Breaking Changes": "### Cambios importantes"
            },
            // Portuguese headers
            pt: {
                "### Added": "### Adicionado",
                "### Changed": "### Alterado",
                "### Fixed": "### Corrigido",
                "### Removed": "### Removido",
                "### Deprecated": "### Obsoleto",
                "### Breaking Changes": "### Mudanças significativas"
            }
        };
        
        for (const line of bodyLines) {
            // Check if line is a changelog section header
            const headerMatch = line.match(/^(### (?:Added|Changed|Fixed|Removed|Deprecated|Breaking Changes))/);
            if (headerMatch) {
                const header = headerMatch[1];
                if (sectionHeaders[langCode] && sectionHeaders[langCode][header]) {
                    translatedLines.push(sectionHeaders[langCode][header]);
                    continue;
                }
            }
            // Deteksi blok kode
            if (line.trim().startsWith("```")) {
                inCodeBlock = !inCodeBlock;
                translatedLines.push(line);
                continue;
            }
            
            // Jika dalam blok kode, jangan terjemahkan
            if (inCodeBlock) {
                translatedLines.push(line);
                continue;
            }
            
            // Deteksi versi (format: ## [1.0.0] - 2024-01-01)
            const versionMatch = line.match(/^(##\s+\[[\d\.]+\]\s*-\s*\d{4}-\d{2}-\d{2})/);
            if (versionMatch) {
                translatedLines.push(line);
                continue;
            }
            
            // 🛡️ PERBAIKAN: Deteksi dan proteksi section headers changelog
            const sectionHeaderMatch = line.match(/^(###\s+(Fixed|Added|Changed|Removed|Security))/i);
            if (sectionHeaderMatch) {
                translatedLines.push(line);  // Jangan terjemahkan section header
                continue;
            }
            
            // Deteksi elemen struktural
            const isStructural = (
                /^\s*[-=]+\s*$/.test(line) ||  // Garis pemisah
                !line.trim() ||                 // Baris kosong
                /^\s*\[.*?\]:\s*/.test(line)   // Link references
            );
            
            if (isStructural) {
                translatedLines.push(line);
                continue;
            }
            
            // Proteksi teks sebelum terjemahan
            const { text: protectedText, placeholders } = createPlaceholderProtection(
                line, 
                protectedData.protected_phrases
            );

            // Terjemahkan teks yang sudah diproteksi
            let translated = await translateWithGoogle(protectedText, translateCode);

            // Restore placeholder ke teks asli
            translated = restorePlaceholders(translated, placeholders);

            // Perbaikan formatting setelah terjemahan
            translated = fixPostTranslationFormatting(translated, line);

            translatedLines.push(translated);
        }
        
        const translatedBody = translatedLines.join("\n");
        
        // Gabungkan header dan body
        let finalChangelog = `${translatedHeader}\n\n---\n${translatedBody}`;
        
        // Cleanup placeholder yang tersisa
        finalChangelog = finalChangelog.replace(/__[A-Za-z_]+_\d+__/g, '');
        
        // Tulis file CHANGELOG yang sudah diterjemahkan
        fs.writeFileSync(changelogDestPath, finalChangelog, "utf-8");
        
        Logger.log(`${changelogDestPath} successfully created`);
        return true;
        
    } catch (error) {
        Logger.error('Failed to translate CHANGELOG', error);
        return false;
    }
}

// 🔄 NEW: Update CHANGELOG links in translated README
export async function updateChangelogLinksInReadme(
    langCode: string, 
    langInfo: [string, string, string], 
    workspace: string
): Promise<void> {
    const readmePath = path.join(workspace, OUTPUT_DIR, `README-${langCode.toUpperCase()}.md`);
    const changelogDestPath = `CHANGELOG-${langCode.toUpperCase()}.md`;
    
    if (!fs.existsSync(readmePath)) {
        return;
    }
    
    try {
        let content = fs.readFileSync(readmePath, "utf-8");
        
        // Terjemahkan teks "Changelog" dan "release notes"
        const [, translateCode] = langInfo;
        const translatedChangelog = await translateWithGoogle("Changelog", translateCode);
        const translatedReleaseNotes = await translateWithGoogle("release notes", translateCode);
        const translatedView = await translateWithGoogle("view", translateCode);
        const translatedAlso = await translateWithGoogle("also", translateCode);
        const translatedYouCan = await translateWithGoogle("You can", translateCode);
        
        // Dapatkan GitHub Releases URL yang dinamis
        const githubReleasesUrl = getGitHubReleasesUrl(workspace);
        
        // Update judul Changelog section
        content = content.replace(
            /##\s+🧾\s+Changelog/gi,
            `## 🧾 ${translatedChangelog}`
        );
        
        // Update link ke file CHANGELOG yang sudah diterjemahkan
        content = content.replace(
            /\[CHANGELOG\.md\]\(CHANGELOG\.md\)/g,
            `[${translatedChangelog}](${changelogDestPath})`
        );
        
        // Update teks release notes dengan URL yang dinamis
        content = content.replace(
            /You can also view release notes directly on the \[GitHub Releases page\]\([^)]+\)/gi,
            `${translatedYouCan} ${translatedAlso} ${translatedView} ${translatedReleaseNotes} directly on the [GitHub Releases page](${githubReleasesUrl})`
        );
        
        fs.writeFileSync(readmePath, content, "utf-8");
        
        Logger.log(`Changelog links updated in README-${langCode.toUpperCase()}`);
        
    } catch (error) {
        Logger.error(`Failed to update changelog links in README-${langCode.toUpperCase()}`, error);
    }
}

// 🔄 NEW: Translate CHANGELOG only function
export async function translateChangelogOnly(
    langCodes: string[], 
    workspace: string, 
    progressOutput?: vscode.OutputChannel
): Promise<boolean> {
    if (!hasChangelogFile(workspace)) {
        if (progressOutput) {
            progressOutput.appendLine('No CHANGELOG.md file found in workspace');
        }
        return false;
    }
    
    const protectedData = loadProtectedPhrases(workspace);
    const l10n = getL10n();
    
    let successCount = 0;
    // Filter out English from language codes
    const filteredLangCodes = langCodes.filter(code => code !== 'en');

    for (const langCode of filteredLangCodes) {
        if (langCode in LANGUAGES) {
    if (progressOutput) {
        progressOutput.appendLine(l10n.t('progress.translatingTo', LANGUAGES[langCode][0], langCode.toUpperCase(), new Date().toLocaleTimeString()));
    }            if (await translateChangelog(langCode, LANGUAGES[langCode], protectedData, workspace)) {
                successCount++;
                
                // Update links in README if it exists
                await updateChangelogLinksInReadme(langCode, LANGUAGES[langCode], workspace);
            }
            
            // Delay untuk menghindari rate limiting
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    
    if (successCount > 0) {
        if (progressOutput) {
            progressOutput.appendLine(l10n.t('changelog.translationComplete', successCount));
        }
        return true;
    } else {
        if (progressOutput) {
            progressOutput.appendLine(l10n.t('changelog.translationFailed'));
        }
        return false;
    }
}

// PERBAIKAN: Fungsi utama untuk menerjemahkan README dengan spacing yang benar
export async function translateReadme(
    langCode: string, 
    langInfo: [string, string, string], 
    protectedData: ProtectedData, 
    workspace: string,
    progressOutput?: vscode.OutputChannel
): Promise<void> {
    const [langName, translateCode, introText] = langInfo;
    const srcPath = path.join(workspace, SOURCE_FILE);
    const outDir = path.join(workspace, OUTPUT_DIR);
    const destPath = path.join(outDir, `README-${langCode.toUpperCase()}.md`);
    const l10n = getL10n();

    if (!fs.existsSync(srcPath)) {
        throw new Error("README.md not found");
    }

    // Tampilkan progress mulai
    if (progressOutput) {
        const timestamp = new Date().toLocaleTimeString();
        // Get the l10n instance
        const l10n = getL10n();
        progressOutput.appendLine(l10n.t('progress.translatingTo', langName, langCode.toUpperCase(), timestamp));
    }

    const srcText = fs.readFileSync(srcPath, "utf-8");
    const parts = srcText.split(/\n-{3,}\n/);
    const srcHeader = parts[0] || "";
    const srcBody = parts.slice(1).join("\n---\n");

    // PERBAIKAN: Bersihkan SEMUA language switcher yang sudah ada dari header
    const switcherPatterns = [
        /> 🌐 Available in other languages:[^\n]*(\n|$)/g,
        /> 🌐 Tersedia dalam bahasa lain:[^\n]*(\n|$)/g,
        /> 🌐 Disponible dans d'autres langues:[^\n]*(\n|$)/g,
        /> 🌐 Disponible dans d'autres langues :[^\n]*(\n|$)/g,
        /> 🌐 In anderen Sprachen verfügbar:[^\n]*(\n|$)/g,
        /> 🌐 他の言語でも利用可能:[^\n]*(\n|$)/g,
        /> 🌐 提供其他语言版本：[^\n]*(\n|$)/g,
        /> 🌐 Disponible en otros idiomas:[^\n]*(\n|$)/g,
        /> 🌐 Dostępne w innych językach:[^\n]*(\n|$)/g,
        /> 🌐 Доступно на他の言語で:[^\n]*(\n|$)/g,
        /> 🌐 Disponível em outros idiomas:[^\n]*(\n|$)/g,
        /> 🌐 다른 언어로도 사용 가능:[^\n]*(\n|$)/g
    ];
    
    let cleanedHeader = srcHeader;
    for (const pattern of switcherPatterns) {
        cleanedHeader = cleanedHeader.replace(pattern, '');
    }
    cleanedHeader = cleanedHeader.trim();
    
    // Dapatkan semua bahasa yang sudah ada untuk membuat language switcher
    const existingLangs = getExistingTranslatedLanguages(workspace);
    
    // PERBAIKAN: Urutkan bahasa sesuai urutan di LANGUAGES (seperti Python)
    const sortedExistingLangs = Object.keys(LANGUAGES).filter(code => 
        existingLangs.includes(code)
    );
    
    // Buat language switcher untuk bahasa ini - URUTAN SESUAI PYTHON
    const links = ["[English](../../README.md)"];
    for (const code of sortedExistingLangs) {
        if (code !== langCode) {
            const name = LANGUAGES[code][0];
            links.push(`[${name}](README-${code.toUpperCase()}.md)`);
        }
    }
    
    const linksText = links.join(" | ");
    // PERBAIKAN: Gunakan hanya 1 baris kosong setelah header
    const finalHeader = `${cleanedHeader}\n\n> ${introText} ${linksText}`;

    const bodyLines = srcBody.split(/\r?\n/);
    const translatedLines: string[] = [];
    let inCodeBlock = false;
    let inExampleBlock = false;
    let inTable = false;
    let tableHeaderProcessed = false;
    let isFirstTableRow = true;

    // Progress tracking
    let totalLines = bodyLines.length;
    let processedLines = 0;

    for (const rawLine of bodyLines) {
        const line = rawLine;
        processedLines++;
        
        // 10行ごとに進捗を更新
        if (progressOutput && processedLines % 10 === 0) {
            const percent = Math.round((processedLines / totalLines) * 100);
            progressOutput.appendLine(l10n.t('progress.lineProgress', processedLines, totalLines, percent));
        }
        
        // コードブロックを検出
        if (line.trim().startsWith("```")) {
            inCodeBlock = !inCodeBlock;
            translatedLines.push(line);
            continue;
        }

        // Jika dalam blok kode, jangan terjemahkan sama sekali
        if (inCodeBlock) {
            translatedLines.push(line);
            continue;
        }

        // Deteksi tabel - HANYA HEADER YANG DITERJEMAHKAN
        if (/^\|.*\|$/.test(line)) {
            if (!inTable) {
                inTable = true;
                isFirstTableRow = true;
                tableHeaderProcessed = false;
            }
            
            // Baris pemisah tabel (|---|---|) - tidak diterjemahkan
            if (/^\|[\s:-|]+\|$/.test(line.trim())) {
                translatedLines.push(line);
                tableHeaderProcessed = true;
                isFirstTableRow = false;
                continue;
            }
            
            // HEADER TABEL (baris pertama) - DITERJEMAHKAN
            if (inTable && isFirstTableRow && !tableHeaderProcessed) {
                // Pisahkan kolom dan terjemahkan header
                const columns = line.split('|').map(col => col.trim());
                const translatedColumns: string[] = [];
                
                for (let i = 0; i < columns.length; i++) {
                    const col = columns[i];
                    
                    // Skip kolom kosong di awal dan akhir
                    if ((i === 0 && col === '') || (i === columns.length - 1 && col === '')) {
                        translatedColumns.push('');
                        continue;
                    }
                    
                    if (col && !/^[\s:-]*$/.test(col)) {
                        try {
                            // Proteksi teks sebelum terjemahan
                            const { text: protectedText, placeholders } = createPlaceholderProtection(
                                line, 
                                protectedData.protected_phrases
                            );

                            // Terjemahkan header kolom
                            let translatedCol = await translateWithGoogle(protectedText, translateCode);

                            // Restore placeholder ke teks asli
                            translatedCol = restorePlaceholders(translatedCol, placeholders);

                            // Perbaikan formatting
                            translatedCol = fixPostTranslationFormatting(translatedCol, col);
                            
                            // Pastikan teks tetap dalam format yang benar
                            translatedCol = translatedCol.trim();
                            translatedColumns.push(` ${translatedCol} `);
                        } catch (error) {
                            // Jika error, gunakan teks asli
                            translatedColumns.push(` ${col} `);
                        }
                    } else {
                        translatedColumns.push(col);
                    }
                }
                
                const translatedLine = '|' + translatedColumns.join('|') + '|';
                translatedLines.push(translatedLine);
                isFirstTableRow = false;
                tableHeaderProcessed = true;
                continue;
            }
            
            // DATA TABEL (baris setelah header) - TIDAK DITERJEMAHKAN
            if (inTable && tableHeaderProcessed) {
                translatedLines.push(line);
                continue;
            }
            
            translatedLines.push(line);
            continue;
        } else {
            // Keluar dari mode tabel
            if (inTable) {
                inTable = false;
                tableHeaderProcessed = false;
                isFirstTableRow = true;
            }
        }

        // Deteksi dan lewati baris dengan inline code yang penting
        const hasImportantInlineCode = /`(src|href|Ctrl \+ Alt \+ P|F5|Ctrl\+Shift\+X|MultiDoc-Translator)`/.test(line);
        if (hasImportantInlineCode) {
            translatedLines.push(line);
            continue;
        }

        // Deteksi bagian contoh (Before/After)
        if (/^\*\*Before:\*\*$/i.test(line)) {
            inExampleBlock = true;
            const translatedBefore = await translateWithGoogle("Before:", translateCode);
            translatedLines.push(`**${translatedBefore}**`);
            continue;
        }
        
        if (/^\*\*After \(Absolute\):\*\*$/i.test(line)) {
            inExampleBlock = true;
            const translatedAfter = await translateWithGoogle("After (Absolute):", translateCode);
            translatedLines.push(`**${translatedAfter}**`);
            continue;
        }

        if (/^\*\*After \(Relative\):\*\*$/i.test(line)) {
            inExampleBlock = true;
            const translatedAfter = await translateWithGoogle("After (Relative):", translateCode);
            translatedLines.push(`**${translatedAfter}**`);
            continue;
        }

        // Jika dalam blok contoh, jangan terjemahkan konten kode
        if (inExampleBlock) {
            translatedLines.push(line);
            if (inExampleBlock && !line.trim()) {
                inExampleBlock = false;
            }
            continue;
        }

        // Deteksi elemen struktural (baris kosong, dll)
        const isStructural = (
            /^\s*\|?[-:|\s]+\|?\s*$/.test(line) || 
            !line.trim()
        );
        
        if (isStructural) {
            translatedLines.push(line);
            continue;
        }

        // Proteksi teks sebelum terjemahan
        const { text: protectedText, placeholders } = createPlaceholderProtection(
            line, 
            protectedData.protected_phrases
        );

        // Terjemahkan teks yang sudah diproteksi
        let translated = await translateWithGoogle(protectedText, translateCode);

        // Restore placeholder ke teks asli
        translated = restorePlaceholders(translated, placeholders);

        // Perbaikan formatting setelah terjemahan
        translated = fixPostTranslationFormatting(translated, rawLine);

        translatedLines.push(translated);
    }

    let translatedBody = translatedLines.join("\n");
    
    // Final cleanup dan perbaikan
    translatedBody = applyPostTranslationFixes(translatedBody, langCode);

    // Pastikan link LICENSE tetap konsisten
    // PERBAIKAN: Gunakan hanya 1 baris kosong setelah header
    let finalText = `${finalHeader}\n\n---\n${translatedBody}`;
    finalText = finalText.replace(/\(LICENSE\)/g, "(../../LICENSE)");

    // Gunakan finalCleanup yang baru dengan perbaikan spacing
    finalText = finalCleanup(finalText);

    // PERBAIKAN: Pastikan tidak ada baris kosong berlebih di akhir file
    finalText = finalText.replace(/\n+$/, '\n');

    try {
        fs.mkdirSync(outDir, { recursive: true });
        fs.writeFileSync(destPath, finalText, "utf-8");

        // 進捗完了を表示
        if (progressOutput) {
            progressOutput.appendLine(l10n.t('progress.fileCreated', destPath));
        }

        // Setelah berhasil translate README, handle CHANGELOG
        if (hasChangelogFile(workspace) && hasChangelogSectionInReadme(workspace)) {
            // Terjemahkan CHANGELOG
            await translateChangelog(langCode, langInfo, protectedData, workspace);
            
            // Update link CHANGELOG di README yang sudah diterjemahkan
            await updateChangelogLinksInReadme(langCode, langInfo, workspace);
        }
    } catch (error) {
        Logger.error(`Failed to write translated README for ${langCode}`, error);
        throw error;
    }
}