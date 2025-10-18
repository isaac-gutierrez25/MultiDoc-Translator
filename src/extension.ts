/* src/extension.ts */
import * as vscode from "vscode";
import * as fs from "fs";
import * as path from "path";
import fetch from "node-fetch";

// 🌍 Bahasa yang didukung
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

// 🌐 Translate via Google
async function translateWithGoogle(text: string, to: string): Promise<string> {
  if (!text.trim()) return text;
  const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${to}&dt=t&q=${encodeURIComponent(text)}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data: any = await res.json();
    return data[0]?.map((seg: any) => seg[0]).join("") || text;
  } catch {
    return text;
  }
}

// 🌟 Activate Extension
export function activate(context: vscode.ExtensionContext) {
  const provider = new TranslateSidebarProvider(context.extensionUri);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("autoTranslateView", provider),
    vscode.commands.registerCommand("auto-translate-readmes.run", () =>
      provider.generateReadmes()
    )
  );
}

class TranslateSidebarProvider implements vscode.WebviewViewProvider {
  private _view?: vscode.WebviewView;
  private readonly output = vscode.window.createOutputChannel("Auto Translate Readmes");

  constructor(private readonly _uri: vscode.Uri) {}

  resolveWebviewView(view: vscode.WebviewView) {
    this._view = view;
    view.webview.options = { enableScripts: true };
    view.webview.html = `
      <html>
        <body style="font-family:sans-serif;padding:12px;">
          <h3>🌍 Auto Translate READMEs</h3>
          <button id="runBtn" style="width:100%;padding:8px;background:#007acc;color:white;border:none;border-radius:4px;">
            ⚙️ Generate Multilingual READMEs
          </button>
          <script>
            const vscode = acquireVsCodeApi();
            document.getElementById('runBtn').addEventListener('click', ()=>vscode.postMessage({command:'run'}));
          </script>
        </body>
      </html>`;
    view.webview.onDidReceiveMessage(async (msg) => {
      if (msg.command === "run") await this.generateReadmes();
    });
  }

  async generateReadmes() {
    const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspace) return vscode.window.showErrorMessage("❌ No workspace open.");

    const srcPath = path.join(workspace, "README.md");
    if (!fs.existsSync(srcPath))
      return vscode.window.showErrorMessage("README.md not found.");

    let originalText = fs.readFileSync(srcPath, "utf-8");

    // Tambahkan language switcher jika belum ada
    if (!originalText.includes("> 🌐")) {
      const parts = originalText.split(/\n-{3,}\n/);
      const header = parts[0] || "";
      const body = parts.slice(1).join("\n---\n");
      const langLinks = Object.entries(LANGUAGES)
        .map(([code, [name]]) => `[${name}](docs/lang/README-${code.toUpperCase()}.md)`)
        .join(" | ");
      originalText = `${header.trim()}\n\n> 🌐 Available in other languages: ${langLinks}\n\n---\n${body}`;
      fs.writeFileSync(srcPath, originalText, "utf-8");
    }

    const outDir = path.join(workspace, "docs", "lang");
    fs.mkdirSync(outDir, { recursive: true });

    const [headerPart, ...bodyParts] = originalText.split(/\n-{3,}\n/);
    const bodyPart = bodyParts.join("\n---\n");

    for (const [code, [langName, langCode, intro]] of Object.entries(LANGUAGES)) {
      this.output.appendLine(`🌐 Translating to ${langName}...`);

      const cleanedHeader = headerPart.replace(/^\s*>\s*🌐.*$/m, "").trim();
      const links = ["[English](../../README.md)"];
      for (const [c, [n]] of Object.entries(LANGUAGES)) {
        if (c !== code) links.push(`[${n}](README-${c.toUpperCase()}.md)`);
      }
      const finalHeader = `${cleanedHeader}\n\n> ${intro} ${links.join(" | ")}`;

      const lines = bodyPart.split(/\r?\n/);
      const translatedLines: string[] = [];
      let inCodeBlock = false;

      for (const rawLine of lines) {
        const line = rawLine;
        if (line.trim().startsWith("```")) {
          inCodeBlock = !inCodeBlock;
          translatedLines.push(line);
          continue;
        }

        const isStructural =
          inCodeBlock || /^\s*\|?[-:|\s]+\|?\s*$/.test(line) || !line.trim();
        if (isStructural) {
          translatedLines.push(line);
          continue;
        }

        const placeholders: Record<string, string> = {};
        let counter = 0;

        let temp = line;
        // Lindungi bagian penting agar tidak diterjemahkan
        const protect = (regex: RegExp) => {
          temp = temp.replace(regex, (m) => {
            const key = `__p${counter++}__`;
            placeholders[key] = m;
            return key;
          });
        };

        protect(/\[.*?\]\(.*?\)/g);
        protect(/https?:\/\/\S+/g);
        protect(/`[^`]+`/g);
        protect(/\*\*[^*]+\*\*/g);

        let translated = await translateWithGoogle(temp, langCode);

        // Pulihkan placeholder
        for (const key of Object.keys(placeholders)) {
          translated = translated.replace(key, placeholders[key]);
        }

        // 🔧 FIX 1: Pastikan bold di awal tidak pecah (* *Before:**)
        translated = translated
          .replace(/^\*\s*\*([^*]+)\*\s*\*$/, "**$1**")
          .replace(/^\s*\*\s*\*([^*]+)\*\s*$/, "**$1**")
          .replace(/^\s*\*\*([^*]+)\*\s*\*$/, "**$1**");

        // 🔧 FIX 2: Pastikan list tetap punya spasi setelah tanda (- / *) tapi tidak mengenai bold
        translated = translated.replace(/^(\s*[-*])(?!\*)([^\s\-*])/u, "$1 $2");

        // Kembalikan indentasi asli
        const indent = rawLine.match(/^\s*/)?.[0] ?? "";
        translatedLines.push(indent + translated.trimEnd());
      }

      const translatedBody = translatedLines.join("\n");
      const finalContent = `${finalHeader}\n\n---\n${translatedBody}`;
      const dest = path.join(outDir, `README-${code.toUpperCase()}.md`);

      fs.writeFileSync(dest, finalContent.replace(/\(LICENSE\)/g, "(../../LICENSE)"), "utf-8");
      this.output.appendLine(`✅ ${langName} done.`);
    }

    vscode.window.showInformationMessage("✅ All READMEs translated successfully!");
  }
}

export function deactivate() {}
