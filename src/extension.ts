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

/**
 * 🌐 Google Translate gratis (tanpa API key wajib)
 */
async function translateWithGoogle(text: string, from: string, to: string): Promise<string> {
  const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${from}&tl=${to}&dt=t&q=${encodeURIComponent(
    text
  )}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  return data[0]?.map((item: any) => item[0]).join("") || "Tidak ada hasil terjemahan";
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

    // Terima pesan dari webview
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

  /**
   * 🧩 Sidebar UI HTML
   */
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
            document.getElementById('saveBtn').addEventListener('click', () => {
              const apiKey = document.getElementById('apiKey').value;
              vscode.postMessage({ command: 'saveKey', apiKey });
            });
            document.getElementById('runBtn').addEventListener('click', () => {
              vscode.postMessage({ command: 'run' });
            });
          </script>
        </body>
      </html>`;
  }

  /**
   * ⚙️ Generate README translations
   */
  async generateReadmes() {
    const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspace)
      return vscode.window.showErrorMessage("❌ No workspace open.");

    const srcPath = path.join(workspace, "README.md");
    if (!fs.existsSync(srcPath))
      return vscode.window.showErrorMessage("README.md not found.");

    // === Baca README utama ===
    let originalText = fs.readFileSync(srcPath, "utf-8");

    // === Tambahkan language switcher ke README root jika belum ada ===
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
        originalText = newContent; // Perbarui variabel dengan konten baru
        this.output.appendLine("✅ Language switcher block added to root README.md.");
        vscode.window.showInformationMessage("Language switcher added to root README.md.");
    }

    // Pisahkan header dan body (semua teks setelah --- pertama dianggap body)
    const parts = originalText.split(/\n-{3,}\n/);
    const headerPart = parts[0] || "";
    const bodyPart = parts.slice(1).join("\n---\n");

    // === Bersihkan blok multi-bahasa lama di header ===
    const cleanedHeader = headerPart
      .split("\n")
      .filter(
        (line) =>
          !line.includes("🌐") &&
          !line.match(/\(README-[A-Z]{2}\.md\)/) &&
          !line.match(/\(\.\.\/\.\.\/README\.md\)/)
      )
      .join("\n")
      .trim();

    // === Siapkan folder output ===
    const outDir = path.join(workspace, "docs", "lang");
    fs.mkdirSync(outDir, { recursive: true });

    this.output.clear();
    this.output.appendLine("=== Auto Translate Readmes ===");
    this.output.appendLine(`📁 Workspace: ${workspace}`);
    this.output.appendLine("--------------------------------");

    // === Loop untuk setiap bahasa ===
    for (const [code, [name, lang, intro]] of Object.entries(LANGUAGES)) {
      const dest = path.join(outDir, `README-${code.toUpperCase()}.md`);
      vscode.window.showInformationMessage(`🌐 Translating to ${name}...`);
      this.output.appendLine(`🌐 Translating → ${name}`);

      try {
        const placeholderMap: Record<string, string> = {};
        let tempBody = bodyPart;
        let counter = 0;
        
        // 1. Pemisah tabel Markdown
        tempBody = tempBody.replace(/^\|[-| :]+\|/gm, (match) => {
            const key = `@@TABLE_SEPARATOR_${counter++}@@`;
            placeholderMap[key] = match;
            return key;
        });

        // 2. Blok Kode
        tempBody = tempBody.replace(/```[\s\S]*?```/g, (match) => {
          const key = `@@CODEBLOCK_${counter++}@@`;
          placeholderMap[key] = match;
          return key;
        });

        // 3. Kode Inline
        tempBody = tempBody.replace(/`[^`]+`/g, (match) => {
          const key = `@@INLINECODE_${counter++}@@`;
          placeholderMap[key] = match;
          return key;
        });

        // 4. Link & URL
        tempBody = tempBody.replace(/\[.*?\]\(.*?\)|https?:\/\/\S+/g, (match) => {
          const key = `@@LINK_${counter++}@@`;
          placeholderMap[key] = match;
          return key;
        });

        // 🌐 Lindungi placeholder agar tidak diterjemahkan
        for (const key of Object.keys(placeholderMap)) {
          const safeKey = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
          const regex = new RegExp(safeKey, "g");
          tempBody = tempBody.replace(regex, `<span class="notranslate">${key}</span>`);
        }

        // 🔄 Terjemahkan body penuh
        const translatedBodyRaw = await translateWithGoogle(tempBody, "en", lang);

        // 🧹 Hapus tag pelindung
        let translatedBody = translatedBodyRaw.replace(/<span class="notranslate">(.*?)<\/span>/g, "$1");

        // 🔁 Pulihkan placeholder
        for (const [key, val] of Object.entries(placeholderMap)) {
          const safeKey = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
          const regex = new RegExp(safeKey, "g");
          translatedBody = translatedBody.replace(regex, val);
        }
        
        // Normalkan format list Markdown
        translatedBody = translatedBody.replace(/^\s*(-|\*|–)\s*(.*)/gm, "- $2");

        // 🌍 Blok tautan antar bahasa
        const links = ["[English](../../README.md)"];
        for (const [c, [n]] of Object.entries(LANGUAGES)) {
          if (c !== code) links.push(`[${n}](README-${c.toUpperCase()}.md)`);
        }
        const multilingualBlock = `> ${intro} ${links.join(" | ")}\n\n---\n`;

        // 🧾 Gabungkan hasil akhir
        const finalReadme = `${cleanedHeader}\n\n${multilingualBlock}${translatedBody.trim()}`;

        // 🧹 Hapus file lama & betulkan link LICENSE
        if (fs.existsSync(dest)) fs.unlinkSync(dest);
        const fixedReadme = finalReadme.replace(/\(LICENSE\)/g, "(../../LICENSE)");

        // 💾 Simpan hasil
        fs.writeFileSync(dest, fixedReadme, "utf-8");

        // --- PERBAIKAN DI SINI ---
        this.output.appendLine(`✅ ${name} done.`);
      } catch (e: any) {
        vscode.window.showErrorMessage(`❌ ${name}: ${e.message}`);
        this.output.appendLine(`❌ ${name} failed: ${e.message}`);
      }
    }

    vscode.window.showInformationMessage("✅ Semua README berhasil diterjemahkan!");
    this.output.appendLine("--------------------------------");
    this.output.appendLine("✅ Semua README berhasil diterjemahkan!");
    this.output.show(true);
    // --- AKHIR PERBAIKAN ---
  }
}

export function deactivate() {}