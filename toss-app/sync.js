// 본체(../index.html + 데이터)를 토스 미니앱 빌드용으로 동기화한다.
// - 토스 어댑터 스크립트 주입
// - PWA 요소(manifest, service worker) 제거 (토스 웹뷰에서 불필요)
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const HERE = __dirname;
const PUB = path.join(HERE, 'public');

let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

const replaces = [
  ['<link rel="manifest" href="manifest.json">\n', ''],
  ["navigator.serviceWorker.register('sw.js').catch(() => {});", '/* toss build: service worker 미사용 */'],
  ['</body>', '<script type="module" src="/src/toss-adapter.js"></script>\n</body>'],
];
for (const [from, to] of replaces) {
  if (!html.includes(from)) {
    console.warn(`[sync] 경고: 대상 문자열을 찾지 못함 → ${from.slice(0, 50)}`);
    continue;
  }
  html = html.replace(from, to);
}
fs.writeFileSync(path.join(HERE, 'index.html'), html);

fs.mkdirSync(PUB, { recursive: true });
for (const f of ['korea-spots.json', 'icon-180.png', 'icon-192.png', 'icon-512.png', 'privacy.html']) {
  fs.copyFileSync(path.join(ROOT, f), path.join(PUB, f));
}
console.log('[sync] 완료: index.html 변환 + 정적 파일 복사');
