import { defineConfig } from 'vite';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));

// 본체(../index.html)를 토스 빌드용으로 동기화하는 플러그인
function syncRootApp() {
  const run = () => execSync('node sync.js', { stdio: 'inherit', cwd: here });
  return {
    name: 'sync-root-app',
    buildStart() { run(); },
    configureServer() { run(); },
  };
}

export default defineConfig({
  plugins: [syncRootApp()],
});
