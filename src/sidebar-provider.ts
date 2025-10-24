import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { 
    translateReadme, 
    translateChangelogOnly, 
    updateLanguageSwitcher, 
    removeLanguageFiles, 
    removeAllLanguageFiles,
    hasChangelogFile,
    hasChangelogSectionInReadme,
    addChangelogSectionToReadme,
    fixExistingChangelogSpacing,
    getGitHubRepoUrl,
    getGitHubReleasesUrl,
    loadProtectedPhrases,
    saveProtectedPhrases,
    isProtectEnabled,
    setProtectStatus,
    DEFAULT_PROTECTED_PHRASES,
    Logger,
    ProtectedData
} from './translation-core';
import { getL10n, LANGUAGES } from './l10n';

export class TranslateSidebarProvider implements vscode.WebviewViewProvider {
    public readonly output: vscode.OutputChannel;
    public readonly progressOutput: vscode.OutputChannel;
    private _view?: vscode.WebviewView;
    private selectedLanguages: Set<string> = new Set(Object.keys(LANGUAGES));
    private protectEnabled: boolean = false;
    private protectedPhrases: string[] = [...DEFAULT_PROTECTED_PHRASES];
    private l10n: ReturnType<typeof getL10n>;

    constructor(
        private readonly _uri: vscode.Uri,
        private readonly _context: vscode.ExtensionContext
    ) {
        this.output = vscode.window.createOutputChannel("MultiDoc Translator");
        this.progressOutput = vscode.window.createOutputChannel("Translation Progress");
        this.l10n = getL10n();
        this.loadProtectionStatus();
    }

    resolveWebviewView(view: vscode.WebviewView) {
        this._view = view;
        view.webview.options = { enableScripts: true };
        this.loadProtectionStatus();
        view.webview.html = this.getWebviewContent();
        
        view.webview.onDidReceiveMessage(async (msg) => {
            try {
                switch (msg.command) {
                    case 'run':
                        await this.generateReadmes();
                        break;
                    case 'toggleAll':
                        this.toggleAllLanguages(msg.checked);
                        break;
                    case 'toggleLanguage':
                        this.toggleLanguage(msg.language, msg.checked);
                        break;
                    case 'toggleAll':
                        this.toggleAllLanguages(msg.checked);
                        break;
                    case 'removeSelected':
                        await this.removeSelectedLanguages();
                        break;
                    case 'removeAll':
                        await this.removeAllLanguages();
                        break;
                    case 'addProtect':
                        await this.addProtectPhrase();
                        break;
                    case 'removeProtect':
                        await this.removeProtectPhrase();
                        break;
                    case 'listProtect':
                        await this.listProtectPhrases();
                        break;
                    case 'initProtect':
                        await this.initProtectPhrases();
                        break;
                    case 'enableProtect':
                        await this.setProtectStatus(true);
                        break;
                    case 'disableProtect':
                        await this.setProtectStatus(false);
                        break;
                    case 'statusProtect':
                        await this.showProtectStatus();
                        break;
                    case 'showProgress':
                        this.showProgressOutput();
                        break;
                    case 'autoSetupChangelog':
                        await this.autoSetupChangelog();
                        break;
                    case 'translateChangelog':
                        await this.translateChangelog();
                        break;
                    case 'detectGitHubUrl':
                        await this.detectGitHubUrl();
                        break;
                }
            } catch (error) {
                Logger.error('Error handling webview message', error);
                vscode.window.showErrorMessage(this.l10n.t('errors.translationFailedCheckOutput'));
            }
        });
    }

    private loadProtectionStatus() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (workspace) {
            this.protectEnabled = isProtectEnabled(workspace);
            const protectedData = loadProtectedPhrases(workspace);
            this.protectedPhrases = protectedData.protected_phrases;
        }
    }

    private getWebviewContent(): string {
        const t = this.l10n.t.bind(this.l10n);
        
        const languageCheckboxes = Object.entries(LANGUAGES as Record<string, [string, string, string]>)
            .filter(([code]) => code !== 'en')
            .map(([code, [name]]) => {
                const checked = this.selectedLanguages.has(code) ? 'checked' : '';
                return `
                <div class="language-item">
                    <label>
                        <input type="checkbox" id="lang-${code}" value="${code}" ${checked} 
                               onchange="toggleLanguage('${code}', this.checked)"
                               class="language-checkbox">
                        ${name}
                    </label>
                </div>
                `;
            })
            .join('');

        const availableLanguages = Object.keys(LANGUAGES).filter(code => code !== 'en').length;
        const allChecked = this.selectedLanguages.size === availableLanguages ? 'checked' : '';
        const someChecked = this.selectedLanguages.size > 0 && this.selectedLanguages.size < availableLanguages;

        const protectStatusText = this.protectEnabled ? t('protection.active') : t('protection.inactive');
        const protectButtonText = this.protectEnabled ? t('protection.disable') : t('protection.enable');
        const protectButtonCommand = this.protectEnabled ? 'disableProtect' : 'enableProtect';

        return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-family: var(--vscode-font-family);
                    font-size: var(--vscode-font-size);
                    color: var(--vscode-foreground);
                    background: var(--vscode-editor-background);
                    padding: 12px;
                    margin: 0;
                }
                .header {
                    margin-bottom: 20px;
                }
                .header h3 {
                    margin: 0 0 8px 0;
                    color: var(--vscode-titleBar-activeForeground);
                    font-size: 14px;
                }
                .header p {
                    margin: 0;
                    color: var(--vscode-descriptionForeground);
                    font-size: 12px;
                    line-height: 1.4;
                }
                .section {
                    margin-bottom: 20px;
                    border: 1px solid var(--vscode-panel-border);
                    border-radius: 6px;
                    padding: 16px;
                    background: var(--vscode-input-background);
                }
                .section-title {
                    font-weight: bold;
                    margin-bottom: 12px;
                    color: var(--vscode-foreground);
                    font-size: 13px;
                }
                .language-list {
                    max-height: 200px;
                    overflow-y: auto;
                    border: 1px solid var(--vscode-panel-border);
                    border-radius: 4px;
                    padding: 12px;
                    background: var(--vscode-input-background);
                    margin-bottom: 8px;
                }
                .language-item {
                    margin: 6px 0;
                    padding: 4px 0;
                }
                .language-item label {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                    font-size: 13px;
                    line-height: 1.4;
                }
                .language-item input[type="checkbox"] {
                    margin-right: 10px;
                    transform: scale(1.1);
                }
                .select-all {
                    margin-bottom: 12px;
                    padding: 6px 0;
                    border-bottom: 1px solid var(--vscode-panel-border);
                }
                .select-all label {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                    font-weight: bold;
                    font-size: 13px;
                    line-height: 1.4;
                }
                .select-all input[type="checkbox"] {
                    margin-right: 10px;
                    transform: scale(1.1);
                }
                .button {
                    width: 100%;
                    padding: 10px 12px;
                    background: var(--vscode-button-background);
                    color: var(--vscode-button-foreground);
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 13px;
                    margin-top: 8px;
                    font-weight: 500;
                    transition: background 0.2s;
                }
                .button:hover {
                    background: var(--vscode-button-hoverBackground);
                }
                .button:disabled {
                    background: var(--vscode-button-secondaryBackground);
                    color: var(--vscode-button-secondaryForeground);
                    cursor: not-allowed;
                    opacity: 0.6;
                }
                .button.remove {
                    background: var(--vscode-inputValidation-errorBackground);
                    color: var(--vscode-inputValidation-errorForeground);
                }
                .button.remove:hover {
                    background: var(--vscode-inputValidation-errorBorder);
                }
                .button.protect {
                    background: var(--vscode-inputOption-activeBackground);
                    color: var(--vscode-inputOption-activeForeground);
                    border: 1px solid var(--vscode-inputOption-activeBorder);
                }
                .button.protect:hover {
                    background: var(--vscode-inputOption-activeBorder);
                }
                .stats {
                    margin-top: 12px;
                    font-size: 11px;
                    color: var(--vscode-descriptionForeground);
                    text-align: center;
                    padding: 4px;
                    background: var(--vscode-badge-background);
                    border-radius: 3px;
                }
                .indeterminate {
                    opacity: 0.7;
                }
                .button-group {
                    display: flex;
                    gap: 10px;
                    margin-top: 16px;
                }
                .button-group .button {
                    flex: 1;
                    margin-top: 0;
                }
                .protect-status {
                    padding: 12px;
                    background: var(--vscode-input-background);
                    border-radius: 4px;
                    margin-bottom: 16px;
                    font-size: 12px;
                    text-align: center;
                    border: 1px solid var(--vscode-panel-border);
                    font-weight: 500;
                }
                .protect-status.active {
                    background: var(--vscode-testing-iconPassed);
                    color: var(--vscode-input-foreground);
                    border-color: var(--vscode-testing-iconPassed);
                }
                .protect-status.inactive {
                    background: var(--vscode-inputValidation-errorBackground);
                    color: var(--vscode-inputValidation-errorForeground);
                    border-color: var(--vscode-inputValidation-errorBorder);
                }
                .small-button {
                    padding: 8px 12px;
                    font-size: 12px;
                    margin: 4px 0;
                    font-weight: 500;
                }
                .protect-buttons-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                    margin: 12px 0;
                }
                .protect-buttons-grid .button {
                    margin: 0;
                }
                .spacer {
                    height: 8px;
                }
                .divider {
                    height: 1px;
                    background: var(--vscode-panel-border);
                    margin: 16px 0;
                    opacity: 0.5;
                }
                .compact-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 8px;
                    margin: 8px 0;
                }
                .compact-grid .button {
                    margin: 0;
                    padding: 6px 8px;
                    font-size: 11px;
                }
                .changelog-section {
                    background: var(--vscode-textBlockQuote-background);
                    border-left: 4px solid var(--vscode-textBlockQuote-border);
                    padding: 12px;
                    margin: 12px 0;
                    border-radius: 4px;
                }
                .info-box {
                    background: var(--vscode-textCodeBlock-background);
                    border: 1px solid var(--vscode-panel-border);
                    border-radius: 4px;
                    padding: 10px;
                    margin: 8px 0;
                    font-size: 11px;
                    line-height: 1.4;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h3>${t('extension.title')}</h3>
                <p>${t('extension.description')}</p>
            </div>

            <!-- PROGRESS SECTION -->
            <div class="section">
                <div class="section-title">${t('progress.title')}</div>
                <button class="button" onclick="vscodePostMessage('showProgress')">
                    ${t('progress.show')}
                </button>
                <div style="font-size: 11px; color: var(--vscode-descriptionForeground); margin-top: 8px;">
                    ${t('progress.description')}
                </div>
            </div>

            <!-- CHANGELOG SECTION -->
            <div class="section">
                <div class="section-title">${t('changelog.title')}</div>
                <div class="changelog-section">
                    <div style="font-size: 12px; margin-bottom: 8px;">
                        <strong>${t('changelog.features')}</strong>
                    </div>
                    <div style="font-size: 11px; color: var(--vscode-descriptionForeground); line-height: 1.4;">
                        ${t('changelog.featureList')}
                    </div>
                </div>
                
                <button class="button small-button" onclick="vscodePostMessage('autoSetupChangelog')">
                    ${t('changelog.autoSetup')}
                </button>
                <button class="button small-button" onclick="vscodePostMessage('translateChangelog')">
                    ${t('changelog.translateOnly')}
                </button>
                <button class="button small-button" onclick="vscodePostMessage('detectGitHubUrl')">
                    ${t('changelog.detectGitHub')}
                </button>
                
                <div class="info-box">
                    <strong>${t('changelog.githubDetection')}</strong><br>
                    ${t('changelog.githubSources')}
                </div>
            </div>

            <!-- PROTECTION SETTINGS BOX -->
            <div class="section">
                <div class="section-title">${t('protection.title')}</div>
                
                <div class="protect-status ${this.protectEnabled ? 'active' : 'inactive'}">
                    ${t('protection.status')}: <strong>${protectStatusText}</strong>
                </div>
                
                <div class="protect-buttons-grid">
                    <button class="button protect small-button" onclick="vscodePostMessage('${protectButtonCommand}')">
                        ${protectButtonText}
                    </button>
                    <button class="button protect small-button" onclick="vscodePostMessage('statusProtect')">
                        ${t('protection.statusDetails')}
                    </button>
                </div>

                <div class="divider"></div>

                <div class="section-title" style="font-size: 12px; margin-bottom: 8px;">${t('protection.managePhrases')}:</div>
                
                <div class="compact-grid">
                    <button class="button protect" onclick="vscodePostMessage('addProtect')">
                        ${t('protection.add')}
                    </button>
                    <button class="button protect" onclick="vscodePostMessage('removeProtect')">
                        ${t('protection.remove')}
                    </button>
                    <button class="button protect" onclick="vscodePostMessage('listProtect')">
                        ${t('protection.list')}
                    </button>
                    <button class="button protect" onclick="vscodePostMessage('initProtect')">
                        ${t('protection.reset')}
                    </button>
                </div>
            </div>

            <!-- LANGUAGES BOX -->
            <div class="section">
                <div class="section-title">${t('languages.title')}</div>
                <div class="select-all">
                    <label class="${someChecked ? 'indeterminate' : ''}">
                        <input type="checkbox" id="selectAll" ${allChecked} 
                               onchange="toggleAllLanguages(this.checked)">
                        ${t('languages.selectAll')}
                    </label>
                </div>
                <div class="language-list">
                    ${languageCheckboxes}
                </div>
                <div class="stats">
                    ${t('languages.selectedCount', this.selectedLanguages.size.toString(), availableLanguages.toString())}
                </div>
            </div>

            <button class="button" id="runBtn" ${this.selectedLanguages.size === 0 ? 'disabled' : ''} onclick="vscodePostMessage('run')">
                ${t('actions.generate')}
            </button>

            <div class="button-group">
                <button class="button remove" id="removeSelectedBtn" ${this.selectedLanguages.size === 0 ? 'disabled' : ''} onclick="vscodePostMessage('removeSelected')">
                    ${t('actions.removeSelected')}
                </button>
                <button class="button remove" id="removeAllBtn" onclick="vscodePostMessage('removeAll')">
                    ${t('actions.removeAll')}
                </button>
            </div>

            <script>
                const vscode = acquireVsCodeApi();
                
                function vscodePostMessage(command) {
                    vscode.postMessage({ command: command });
                }
                
                function toggleLanguage(language, checked) {
                    vscode.postMessage({
                        command: 'toggleLanguage',
                        language: language,
                        checked: checked
                    });
                }
                
                function toggleAllLanguages(checked) {
                    // Update all language checkboxes
                    document.querySelectorAll('.language-checkbox').forEach(checkbox => {
                        checkbox.checked = checked;
                    });

                    // Get all selected language values
                    const selectedLanguages = Array.from(document.querySelectorAll('.language-checkbox:checked')).map(cb => cb.value);

                    // Notify the extension
                    vscode.postMessage({
                        command: 'toggleAll',
                        checked: checked
                    });
                }

                // Update UI when selection changes
                window.addEventListener('message', event => {
                    const message = event.data;
                    if (message.command === 'updateSelection') {
                        // Update checkboxes
                        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                            if (checkbox.id === 'selectAll') {
                                // Get total number of language checkboxes
                                const totalLanguages = document.querySelectorAll('.language-checkbox').length;
                                checkbox.checked = message.selectedLanguages.length === totalLanguages;
                                checkbox.indeterminate = message.selectedLanguages.length > 0 && message.selectedLanguages.length < totalLanguages;
                            } else {
                                checkbox.checked = message.selectedLanguages.includes(checkbox.value);
                            }
                        });

                        // Update button states
                        const runBtn = document.getElementById('runBtn');
                        const removeSelectedBtn = document.getElementById('removeSelectedBtn');
                        if (runBtn) {
                            runBtn.disabled = message.selectedLanguages.length === 0;
                        }
                        if (removeSelectedBtn) {
                            removeSelectedBtn.disabled = message.selectedLanguages.length === 0;
                        }
                    }
                });
            </script>
        </body>
        </html>
        `;
    }

    private toggleLanguage(language: string, checked: boolean) {
        if (checked) {
            this.selectedLanguages.add(language);
        } else {
            this.selectedLanguages.delete(language);
        }
        this.updateWebview();
    }

    private toggleAllLanguages(checked: boolean) {
        // Get all available languages except English
        const availableLanguages = Object.keys(LANGUAGES).filter(code => code !== 'en');
        
        if (checked) {
            this.selectedLanguages = new Set(availableLanguages);
        } else {
            this.selectedLanguages.clear();
        }
        
        this.updateWebview();
    }

    private updateWebview() {
        if (this._view) {
            this._view.webview.postMessage({
                command: 'updateSelection',
                selectedLanguages: Array.from(this.selectedLanguages)
            });
        }
    }

    async generateReadmes() {
        if (this.selectedLanguages.size === 0) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noLanguagesSelected'));
            return;
        }

        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        // Auto setup changelog jika file CHANGELOG ada tapi section belum ada di README
        if (hasChangelogFile(workspace) && !hasChangelogSectionInReadme(workspace)) {
            this.progressOutput.show();
            this.progressOutput.appendLine(this.l10n.t('changelog.autoSettingUp'));
            addChangelogSectionToReadme(workspace);
        } else if (hasChangelogSectionInReadme(workspace)) {
            // Perbaiki spacing untuk section yang sudah ada
            this.progressOutput.appendLine(this.l10n.t('changelog.checkingSpacing'));
            fixExistingChangelogSpacing(workspace);
        }

        const protectedData = loadProtectedPhrases(workspace);

        // Show progress output channel
        this.progressOutput.show();
        this.progressOutput.clear();
        
        const timestamp = new Date().toLocaleTimeString();
        // Count languages excluding English
        const languageCount = Array.from(this.selectedLanguages).filter(code => code !== 'en').length;
        this.progressOutput.appendLine(this.l10n.t('progress.startingTranslation', languageCount.toString()));
        this.progressOutput.appendLine("");

        try {
            // Show progress bar
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: this.l10n.t('progress.translating'),
                cancellable: false
            }, async (progress) => {
                const languages = Array.from(this.selectedLanguages);
                const total = languages.length;
                
                for (let i = 0; i < languages.length; i++) {
                    const code = languages[i];
                    if (code in LANGUAGES) {
                        const langName = LANGUAGES[code][0];
                        
                        // Update progress bar
                        progress.report({
                            message: this.l10n.t('progress.translatingLanguage', langName, (i + 1).toString(), total.toString()),
                            increment: (100 / total)
                        });

                        // Tampilkan progress di output channel
                        this.progressOutput.appendLine(this.l10n.t('progress.translatingLanguage', langName, (i + 1).toString(), total.toString()));

                        try {
                            // Translate README first
                            await translateReadme(code, LANGUAGES[code], protectedData, workspace, this.progressOutput);
                            
                            // If CHANGELOG exists, translate it too and show progress
                            if (hasChangelogFile(workspace)) {
                                this.progressOutput.appendLine("");
                                this.progressOutput.appendLine(this.l10n.t('changelog.translating', langName));
                                await translateChangelogOnly([code], workspace, this.progressOutput);
                                this.progressOutput.appendLine(this.l10n.t('progress.changelogTranslated', langName));
                            }
                            
                            // Delay untuk menghindari rate limiting dengan progress
                            await new Promise(resolve => {
                                let countdown = 3;
                                const interval = setInterval(() => {
                                    if (countdown > 0) {
                                        this.progressOutput.appendLine(this.l10n.t('progress.waiting', countdown.toString()));
                                        countdown--;
                                    } else {
                                        clearInterval(interval);
                                        resolve(null);
                                    }
                                }, 1000);
                            });
                            
                        } catch (error) {
                            const errorMsg = this.l10n.t('errors.translationFailed', code, error instanceof Error ? error.message : String(error));
                            Logger.error(errorMsg);
                            this.progressOutput.appendLine(errorMsg);
                            vscode.window.showErrorMessage(this.l10n.t('errors.translationFailedShort', LANGUAGES[code][0]));
                        }
                    }
                }
            });

            // Update language switcher untuk SEMUA bahasa yang sudah ada (termasuk yang baru)
            updateLanguageSwitcher(workspace, Array.from(this.selectedLanguages));

            // Tampilkan summary
            this.progressOutput.appendLine("");
            this.progressOutput.appendLine(this.l10n.t('progress.completed'));
            this.progressOutput.appendLine(this.l10n.t('progress.filesSaved', path.join(workspace, 'docs/lang')));

            vscode.window.showInformationMessage(
                this.l10n.t('success.translationCompleted', this.selectedLanguages.size.toString())
            );

        } catch (error) {
            const errorMsg = this.l10n.t('errors.translationFailedGeneral', error instanceof Error ? error.message : String(error));
            this.progressOutput.appendLine(errorMsg);
            vscode.window.showErrorMessage(this.l10n.t('errors.translationFailedCheckOutput'));
        }
    }

    async removeSelectedLanguages() {
        if (this.selectedLanguages.size === 0) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noLanguagesSelectedRemove'));
            return;
        }

        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const result = await vscode.window.showWarningMessage(
            this.l10n.t('confirmation.removeSelected', this.selectedLanguages.size.toString()),
            { modal: true },
            this.l10n.t('actions.yesRemove'),
            this.l10n.t('actions.cancel')
        );

        if (result !== this.l10n.t('actions.yesRemove')) {
            return;
        }

        // Show progress output
        this.progressOutput.show();
        this.progressOutput.clear();
        
        const timestamp = new Date().toLocaleTimeString();
        this.progressOutput.appendLine(this.l10n.t('progress.removingSelected', this.selectedLanguages.size.toString()));
        this.progressOutput.appendLine("");

        const langCodes = Array.from(this.selectedLanguages);
        const removedLangs = removeLanguageFiles(langCodes, workspace);

        if (removedLangs.length > 0) {
            // Update language switcher di SEMUA file setelah menghapus
            updateLanguageSwitcher(workspace, undefined, removedLangs);
            
            // Show success message in output
            this.progressOutput.appendLine(this.l10n.t('success.removalCompleted'));
            this.progressOutput.appendLine(this.l10n.t('success.removedLanguages', removedLangs.map(code => LANGUAGES[code][0]).join(', ')));
            
            vscode.window.showInformationMessage(
                this.l10n.t('success.languagesRemoved', removedLangs.length.toString(), removedLangs.map(code => LANGUAGES[code][0]).join(', '))
            );
        } else {
            this.progressOutput.appendLine(this.l10n.t('info.noFilesDeleted'));
            vscode.window.showInformationMessage(this.l10n.t('info.noFilesDeleted'));
        }
    }

    async removeAllLanguages() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const result = await vscode.window.showWarningMessage(
            this.l10n.t('confirmation.removeAll'),
            { modal: true },
            this.l10n.t('actions.yesRemoveAll'),
            this.l10n.t('actions.cancel')
        );

        if (result !== this.l10n.t('actions.yesRemoveAll')) {
            return;
        }

        // Show progress output
        this.progressOutput.show();
        this.progressOutput.clear();
        
        const timestamp = new Date().toLocaleTimeString();
        this.progressOutput.appendLine(this.l10n.t('progress.removingAll'));
        this.progressOutput.appendLine("");

        const removedLangs = removeAllLanguageFiles(workspace);

        if (removedLangs.length > 0) {
            this.progressOutput.appendLine(this.l10n.t('success.allRemoved'));
            this.progressOutput.appendLine(this.l10n.t('success.totalRemoved', removedLangs.length.toString()));
            
            vscode.window.showInformationMessage(
                this.l10n.t('success.allTranslationFilesRemoved', removedLangs.length.toString())
            );
        } else {
            this.progressOutput.appendLine(this.l10n.t('info.noTranslationFiles'));
            vscode.window.showInformationMessage(this.l10n.t('info.noTranslationFiles'));
        }
    }

    async addProtectPhrase() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const phrase = await vscode.window.showInputBox({
            prompt: this.l10n.t('protection.enterPhrase'),
            placeHolder: this.l10n.t('protection.phraseExample')
        });

        if (phrase) {
            const protectedData = loadProtectedPhrases(workspace);
            
            if (!protectedData.protected_phrases.includes(phrase)) {
                protectedData.protected_phrases.push(phrase);
                saveProtectedPhrases(workspace, protectedData);
                this.protectedPhrases = protectedData.protected_phrases;
                vscode.window.showInformationMessage(this.l10n.t('success.phraseAdded', phrase));
            } else {
                vscode.window.showWarningMessage(this.l10n.t('info.phraseExists', phrase));
            }
        }
    }

    async removeProtectPhrase() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const protectedData = loadProtectedPhrases(workspace);
        
        if (protectedData.protected_phrases.length === 0) {
            vscode.window.showInformationMessage(this.l10n.t('info.noPhrasesToRemove'));
            return;
        }

        const phrase = await vscode.window.showQuickPick(protectedData.protected_phrases, {
            placeHolder: this.l10n.t('protection.selectPhraseToRemove')
        });

        if (phrase) {
            protectedData.protected_phrases = protectedData.protected_phrases.filter(p => p !== phrase);
            saveProtectedPhrases(workspace, protectedData);
            this.protectedPhrases = protectedData.protected_phrases;
            vscode.window.showInformationMessage(this.l10n.t('success.phraseRemoved', phrase));
        }
    }

    async listProtectPhrases() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const protectedData = loadProtectedPhrases(workspace);
        
        if (protectedData.protected_phrases.length === 0) {
            vscode.window.showInformationMessage(this.l10n.t('info.noPhrasesRegistered'));
            return;
        }

        const phrasesList = protectedData.protected_phrases.map((phrase, index) => 
            `${index + 1}. ${phrase}`
        ).join('\n');

        this.output.show();
        this.output.appendLine(this.l10n.t('protection.phraseList'));
        this.output.appendLine(phrasesList);
        this.output.appendLine("");

        vscode.window.showInformationMessage(this.l10n.t('info.phraseListShown'));
    }
    
    async initProtectPhrases() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const result = await vscode.window.showWarningMessage(
            this.l10n.t('confirmation.resetPhrases'),
            { modal: true },
            this.l10n.t('actions.yesReset'),
            this.l10n.t('actions.cancel')
        );

        if (result === this.l10n.t('actions.yesReset')) {
            const defaultData: ProtectedData = { protected_phrases: DEFAULT_PROTECTED_PHRASES };
            saveProtectedPhrases(workspace, defaultData);
            this.protectedPhrases = DEFAULT_PROTECTED_PHRASES;
            vscode.window.showInformationMessage(this.l10n.t('success.phrasesReset'));
        }
    }

    async setProtectStatus(enabled: boolean) {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        setProtectStatus(workspace, enabled);
        this.protectEnabled = enabled;
        
        // Reload webview to update status
        if (this._view) {
            this._view.webview.html = this.getWebviewContent();
        }

        vscode.window.showInformationMessage(
            enabled ? this.l10n.t('success.protectionEnabled') : this.l10n.t('success.protectionDisabled')
        );
    }

    async showProtectStatus() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const protectedData = loadProtectedPhrases(workspace);
        const status = isProtectEnabled(workspace) ? this.l10n.t('protection.active') : this.l10n.t('protection.inactive');
        
        const message = this.l10n.t('protection.statusDetailsFull', status, protectedData.protected_phrases.length.toString());
        
        vscode.window.showInformationMessage(message);
    }

    showProgressOutput() {
        this.progressOutput.show();
    }

    // 🔄 Changelog Functions
    async autoSetupChangelog() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        this.progressOutput.show();
        this.progressOutput.clear();
        
        const timestamp = new Date().toLocaleTimeString();
        this.progressOutput.appendLine(this.l10n.t('changelog.autoSettingUp'));

        if (addChangelogSectionToReadme(workspace)) {
            this.progressOutput.appendLine(this.l10n.t('success.changelogSetupCompleted'));
            vscode.window.showInformationMessage(this.l10n.t('success.changelogSectionAdded'));
        } else {
            this.progressOutput.appendLine(this.l10n.t('errors.changelogSetupFailed'));
            vscode.window.showErrorMessage(this.l10n.t('errors.changelogSetupFailed'));
        }
    }

    async translateChangelog() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        if (!hasChangelogFile(workspace)) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noChangelogFile'));
            return;
        }

        const result = await vscode.window.showQuickPick(
            [
                {
                    label: this.l10n.t('languages.all'),
                    description: this.l10n.t('changelog.translateAll')
                },
                {
                    label: this.l10n.t('languages.selected'), 
                    description: this.l10n.t('changelog.translateSelected', this.selectedLanguages.size.toString())
                }
            ],
            {
                placeHolder: this.l10n.t('changelog.selectLanguages')
            }
        );

        if (!result) {
            return;
        }

        const langCodes = result.label === this.l10n.t('languages.all') 
            ? Array.from(Object.keys(LANGUAGES))
            : Array.from(this.selectedLanguages);

        if (langCodes.length === 0) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noLanguagesSelected'));
            return;
        }

        this.progressOutput.show();
        this.progressOutput.clear();
        
        const timestamp = new Date().toLocaleTimeString();
        this.progressOutput.appendLine(this.l10n.t('changelog.translatingChangelog', langCodes.length.toString()));

        const success = await translateChangelogOnly(langCodes, workspace, this.progressOutput);

        if (success) {
            this.progressOutput.appendLine(this.l10n.t('success.changelogTranslationCompleted'));
            vscode.window.showInformationMessage(this.l10n.t('success.changelogTranslated', langCodes.length.toString()));
        } else {
            this.progressOutput.appendLine(this.l10n.t('errors.changelogTranslationFailed'));
            vscode.window.showErrorMessage(this.l10n.t('errors.changelogTranslationFailed'));
        }
    }

    // 🔄 GitHub URL Detection Function
    async detectGitHubUrl() {
        const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspace) {
            vscode.window.showErrorMessage(this.l10n.t('errors.noWorkspace'));
            return;
        }

        const repoUrl = getGitHubRepoUrl(workspace);
        const releasesUrl = getGitHubReleasesUrl(workspace);

        if (repoUrl) {
            this.output.show();
            this.output.appendLine(this.l10n.t('github.detectionResults'));
            this.output.appendLine(this.l10n.t('github.repositoryUrl', repoUrl));
            this.output.appendLine(this.l10n.t('github.releasesUrl', releasesUrl));
            this.output.appendLine("");
            this.output.appendLine(this.l10n.t('github.sourcesChecked'));
            this.output.appendLine(this.l10n.t('github.sourcePackageJson'));
            this.output.appendLine(this.l10n.t('github.sourceGitConfig'));
            this.output.appendLine(this.l10n.t('github.sourceReadme'));
            
            vscode.window.showInformationMessage(
                this.l10n.t('success.githubUrlDetected', repoUrl, releasesUrl),
                { modal: true }
            );
        } else {
            vscode.window.showWarningMessage(
                this.l10n.t('errors.githubUrlNotDetected'),
                { modal: true }
            );
        }
    }
}