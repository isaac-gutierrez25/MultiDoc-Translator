// l10n.ts
import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

// Logger untuk l10n
class L10nLogger {
    static log(message: string): void {
        console.log(`[MultiDoc-L10n] ${message}`);
    }
    
    static error(message: string, error?: any): void {
        console.error(`[MultiDoc-L10n] ERROR: ${message}`, error);
    }
}

// 🌍 Supported Languages dengan kode yang sesuai untuk l10n
export const LANGUAGES: Record<string, [string, string, string]> = {
    "en": ["English", "en", "🌐 Available in other languages:"],
    "id": ["Bahasa Indonesia", "id", "🌐 Tersedia dalam bahasa lain:"],
    "fr": ["Français", "fr", "🌐 Disponible dans d'autres langues :"],
    "de": ["Deutsch", "de", "🌐 In anderen Sprachen verfügbar:"],
    "jp": ["日本語", "ja", "🌐 他の言語でも利用可能:"],
    "zh": ["简体中文", "zh-CN", "🌐 提供其他语言版本："],
    "es": ["Español", "es", "🌐 Disponible en otros idiomas:"],
    "pl": ["Polski", "pl", "🌐 Dostępne w innych językach:"],
    "ru": ["Русский", "ru", "🌐 Доступно на других языках:"],
    "pt": ["Português", "pt", "🌐 Disponível em outros idiomas:"],
    "ko": ["한국어", "ko", "🌐 다른 언어로도 사용 가능:"],
    "kr": ["한국어", "ko", "🌐 다른 언어로도 사용 가능:"],  // Alias for backward compatibility
};

// Interface untuk bundle l10n
interface L10nBundle {
    [key: string]: string;
}

// Fallback translations jika bundle tidak ditemukan - DITAMBAH KEYS BARU
const FALLBACK_TRANSLATIONS: L10nBundle = {
    "extension.title": "🌍 MultiDoc Translator",
    "progress.translatingTo": "📘 [{2}] Translating to {0} ({1})",
    "extension.description": "Select languages to translate or remove:",
    "progress.title": "📊 Translation Progress",
    "progress.show": "📈 Show Progress Output",
    "progress.description": "View detailed translation logs and progress",
    "progress.startingTranslation": "🚀 Starting translation for {0} languages...",
    "progress.translating": "🌍 Translating READMEs",
    
    // ✅ KEYS BARU YANG DITAMBAHKAN:
    "progress.translatingLanguage": "📘 Translating {0} ({1}) ...",
    "progress.lineProgress": "   ↳ Progress: {0}/{1} lines ({2}%)",
    "progress.fileCreated": "✅ {0} successfully created",
    "progress.waiting": "   ⏳ Waiting {0}s...",
    
    "progress.completed": "🎉 Translation completed successfully!",
    "progress.filesSaved": "📁 Files saved in: {0}",
    "progress.removingSelected": "🗑️ Removing {0} selected languages...",
    "progress.removingAll": "🗑️ Removing ALL translation files...",
    "changelog.title": "📋 Changelog Management",
    "changelog.features": "CHANGELOG.md Features:",
    "changelog.featureList": "• Auto-detect CHANGELOG.md file<br>• Add changelog section to README<br>• Translate changelog to all languages<br>• Update links in translated READMEs<br>• <strong>Auto-detect GitHub URL</strong> from package.json",
    "changelog.autoSetup": "🔧 Auto Setup Changelog",
    "changelog.translateOnly": "🌐 Translate Changelog Only",
    "changelog.detectGitHub": "🔍 Detect GitHub URL",
    "changelog.githubDetection": "GitHub URL Auto-detection:",
    "changelog.githubSources": "• Reads from package.json (repository field)<br>• Falls back to .git/config<br>• Auto-generates Releases page link",
    "changelog.autoSettingUp": "🔧 Auto-setting up changelog section in README...",
    "changelog.checkingSpacing": "🔧 Checking changelog section spacing...",
    "changelog.translatingChangelog": "🌐 Translating CHANGELOG to {0} languages...",
    "changelog.selectLanguages": "Select which languages to translate CHANGELOG to",
    "changelog.translateAll": "Translate CHANGELOG to all supported languages",
    "changelog.translateSelected": "Translate CHANGELOG to {0} selected languages",
    "protection.title": "🛡️ Phrase Protection Settings",
    "protection.status": "Protection Status",
    "protection.active": "ACTIVE ✅",
    "protection.inactive": "INACTIVE ❌",
    "protection.enable": "🟢 Enable Protection",
    "protection.disable": "🔴 Disable Protection",
    "protection.statusDetails": "🔍 Status Details",
    "protection.managePhrases": "Manage Protection Phrases:",
    "protection.add": "➕ Add",
    "protection.remove": "➖ Remove",
    "protection.list": "📜 List",
    "protection.reset": "🔁 Reset",
    "protection.enterPhrase": "Enter phrase or regex to protect:",
    "protection.phraseExample": "Example: MIT License or MIT\\s+License for regex",
    "protection.selectPhraseToRemove": "Select phrase to remove from protection",
    "protection.phraseList": "📜 Protection Phrases List:",
    "protection.statusDetailsFull": "Protection Status: {0}\nTotal Phrases: {1}",
    "languages.title": "Available Languages",
    "languages.selectAll": "Select All Languages",
    "languages.selectedCount": "{0} of {1} languages selected",
    "languages.all": "All Languages",
    "languages.selected": "Selected Languages",
    "actions.generate": "⚙️ Generate Multilingual READMEs",
    "actions.removeSelected": "🗑️ Remove Selected",
    "actions.removeAll": "🗑️ Remove All",
    "actions.yesRemove": "Yes, Remove",
    "actions.yesRemoveAll": "Yes, Remove All",
    "actions.yesReset": "Yes, Reset",
    "actions.cancel": "Cancel",
    "errors.noLanguagesSelected": "❌ Select at least one language to translate.",
    "errors.noWorkspace": "❌ No workspace open.",
    "errors.translationFailed": "❌ Failed to translate {0}: {1}",
    "errors.translationFailedShort": "❌ Failed to translate {0}",
    "errors.translationFailedGeneral": "❌ Translation failed: {0}",
    "errors.translationFailedCheckOutput": "❌ Translation failed. Check output for details.",
    "errors.noLanguagesSelectedRemove": "❌ Select at least one language to remove.",
    "errors.noChangelogFile": "❌ You don't have CHANGELOG.md file in root directory",
    "errors.changelogSetupFailed": "❌ Changelog setup failed",
    "errors.changelogTranslationFailed": "❌ Failed to translate CHANGELOG",
    "errors.githubUrlNotDetected": "❌ Could not detect GitHub repository URL automatically.\n\nPlease check:\n• package.json has 'repository' field\n• .git/config has remote URL\n• Or add GitHub URL manually to README",
    "confirmation.removeSelected": "Are you sure you want to remove {0} selected languages?",
    "confirmation.removeAll": "Are you sure you want to remove ALL translation files?",
    "confirmation.resetPhrases": "Are you sure you want to reset protection phrases to default?",
    "changelog.translating": "📘 Translating CHANGELOG for {0}...",
    "changelog.translated": "✅ CHANGELOG successfully translated for {0}",
    "success.translationCompleted": "✅ {0} READMEs successfully translated! Check \"Translation Progress\" output for details.",
    "success.removalCompleted": "✅ Removal completed successfully!",
    "success.removedLanguages": "📋 Removed languages: {0}",
    "success.languagesRemoved": "🗑️ {0} languages successfully removed: {1}",
    "success.allRemoved": "✅ All translation files successfully removed!",
    "success.totalRemoved": "📋 Total removed: {0} languages",
    "success.allTranslationFilesRemoved": "🗑️ All translation files successfully removed ({0} languages)",
    "success.phraseAdded": "✅ Phrase '{0}' added to protection.",
    "success.phraseRemoved": "🗑️ Phrase '{0}' removed from protection.",
    "success.phrasesReset": "🔁 Protection phrases reset to default.",
    "success.protectionEnabled": "🟢 Phrase protection enabled.",
    "success.protectionDisabled": "🔴 Phrase protection disabled.",
    "success.changelogSetupCompleted": "✅ Changelog setup completed",
    "success.changelogSectionAdded": "✅ Changelog section added to README.md",
    "success.changelogTranslationCompleted": "🎉 CHANGELOG translation completed!",
    "success.changelogTranslated": "✅ CHANGELOG translated to {0} languages",
    "success.githubUrlDetected": "✅ GitHub URL detected: {0}\nReleases: {1}",
    "info.noFilesDeleted": "ℹ️ No files were successfully deleted.",
    "info.noTranslationFiles": "ℹ️ No translation files found.",
    "info.phraseExists": "ℹ️ Phrase '{0}' already exists in protection list.",
    "info.noPhrasesToRemove": "ℹ️ No protection phrases available to remove.",
    "info.noPhrasesRegistered": "ℹ️ No protection phrases registered.",
    "info.phraseListShown": "📜 Protection phrases list shown in Output Channel.",
    "github.detectionResults": "🔍 GitHub Repository Detection Results:",
    "github.repositoryUrl": "📦 Repository URL: {0}",
    "github.releasesUrl": "🚀 Releases URL: {0}",
    "github.sourcesChecked": "📋 Sources checked:",
    "github.sourcePackageJson": "• package.json (repository field)",
    "github.sourceGitConfig": "• .git/config",
    "github.sourceReadme": "• README.md (GitHub URL patterns)"
};

export class L10nManager {
    private bundles: Map<string, L10nBundle> = new Map();
    private currentLanguage: string = 'en';
    private extensionPath: string;

    constructor(extensionPath: string) {
        this.extensionPath = extensionPath;
        this.loadBundles();
        this.initializeLanguage();
    }

    // Inisialisasi bahasa berdasarkan setting VS Code
    private initializeLanguage(): void {
        try {
            const vscodeLanguage = vscode.env.language;
            L10nLogger.log(`VS Code language: ${vscodeLanguage}`);
            
            // Normalize language code
            const normalizedLang = this.normalizeLanguageCode(vscodeLanguage);
            L10nLogger.log(`Normalized language: ${normalizedLang}`);
            
            this.setLanguage(normalizedLang);
        } catch (error) {
            L10nLogger.error('Error initializing language', error);
            this.currentLanguage = 'en';
        }
    }

    // Normalize VS Code language code to match our bundle codes
    private normalizeLanguageCode(langCode: string): string {
        const langMap: Record<string, string> = {
            'de': 'de',
            'es': 'es',
            'fr': 'fr',
            'id': 'id',
            'ja': 'jp',      // Changed from 'ja' to 'jp'
            'jp': 'jp',      // Added new mapping
            'ko': 'kr',      // Changed from 'ko' to 'kr'
            'kr': 'kr',      // Added new mapping
            'pl': 'pl',
            'pt': 'pt',
            'pt-br': 'pt',
            'ru': 'ru',
            'zh-cn': 'zh',   // Changed from 'zh-CN' to 'zh'
            'zh-tw': 'zh',   // Changed from 'zh-CN' to 'zh'
            'zh': 'zh'       // Changed from 'zh-CN' to 'zh'
        };

        const baseLang = langCode.toLowerCase().split('-')[0];
        return langMap[baseLang] || langMap[langCode.toLowerCase()] || 'en';
    }

    // Memuat semua bundle l10n
    private loadBundles(): void {
        try {
            const l10nPath = path.join(this.extensionPath, 'l10n');
            
            if (!fs.existsSync(l10nPath)) {
                L10nLogger.log('l10n directory not found, using fallback translations');
                this.bundles.set('en', FALLBACK_TRANSLATIONS);
                return;
            }

            const files = fs.readdirSync(l10nPath);
            let loadedCount = 0;
            
            for (const file of files) {
                try {
                    // Pattern: bundle.l10n.[lang].json
                    if (file.startsWith('bundle.l10n.') && file.endsWith('.json')) {
                        const langCode = file.replace('bundle.l10n.', '').replace('.json', '');
                        const filePath = path.join(l10nPath, file);
                        const content = fs.readFileSync(filePath, 'utf-8');
                        const bundle: L10nBundle = JSON.parse(content);
                        this.bundles.set(langCode, bundle);
                        loadedCount++;
                        L10nLogger.log(`Loaded l10n bundle for ${langCode}`);
                    }
                } catch (fileError) {
                    L10nLogger.error(`Error loading bundle ${file}`, fileError);
                }
            }

            // Always ensure English bundle exists as fallback
            if (!this.bundles.has('en')) {
                this.bundles.set('en', FALLBACK_TRANSLATIONS);
                L10nLogger.log('English fallback bundle loaded');
            }

            if (loadedCount === 0) {
                L10nLogger.log('No l10n bundles found, using fallback translations only');
            } else {
                L10nLogger.log(`Successfully loaded ${loadedCount} l10n bundles`);
            }

        } catch (error) {
            L10nLogger.error('Error loading l10n bundles', error);
            // Ensure we always have English fallback
            this.bundles.set('en', FALLBACK_TRANSLATIONS);
        }
    }

    // Mengatur bahasa saat ini
    public setLanguage(langCode: string): void {
        const normalizedLang = this.normalizeLanguageCode(langCode);
        
        if (this.bundles.has(normalizedLang)) {
            this.currentLanguage = normalizedLang;
            L10nLogger.log(`Language set to: ${this.currentLanguage}`);
        } else {
            L10nLogger.log(`Language ${langCode} (normalized: ${normalizedLang}) not found, falling back to English`);
            this.currentLanguage = 'en';
        }
    }

    // Mendapatkan string yang dilokalisasi
    public t(key: string, ...args: any[]): string {
        try {
            let bundle = this.bundles.get(this.currentLanguage);
            
            // Fallback ke English jika tidak ditemukan di bahasa saat ini
            if (!bundle) {
                bundle = this.bundles.get('en');
            }

            // Fallback ke FALLBACK_TRANSLATIONS jika masih tidak ditemukan
            let text = bundle?.[key] || FALLBACK_TRANSLATIONS[key] || key;

            // Replace placeholder dengan args
            if (args.length > 0) {
                for (let i = 0; i < args.length; i++) {
                    const placeholder = `{${i}}`;
                    if (text.includes(placeholder)) {
                        text = text.replace(new RegExp(this.escapeRegExp(placeholder), 'g'), String(args[i]));
                    }
                }
            }

            return text;

        } catch (error) {
            L10nLogger.error(`Translation error for key "${key}"`, error);
            return key;
        }
    }

    // Helper untuk escape regex characters
    private escapeRegExp(string: string): string {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Mendapatkan bahasa yang tersedia
    public getAvailableLanguages(): string[] {
        return Array.from(this.bundles.keys());
    }

    // Mendapatkan info bahasa
    public getLanguageInfo(langCode: string): [string, string, string] | undefined {
        return LANGUAGES[langCode];
    }

    // Mendapatkan semua bahasa yang didukung
    public getAllSupportedLanguages(): typeof LANGUAGES {
        return LANGUAGES;
    }

    // Mendapatkan bahasa saat ini
    public getCurrentLanguage(): string {
        return this.currentLanguage;
    }
}

// Export singleton instance
let l10nManager: L10nManager;

export function initL10n(extensionPath: string): L10nManager {
    L10nLogger.log('Initializing L10nManager...');
    l10nManager = new L10nManager(extensionPath);
    L10nLogger.log(`L10nManager initialized with language: ${l10nManager.getCurrentLanguage()}`);
    return l10nManager;
}

export function getL10n(): L10nManager {
    if (!l10nManager) {
        const errorMsg = 'L10nManager not initialized. Call initL10n first.';
        L10nLogger.error(errorMsg);
        throw new Error(errorMsg);
    }
    return l10nManager;
}