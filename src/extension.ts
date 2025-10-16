import * as vscode from "vscode";
import * as fs from "fs";
import * as path from "path";
import fetch from "node-fetch";

// 🌍 Daftar bahasa target
const LANGUAGES: Record<string, [string, string, string]> = {
  id: ["Bahasa Indonesia", "id", "🌐 Tersedia dalam bahasa lain:"],
  fr: ["Français", "fr", "🌐 Disponible dans d'autres langues :"],
  de: ["Deutsch", "de", "🌐 In anderen Sprachen verfügbar:"],
  jp: ["日本語", "ja", "🌐 他の言語でも利用可能:"],
  zh: ["中文", "zh", "🌐 提供其他语言版本："],
  es: ["Español", "es", "🌐 Disponible en otros idiomas:"],
  pl: ["Polski", "pl", "🌐 Dostępne w innych językach:"],
  ru: ["Русский", "ru", "🌐 Доступно на других языках:"],
  pt: ["Português", "pt", "🌐 Disponível em outros idiomas:"],
  ko: ["한국어", "ko", "🌐 다른 언어로도 사용 가능:"],
};

async function translateWithGoogle(text: string, from: string, to: string): Promise<string> {
  if (!text.trim() || /^[_\s0-9]+$/.test(text.replace(/__p/g, ''))) {
    return text;
  }
  const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${from}&tl=${to}&dt=t&q=${encodeURIComponent(
    text
  )}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  const data: any = await res.json();
  return data[0]?.map((item: any) => item[0]).join("") || text;
}

export function activate(context: vscode.ExtensionContext) {
  const provider = new TranslateSidebarProvider(context.extensionUri);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("autoTranslateView", provider)
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("auto-translate-readmes.run", () =>
      provider.generateReadmes()
    )
  );
}

class TranslateSidebarProvider implements vscode.WebviewViewProvider {
  private _view?: vscode.WebviewView;
  private readonly output = vscode.window.createOutputChannel("Auto Translate Readmes");

  constructor(private readonly _extensionUri: vscode.Uri) {}

  resolveWebviewView(webviewView: vscode.WebviewView) {
    this._view = webviewView;
    webviewView.webview.options = { enableScripts: true };
    webviewView.webview.html = this._getHtml();
    webviewView.webview.onDidReceiveMessage(async (msg) => {
      if (msg.command === "run") {
        await this.generateReadmes();
      }
      if (msg.command === "saveKey") {
        const config = vscode.workspace.getConfiguration("autoTranslateReadmes");
        await config.update("apiKey", msg.apiKey.trim(), vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage("🔑 API Key disimpan ke settings.json");
      }
    });
  }

  private _getHtml(): string {
    const config = vscode.workspace.getConfiguration("autoTranslateReadmes");
    const savedKey = config.get("apiKey", "");
    return /* html */ `
      <html>
        <body style="font-family:sans-serif;padding:12px;">
          <h3>🌍 Auto Translate READMEs</h3>
          <p>Gunakan Google Translate gratis (tanpa API Key wajib)</p>
          <label>API Key (opsional)</label>
          <input id="apiKey" type="text" value="${savedKey}" placeholder="Masukkan API Key (opsional)" style="width:100%;margin-bottom:8px;padding:6px;" />
          <button id="saveBtn" style="width:100%;padding:6px;margin-bottom:10px;">💾 Simpan API Key</button>
          <button id="runBtn" style="width:100%;padding:8px;background:#007acc;color:white;border:none;border-radius:4px;cursor:pointer;">⚙️ Generate Multilingual READMEs</button>
          <script>
            const vscode = acquireVsCodeApi();
            document.getElementById('saveBtn').addEventListener('click', () => vscode.postMessage({ command: 'saveKey', apiKey: document.getElementById('apiKey').value }));
            document.getElementById('runBtn').addEventListener('click', () => vscode.postMessage({ command: 'run' }));
          </script>
        </body>
      </html>`;
  }

  async generateReadmes() {
    const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspace) {
      return vscode.window.showErrorMessage("❌ No workspace open.");
    }

    const srcPath = path.join(workspace, "README.md");
    if (!fs.existsSync(srcPath)) {
      return vscode.window.showErrorMessage("README.md not found.");
    }

    let originalText = fs.readFileSync(srcPath, "utf-8");

    if (!originalText.includes("> 🌐")) {
      const parts = originalText.split(/\n-{3,}\n/);
      const headerPart = parts[0] || "";
      const bodyPart = parts.slice(1).join("\n---\n");
      const langLinks = Object.entries(LANGUAGES).map(([code, [name]]) => `[${name}](docs/lang/README-${code.toUpperCase()}.md)`).join(" | ");
      const multilingualBlock = `> 🌐 Available in other languages: ${langLinks}`;
      const newContent = `${headerPart.trim()}\n\n${multilingualBlock}\n\n---\n${bodyPart}`;
      fs.writeFileSync(srcPath, newContent, "utf-8");
      originalText = newContent;
    }

    const parts = originalText.split(/\n-{3,}\n/);
    const headerPart = parts[0] || "";
    const bodyPart = parts.slice(1).join("\n---\n");
    const cleanedHeader = headerPart.split("\n").filter(line => !line.includes("🌐") && !line.match(/\(README-[A-Z]{2}\.md\)/) && !line.match(/\(\.\.\/\.\.\/README\.md\)/)).join("\n").trim();
    const outDir = path.join(workspace, "docs", "lang");
    fs.mkdirSync(outDir, { recursive: true });

    this.output.clear();
    this.output.appendLine("=== Auto Translate Readmes ===");
    this.output.appendLine(`📁 Workspace: ${workspace}`);
    this.output.appendLine("--------------------------------");

    for (const [code, [name, lang, intro]] of Object.entries(LANGUAGES)) {
      this.output.appendLine(`🌐 Translating → ${name}`);
      try {
        const bodyLines = bodyPart.split('\n');
        const translatedLines: string[] = [];
        let inCodeBlock = false;

        for (const line of bodyLines) {
          if (line.trim().startsWith('```')) {
            inCodeBlock = !inCodeBlock;
            translatedLines.push(line);
            continue;
          }

          // --- PERBAIKAN UTAMA DI SINI ---
          // Regex untuk mendeteksi baris tabel (e.g., |---|---|) dibuat lebih akurat
          const isStructural = inCodeBlock || /^\s*\|?[-:|\s]+\|?\s*$/.test(line) || line.trim() === '';
          if (isStructural && !/^\s*[-*]\s/.test(line)) { // Pastikan bukan baris list biasa
            translatedLines.push(line);
            continue;
          }

          let prefix = '';
          let content = line;

          const prefixMatch = line.match(/^(\s*[-*–]\s+)/);
          if (prefixMatch) {
            prefix = prefixMatch[0];
            content = line.substring(prefix.length);
          }

          const contentPlaceholders: Record<string, string> = {};
          let contentCounter = 0;
          let tempContent = content;

          const protectInContent = (regex: RegExp) => {
            tempContent = tempContent.replace(regex, (match) => {
              const key = `__p${contentCounter++}__`;
              contentPlaceholders[key] = match;
              return key;
            });
          };

          protectInContent(/\[.*?\]\(.*?\)|https?:\/\/\S+/g);
          protectInContent(/\*\*.*?\*\*/g);
          protectInContent(/`[^`]+`/g);

          const translatedContentRaw = await translateWithGoogle(tempContent, 'en', lang);
          
          let restoredContent = translatedContentRaw;
          Object.keys(contentPlaceholders).sort((a, b) => a.localeCompare(b, undefined, { numeric: true })).reverse().forEach(key => {
            restoredContent = restoredContent.replace(key, contentPlaceholders[key]);
          });
          
          translatedLines.push(prefix + restoredContent);
        }

        const translatedBody = translatedLines.join('\n');
        const links = ["[English](../../README.md)"];
        for (const [c, [n]] of Object.entries(LANGUAGES)) {
          if (c !== code) {
            links.push(`[${n}](README-${c.toUpperCase()}.md)`);
          }
        }
        const multilingualBlock = `> ${intro} ${links.join(" | ")}\n\n---\n`;
        const finalReadme = `${cleanedHeader}\n\n${multilingualBlock}${translatedBody}`;

        const dest = path.join(outDir, `README-${code.toUpperCase()}.md`);
        if (fs.existsSync(dest)) {
          fs.unlinkSync(dest);
        }
        const fixedReadme = finalReadme.replace(/\(LICENSE\)/g, "(../../LICENSE)");
        fs.writeFileSync(dest, fixedReadme, "utf-8");

        this.output.appendLine(`✅ ${name} done.`);
      } catch (e: any) {
        this.output.appendLine(`❌ ${name} failed: ${e.message}`);
      }
    }
    vscode.window.showInformationMessage("✅ All READMEs translated successfully!");
    this.output.appendLine("--------------------------------");
    this.output.appendLine("✅ All READMEs translated successfully!");
    this.output.show(true);
  }
}

export function deactivate() {}