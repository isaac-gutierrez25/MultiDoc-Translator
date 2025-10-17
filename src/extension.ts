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
  if (!text.trim()) {
    return text;
  }
  const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${from}&tl=${to}&dt=t&q=${encodeURIComponent(text)}`;
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
        <head>
          <style>
            .spinning { display: inline-block; animation: spin 1s linear infinite; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
          </style>
        </head>
        <body style="font-family:sans-serif;padding:12px;">
          <h3>🌍 Auto Translate READMEs</h3>
          <p>Gunakan Google Translate gratis (tanpa API Key wajib)</p>
          <label>API Key (opsional)</label>
          <input id="apiKey" type="text" value="${savedKey}" placeholder="Masukkan API Key (opsional)" style="width:100%;margin-bottom:8px;padding:6px;" />
          <button id="saveBtn" style="width:100%;padding:6px;margin-bottom:10px;">💾 Simpan API Key</button>
          
          <button id="runBtn" style="width:100%;padding:8px;background:#007acc;color:white;border:none;border-radius:4px;cursor:pointer;">
            <span id="runIcon">⚙️</span> Generate Multilingual READMEs
          </button>

          <script>
            const vscode = acquireVsCodeApi();
            const runBtn = document.getElementById('runBtn');
            const runIcon = document.getElementById('runIcon');
            document.getElementById('saveBtn').addEventListener('click', () => {
              vscode.postMessage({ command: 'saveKey', apiKey: document.getElementById('apiKey').value });
            });
            runBtn.addEventListener('click', () => {
              runIcon.classList.add('spinning');
              runBtn.disabled = true;
              vscode.postMessage({ command: 'run' });
            });
            window.addEventListener('message', event => {
              const message = event.data;
              if (message.command === 'translationFinished') {
                runIcon.classList.remove('spinning');
                runBtn.disabled = false;
              }
            });
          </script>
        </body>
      </html>`;
  }

  async generateReadmes() {
    const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspace) {
      if (this._view) { this._view.webview.postMessage({ command: 'translationFinished' }); }
      return vscode.window.showErrorMessage("❌ No workspace open.");
    }

    try {
      vscode.window.showInformationMessage("🌍 Starting README translation process...");
      this.output.show(true);

      const srcPath = path.join(workspace, "README.md");
      if (!fs.existsSync(srcPath)) {
        if (this._view) { this._view.webview.postMessage({ command: 'translationFinished' }); }
        return vscode.window.showErrorMessage("README.md not found.");
      }

      let originalText = fs.readFileSync(srcPath, "utf-8");

      // Tambahkan language switcher jika belum ada
      if (!originalText.includes("> 🌐")) {
        const parts = originalText.split(/\n-{3,}\n/);
        const headerPart = parts[0] || "";
        const bodyPart = parts.slice(1).join("\n---\n");
        const langLinks = Object.entries(LANGUAGES)
          .map(([code, [name]]) => `[${name}](docs/lang/README-${code.toUpperCase()}.md)`)
          .join(" | ");
        const multilingualBlock = `> 🌐 Available in other languages: ${langLinks}`;
        const newContent = `${headerPart.trim()}\n\n${multilingualBlock}\n\n---\n${bodyPart}`;
        fs.writeFileSync(srcPath, newContent, "utf-8");
        originalText = newContent;
      }

      const outDir = path.join(workspace, "docs", "lang");
      fs.mkdirSync(outDir, { recursive: true });

      this.output.clear();
      this.output.appendLine("=== Auto Translate Readmes ===");
      this.output.appendLine(`📁 Workspace: ${workspace}`);
      this.output.appendLine("--------------------------------");

      const parts = originalText.split(/\n-{3,}\n/);
      const headerPart = parts[0] || "";
      const bodyPart = parts.slice(1).join("\n---\n");

      for (const [code, [name, lang, intro]] of Object.entries(LANGUAGES)) {
        this.output.appendLine(`🌐 Translating → ${name}`);
        try {
          const cleanedHeader = headerPart.replace(/^\s*>\s*🌐.*$/m, "").trim();
          const links = ["[English](../../README.md)"];
          for (const [c, [n]] of Object.entries(LANGUAGES)) {
            if (c !== code) {
              links.push(`[${n}](README-${c.toUpperCase()}.md)`);
            }
          }
          const newSwitcher = `> ${intro} ${links.join(" | ")}`;
          const finalHeader = `${cleanedHeader}\n\n${newSwitcher}`;

          const placeholders: Record<string, string> = {};
          let counter = 0;
          let tempBody = bodyPart;

          // Lindungi bagian penting agar tidak diterjemahkan
          const protect = (regex: RegExp) => {
            tempBody = tempBody.replace(regex, (match: any) => {
              const key = `__p${counter++}__`;
              placeholders[key] = match;
              return key;
            });
          };
          protect(/^\s*```[\s\S]*?^\s*```/gm);
          protect(/^\s*\|?[-:|\s]+\|?\s*$/gm);
          protect(/\[.*?\]\(.*?\)|https?:\/\/\S+/g);
          protect(/\*\*.*?\*\*/g);
          protect(/`[^`]+`/g);

          // Bagi berdasarkan newline tapi tetap pertahankan struktur
          const lines = tempBody.split(/(\n)/);
          const translatedLines: string[] = [];

          for (const line of lines) {
            // skip markup
            if (
              !line.trim() ||
              /^(\s*[-*]|#+|\|.*\||```|>|<|!\[|\[.*?\]\(.*?\))/m.test(line)
            ) {
              translatedLines.push(line);
              continue;
            }
            try {
              const translatedLine = await translateWithGoogle(line, "en", lang);
              translatedLines.push(translatedLine);
            } catch (e: any) {
              this.output.appendLine(`⚠️  Skipping line due to translation error: ${e.message}`);
              translatedLines.push(line);
            }
          }

          // Jangan ubah newline sama sekali
          const translatedBody = translatedLines.join("");

          // Pulihkan placeholder
          let restoredBody = translatedBody;
          Object.keys(placeholders)
            .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
            .reverse()
            .forEach((key) => {
              restoredBody = restoredBody.replace(key, placeholders[key]);
            });

          const finalReadme = `${finalHeader}\n\n---\n${restoredBody}`;
          const dest = path.join(outDir, `README-${code.toUpperCase()}.md`);
          const fixedReadme = finalReadme.replace(/\(LICENSE\)/g, "(../../LICENSE)");
          fs.writeFileSync(dest, fixedReadme, { encoding: "utf-8", flag: "w" });

          this.output.appendLine(`✅ ${name} done.`);
        } catch (e: any) {
          this.output.appendLine(`❌ ${name} failed: ${e.message}`);
        }
      }

      vscode.window.showInformationMessage("✅ All READMEs translated successfully!");
      this.output.appendLine("--------------------------------");
      this.output.appendLine("✅ All READMEs translated successfully!");
    } catch (error: any) {
      vscode.window.showErrorMessage(`An error occurred: ${error.message}`);
    } finally {
      if (this._view) {
        this._view.webview.postMessage({ command: "translationFinished" });
      }
    }
  }
}

export function deactivate() {}
