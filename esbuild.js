// esbuild.js
const { build } = require('esbuild');

build({
  entryPoints: ['src/extension.ts'],
  bundle: true,
  outfile: 'dist/extension.js', // Output ke folder 'dist'
  platform: 'node',
  target: 'node16', // Sesuaikan dengan target Node.js Anda
  external: ['vscode'], // Jangan bundle 'vscode', karena sudah disediakan oleh VS Code
  sourcemap: true,
}).catch(() => process.exit(1));